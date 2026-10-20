# Signing test vectors

One `arc/receipt` envelope signed for real, so you can check your canonicalization, hashing and signing code against known values.

| File | Contents |
|---|---|
| `test-key.json` | A **public test key** (Ed25519) and its `did:key`. Anyone can sign with it, so never use it outside tests. |
| `receipt-envelope.json` | The signed envelope. Its body is [`examples/valid/receipt.settled.json`](../../examples/valid/receipt.settled.json). |
| `expected.json` | The canonical body (JCS), its hash, the JWS protected header, the signing input and the signature |

## How the signature is made

1. Canonicalize the body with JCS (RFC 8785). Hash it with SHA-256 → `sha256:<hex>`.
2. Build a JWS protected header: `{"alg":"EdDSA","kid":"<did>#<key-id>"}`.
3. Signing input: `BASE64URL(header) + "." + BASE64URL(JCS(body))`.
4. Sign with Ed25519. Publish the result as a detached JWS: `header..signature`, with the payload left out (RFC 7515, Appendix F).

To verify, rebuild the signing input from the body you received and check the signature against the key in the issuer's DID document.

`python tools/verify_vectors.py` recomputes every value and also checks that a tampered body is rejected.

> The spec says "detached JWS" but doesn't yet name the variant. These vectors use the RFC 7515 Appendix F form with a base64url-encoded payload. Pinning this down in SPEC.md is tracked for arc/0.6.
