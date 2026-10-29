# Compatibility vectors

SPEC.md §18.6: every valid vector of version N−1 must validate under version N's schemas.

Each folder holds the valid examples exactly as they were published for that version. They are never edited. `python tools/validate.py` checks each one twice: once against its own version's schemas and once against the current ones. If a schema change breaks one, the check fails, so a backward-compatibility break shows up as a failing test instead of a production incident.

| Folder | Frozen from | Checked against |
|---|---|---|
| [`0.5/`](0.5/) | `examples/valid/` at arc/0.5 | `schemas/0.5/` and `schemas/0.7/` |

When a new version ships, copy the current `examples/valid/` here under the outgoing version's number.
