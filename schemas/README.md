# Schemas · arc/0.5

JSON Schema draft 2020-12. One schema per object body, plus the envelope and the shared definitions. They constrain structure and syntax only. Rules that span objects (one attestation per receipt per direction, monotonic counter-offers, value floors, buyer-requirements screening) are normative in [SPEC.md](../SPEC.md) and enforced by the registry.

| Schema | Validates | Spec |
|---|---|---|
| [`common.json`](0.5/common.json) | Shared definitions: ARC-AID, DID, hash, money, pricing, SLO, rubric, payout table, allocation | §2 |
| [`envelope.json`](0.5/envelope.json) | The envelope every object travels in | §3 |
| [`registration.json`](0.5/registration.json) | `arc/registration` | §5 |
| [`card.json`](0.5/card.json) | `arc/card`, the extended Agent Card | §6 |
| [`policy.json`](0.5/policy.json) | `arc/policy`, the trust policy or discovery query | §7.2, §7.4 |
| [`snapshot.json`](0.5/snapshot.json) | `arc/snapshot`, the registry-signed discovery response | §7.4 |
| [`rfq.json`](0.5/rfq.json) | `arc/rfq` | §8.1 |
| [`quote.json`](0.5/quote.json) | `arc/quote` | §8.1 |
| [`offer.json`](0.5/offer.json) | `arc/offer`, including counter-offers via `prior_ref` | §8.2, §8.3 |
| [`acceptance.json`](0.5/acceptance.json) | `arc/acceptance` | §8.3 |
| [`engagement.json`](0.5/engagement.json) | `arc/engagement`: spot, term or standing | §8.3 |
| [`receipt.json`](0.5/receipt.json) | `arc/receipt` | §9 |
| [`attestation.json`](0.5/attestation.json) | `arc/attestation`, both directions | §11.1, §11.2 |
| [`value_model.json`](0.5/value_model.json) | `arc/value_model` | §11.4 |
| [`outcome.json`](0.5/outcome.json) | `arc/outcome` | §11.4 |
| [`dispute.json`](0.5/dispute.json) | `arc/dispute` | §12 |
| [`verdict.json`](0.5/verdict.json) | `arc/verdict` | §12 |
| [`ledger_record.json`](0.5/ledger_record.json) | One record of the `GET /v1/ledger` export | §10.3 |

## Conventions

- An envelope's `type` selects the body schema: `arc/value_model` → `value_model.json`.
- Unknown fields are allowed everywhere except where `additionalProperties` is `false` (the envelope and `arc/acceptance`). This is how minor versions stay compatible.
- Extensions use the `x_` prefix. They are covered by signatures but not validated.
- Each schema's `$id` is its raw URL in this repo, so `$ref`s resolve with any standard validator.
