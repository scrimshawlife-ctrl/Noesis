# Status

## Current state

- Project posture: `CANON-SHADOW`
- Governance effect: `ADVISORY_ONLY`
- Foundation spec: `COMPLETE`
- Canonical requirements/journeys/workflows/state machines/contracts/data/security/acceptance/tasks/verification: `COMPLETE`
- Runtime implementation: `SLICE-001 IMPLEMENTED / STACKED PR #2`
- N0 embedding/representation comparison: `IMPLEMENTED / CI-VERIFIED / ACCEPTANCE REVIEW PENDING`
- N1 hidden-state capture: `IMPLEMENTED / REAL-MODEL ACCEPTANCE NOT_EXECUTED`
- N2 sparse-feature/probe/causal lab: `SPECIFIED / NOT_IMPLEMENTED`
- N3 semantic invariance: `FULLY_SPECIFIED / NOT_EXECUTED`
- N4 cross-model alignment: `FULLY_SPECIFIED / NOT_EXECUTED`
- N5 latent communication: `FULLY_SPECIFIED / BLOCKED`

## Specification settlement

The specification package is complete through doctrine, requirements, journeys, workflows, state machines, contracts, data, security/governance, acceptance, tasks, verification, experiments, and traceability.

Specification completeness does not imply scientific capability.

## SLICE-001 implementation evidence

Implemented on `runtime/slice-001-representation-capture`:
- Python package skeleton and typed capture-domain objects;
- adapter protocol with explicit capability declaration;
- deterministic fake adapter restricted to CI/runtime semantics;
- optional Hugging Face reference adapter for embedding/hidden-state capture;
- immutable manifest validation and execution;
- content-addressed SHA-256 vector/JSON artifact store;
- Observation output with `OBSERVED` provenance;
- explicit FailureRecord persistence for missing fixtures/capture failures;
- cosine, Euclidean, linear CKA, neighborhood overlap;
- permutation-null and bootstrap uncertainty utilities;
- deterministic replay and schema tests;
- fail-closed numeric and metric tests;
- runtime GitHub Actions validation.

The fake adapter is not scientific model evidence and cannot settle a latent claim.

## Remaining acceptance blockers

1. Freeze an open-weight reference model family and exact revision for controlled N1 acceptance.
2. Execute embedding and hidden-state capture twice against that exact model/revision and compare artifact/metric evidence under declared numeric tolerance.
3. Record runtime/device/dependency fingerprint for that execution.
4. Complete AC-N0/AC-N1 review from the resulting evidence packet.
5. EXP-001 fixture corpus remains unfrozen.
6. Hyperlexical transform boundary remains unimplemented.
7. No independent replication evidence exists.
8. No FIELD authorization exists.
9. N5 remains blocked until AC-N4 acceptance plus explicit operator authorization.

## Next executable slice

`SLICE-001A — Pinned Real-Model Acceptance`

Scope:
- choose a small open-weight reference model suitable for repeatable CI/lab execution;
- pin immutable model and tokenizer revisions;
- capture embedding and at least two hidden-state sites;
- execute repeated captures with fixed fixture/seed/environment;
- record Observation and FailureRecord evidence;
- compute replay cosine/Euclidean and applicable matrix metrics;
- verify artifact integrity and environment fingerprint;
- assemble AC-N0/AC-N1 evidence packet.

Exit gate: `AC-N0 ACCEPTED` and `AC-N1 ACCEPTED` or explicit `REJECTED/NOT_COMPUTABLE` with preserved evidence.

## Promotion posture

No latent semantic claim is currently promoted. All semantic, mechanistic, alignment, or communication findings remain CANON-SHADOW until their declared evidence and replication gates are satisfied.
