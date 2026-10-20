#!/usr/bin/env python3
"""Recompute the signing test vectors and check they match.

Usage: python tools/verify_vectors.py      (needs: pip install cryptography)
"""
import json, sys
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
sys.path.insert(0, str(Path(__file__).parent))
from arc_sign import canonicalize, body_hash, sign_detached, verify_detached, did_key

V = Path(__file__).resolve().parent.parent / "test-vectors" / "signing"
key = json.loads((V / "test-key.json").read_text())
env = json.loads((V / "receipt-envelope.json").read_text())
exp = json.loads((V / "expected.json").read_text())

sk = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(key["private_key_hex"]))
pk = sk.public_key()
checks = {
    "did:key derives from the public key": did_key(pk) == key["did"] == env["issuer"],
    "canonical body matches (JCS)": canonicalize(env["body"]).decode() == exp["canonical_body"],
    "body hash matches": body_hash(env["body"]) == exp["body_hash"],
    "signature is reproducible (Ed25519 is deterministic)": sign_detached(env["body"], sk, key["kid"]) == exp["sig"] == env["sig"],
    "signature verifies": verify_detached(env["body"], env["sig"], pk),
    "tampered body is rejected": not verify_detached({**env["body"], "units": {"unit": "page", "count": 13}}, env["sig"], pk),
}
for name, ok in checks.items():
    print(("ok    " if ok else "FAIL  ") + name)
print("READY." if all(checks.values()) else "failed")
sys.exit(0 if all(checks.values()) else 1)
