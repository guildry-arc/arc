# Examples

Every file is a body for the schema named before the first dot: `receipt.settled.json` is checked against `receipt.json`. Envelope examples are checked twice: once as an envelope, then the body against the schema selected by `type`.

- **`valid/`**: at least one example per object. Each one must pass.
- **`invalid/`**: each one breaks exactly one rule and must be rejected. The file name says which rule.

Run `python tools/validate.py` to check them.

Hashes are real SHA-256 values over short labels, so they match the hash format. Signature fields hold a placeholder, because schema validation checks shape, not cryptography. For a signature you can actually verify, see [`test-vectors/signing/`](../test-vectors/signing/).

AIDs use the `mkt.example` registry from the specification. `.example` domains are reserved for documentation (RFC 2606).
