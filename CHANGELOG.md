# Changelog

All versions are drafts until arc/1.0. Minor versions only add: optional fields, endpoints, object types and open-enum values. Anything that breaks compatibility needs a new major version. See [SPEC.md §18](SPEC.md#18-versioning-and-backward-compatibility).

## arc/0.7 · 29 October 2026

Trials and test reports.

- Trial (freemium) terms: an optional `trial` block on a card's capabilities (duration, task or unit caps, discount, buyer eligibility, `per_buyer: once`). Buyers avail one with `trial: true` on an offer (§6.5).
- One trial per buyer AID per capability, ever. Trial engagements end as CONVERTED or TRIAL_EXPIRED.
- `trial` marker on receipts and ledger records, so trial usage shows as itemized shadow cost.
- Trial attestations are weighted at the minimum paid price and capped at 20% of a score's sample weight. Trials are excluded from ROAI (§11.5).
- `arc/test_report` object: closed tri-state verdict (pass, fail, conditional_pass), per-case results and machine-actionable corrections with retest deadlines (§7.4).
- Probe status: unverified, verified, conditional or failed. `probe_status` in snapshots and `include_conditional` on policies.
- Retests are scoped to failed cases and rate-limited (default 3 per P7D per capability).
- New endpoints: `GET /v1/trials`, `POST /v1/test-reports`, `GET /v1/test-reports/{id}`, `POST /v1/cards/{hash}/retest`.
- Error codes ARC-8001 to ARC-8003.
- Trust policy and snapshot moved from §7.4 to §7.5.
- Schemas: `schemas/0.7/` adds `test_report.json`; the 0.6 changes below ship in the same bundle. `schemas/0.5/` stays unchanged at its URL.

## arc/0.6

Versioning and backward compatibility (§18 rewritten). Released as part of the arc/0.7 bundle; there is no separate 0.6 schema set.

- Four version carriers, versioned independently: the wire version (`arc`, major.minor, no patch), immutable versioned schema URLs, the `/v1` API path, and the capability taxonomy.
- Compatibility contract: what a minor release may and must not change. Any change to canonicalization, hashing or signatures is a major version.
- Open enums with normative receiver fallbacks. An unknown pricing model is rejected with ARC-1004.
- `arc_versions` declared at registration. A transaction runs at the lower of the two parties' versions, with downgrade protection.
- Engagements are pinned to the version their acceptance was signed under. Term and standing engagements migrate only at a renewal gate or by bilateral re-signing.
- Deprecation lifecycle: sunset at least P180D after notice, majors N and N−1 served in parallel, ARC-1005 for a removed version.
- Verification continuity (receipts verify forever) and reputation continuity (history carries across versions).
- `/.well-known/arc` lists versions supported and deprecations. Error codes ARC-1004 and ARC-1005.
- Compatibility matrix: every valid vector of the previous version must validate under the current schemas (`test-vectors/compat/`).

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
