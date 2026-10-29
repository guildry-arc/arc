# Schemas · arc/0.7

JSON Schema draft 2020-12. One schema per object body, plus the envelope and the shared definitions. They constrain structure and syntax only. Rules that span objects (one attestation per receipt per direction, monotonic counter-offers, value floors, buyer-requirements screening) are normative in [SPEC.md](../SPEC.md) and enforced by the registry.

| Schema | Validates | Spec |
|---|---|---|
| [`common.json`](0.7/common.json) | Shared definitions: ARC-AID, DID, hash, money, version, pricing, trial terms, probe status, SLO, rubric, payout table, allocation | §2 |
| [`envelope.json`](0.7/envelope.json) | The envelope every object travels in | §3 |
| [`registration.json`](0.7/registration.json) | `arc/registration` | §5 |
| [`card.json`](0.7/card.json) | `arc/card`, the extended Agent Card, including trial terms | §6.1, §6.5 |
| [`policy.json`](0.7/policy.json) | `arc/policy`, the trust policy or discovery query | §7.2, §7.5 |
| [`snapshot.json`](0.7/snapshot.json) | `arc/snapshot`, the registry-signed discovery response | §7.5 |
| [`rfq.json`](0.7/rfq.json) | `arc/rfq` | §8.1 |
| [`quote.json`](0.7/quote.json) | `arc/quote` | §8.1 |
| [`offer.json`](0.7/offer.json) | `arc/offer`, including counter-offers via `prior_ref` | §8.2, §8.3 |
| [`acceptance.json`](0.7/acceptance.json) | `arc/acceptance` | §8.3 |
| [`engagement.json`](0.7/engagement.json) | `arc/engagement`: spot, term or standing | §8.3 |
| [`receipt.json`](0.7/receipt.json) | `arc/receipt` | §9 |
| [`attestation.json`](0.7/attestation.json) | `arc/attestation`, both directions | §11.1, §11.2 |
| [`value_model.json`](0.7/value_model.json) | `arc/value_model` | §11.4 |
| [`outcome.json`](0.7/outcome.json) | `arc/outcome` | §11.4 |
| [`test_report.json`](0.7/test_report.json) | `arc/test_report`: pass, fail or conditional pass, with corrections | §7.4 |
| [`dispute.json`](0.7/dispute.json) | `arc/dispute` | §12 |
| [`verdict.json`](0.7/verdict.json) | `arc/verdict` | §12 |
| [`ledger_record.json`](0.7/ledger_record.json) | One record of the `GET /v1/ledger` export | §10.3 |

## Conventions

- An envelope's `type` selects the body schema: `arc/value_model` → `value_model.json`.
- Unknown fields are allowed everywhere except where `additionalProperties` is `false` (the envelope and `arc/acceptance`). This is how minor versions stay compatible.
- Extensions use the `x_` prefix. They are covered by signatures but not validated.
- Each schema's `$id` is its raw URL in this repo, so `$ref`s resolve with any standard validator.
- Versioned schema URLs never change. [`0.5/`](0.5/) stays exactly as published, so objects made under arc/0.5 keep validating against the schemas they were born under (SPEC.md §18.1). There is no separate 0.6 set: its changes ship in 0.7.
- Every valid arc/0.5 example also validates under 0.7. The frozen copies live in [`test-vectors/compat/`](../test-vectors/compat/).
