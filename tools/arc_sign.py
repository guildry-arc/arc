"""Minimal reference helpers for ARC signing (arc/0.5). Test use only.

- canonicalize(): RFC 8785 (JCS) for the JSON this repo uses: objects, arrays, strings,
  integers and booleans. Non-integer numbers are rejected rather than risk a wrong encoding.
- body_hash(): "sha256:<hex>" over the canonical body.
- sign_detached() / verify_detached(): JWS compact serialization with detached payload
  (RFC 7515 Appendix F), alg EdDSA (Ed25519), payload = JCS(body).
"""
import base64, hashlib, json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

def _b64u(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
def _b64u_dec(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

def _check(v):
    if isinstance(v, float): raise ValueError("non-integer numbers are not supported by this helper")
    if isinstance(v, dict): [_check(x) for x in v.values()]
    if isinstance(v, list): [_check(x) for x in v]

def canonicalize(obj) -> bytes:
    _check(obj)
    def key(k): return k.encode("utf-16-be")   # JCS sorts by UTF-16 code units
    def enc(v):
        if isinstance(v, dict):
            return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + enc(v[k]) for k in sorted(v, key=key)) + "}"
        if isinstance(v, list):
            return "[" + ",".join(enc(x) for x in v) + "]"
        return json.dumps(v, ensure_ascii=False)
    return enc(obj).encode("utf-8")

def body_hash(body) -> str:
    return "sha256:" + hashlib.sha256(canonicalize(body)).hexdigest()

def sign_detached(body, key: Ed25519PrivateKey, kid: str) -> str:
    header = _b64u(json.dumps({"alg": "EdDSA", "kid": kid}, separators=(",", ":")).encode())
    signing_input = (header + "." + _b64u(canonicalize(body))).encode()
    return header + ".." + _b64u(key.sign(signing_input))

def verify_detached(body, jws: str, pub: Ed25519PublicKey) -> bool:
    header, empty, sig = jws.split(".")
    if empty: return False
    signing_input = (header + "." + _b64u(canonicalize(body))).encode()
    try:
        pub.verify(_b64u_dec(sig), signing_input); return True
    except Exception:
        return False

def did_key(pub: Ed25519PublicKey) -> str:
    raw = pub.public_bytes_raw()
    data = b"\xed\x01" + raw                       # multicodec ed25519-pub
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(data, "big"); out = ""
    while n: n, r = divmod(n, 58); out = alphabet[r] + out
    out = "1" * (len(data) - len(data.lstrip(b"\0"))) + out
    return "did:key:z" + out
