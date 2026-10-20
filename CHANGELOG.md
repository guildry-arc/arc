# Changelog

All versions are drafts until arc/1.0. Minor versions add optional fields only; see [SPEC.md §18](SPEC.md#18-versioning-and-extensibility).

## arc/0.5 · 25 August 2026

Finance and spend observability.

- `allocation` object on RFQs, offers and receipts. Receipts inherit the offer's allocation verbatim and immutably.
- Five ledger states: committed, settled, held, refunded, auto_settled.
- `GET /v1/ledger` export and the `ledger_record` schema.
- Variance provisions: quoted versus paid, explicit risk-premium components.
- ROAI band in snapshots.

## arc/0.4

Value attribution.

- `arc/value_model` and `arc/outcome` objects.
- Receipt-DAG attribution rules: last_touch, linear, weighted.
- ROAI computation with three disclosure tiers and anonymized bands; per-capability benchmarks.
- `value_share` pricing with a mandatory audit clause and computed value floor.
- `value_audit` dispute kind, related endpoints and error codes ARC-7001 to ARC-7003.

## arc/0.3

Capability discovery.

- Capability taxonomy with mandatory node mapping; `taxonomy_node` and `tags` on capabilities.
- Intent-mode discovery with schema-compatibility gating.
- Capability probe verification with re-probe cadence; probe fields in snapshots.
- Taxonomy browse endpoints and related error codes.

## arc/0.2

Identity, negotiation and bilateral reputation.

- ARC-AID unique identifiers and explicit autonomous-registration guarantees.
- RFQ and quote negotiation with monotonic-concession rules.
- Bilateral attestations with buyer conduct scoring.
- Seller-side `buyer_requirements` and risk-premium pricing.

## arc/0.1

First draft: envelope, registration, card, policy, snapshot, offer, acceptance, engagement, receipt, dispute and verdict.
