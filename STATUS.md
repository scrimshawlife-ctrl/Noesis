# Status

## Current state

- Project posture: `CANON-SHADOW`
- Governance effect: `ADVISORY_ONLY`
- Runtime implementation: `NOT_STARTED`
- Foundation spec: `COMPLETE`
- Canonical requirements/journeys/workflows/state machines/contracts/data/security/acceptance/tasks/verification: `COMPLETE`
- N0 embedding/representation comparison: `SPECIFIED / NOT_IMPLEMENTED`
- N1 hidden-state capture: `SPECIFIED / NOT_IMPLEMENTED`
- N2 sparse-feature/probe/causal lab: `SPECIFIED / NOT_IMPLEMENTED`
- N3 semantic invariance: `FULLY_SPECIFIED / NOT_EXECUTED`
- N4 cross-model alignment: `FULLY_SPECIFIED / NOT_EXECUTED`
- N5 latent communication: `FULLY_SPECIFIED / BLOCKED`

## Specification settlement

The specification package now includes:
- doctrine/constitution;
- domain boundaries and architecture;
- complete FR/NFR catalog;
- actor journeys;
- deterministic workflow catalog;
- legal state machines;
- canonical contract semantics and JSON Schemas;
- data model and artifact identity rules;
- threat model, privacy, authority, and governance;
- acceptance gates AC-G0, AC-N0..N5, AC-R1/R2, AC-S1;
- implementation task graph;
- verification plan;
- experiment specifications for EXP-001 and gated EXP-002;
- end-to-end traceability;
- CI spec validation.

No runtime capability is inferred from specification completeness.

## Current blockers to runtime execution

1. Reference model family for SLICE-001 has not been frozen.
2. EXP-001 fixture corpus has not been generated/frozen.
3. Hyperlexical transform boundary is specified but not implemented.
4. No capture/metric runtime exists yet.
5. No independent replication evidence exists.
6. No FIELD authorization exists.
7. N5 remains blocked until AC-N4 acceptance plus explicit operator authorization.

## Next executable slice

`SLICE-001 — Reproducible Representation Capture`

Scope:
- Python package skeleton;
- typed core domain/contracts;
- runtime adapter protocol;
- open-weight Hugging Face-compatible reference adapter;
- immutable ExperimentManifest execution;
- deterministic fixture runner;
- hidden-state/embedding capture;
- content-addressed artifact writer;
- Observation and FailureRecord output;
- cosine/Euclidean/CKA comparison foundation;
- null-control utilities;
- schema, replay, numeric-tolerance, and failure-path tests.

Traceability:
- Requirements: FR-001–005, FR-020–025, FR-060–074; relevant NFRs.
- Journeys: J-005, partial J-001.
- Workflows: WF-001, WF-002, WF-003.
- State machines: SM-001, SM-002, SM-006.
- Contracts: C-001, C-002, C-003, C-008.
- Tasks: T-010, T-020, T-021, T-030, T-040.
- Verification: V-001–V-005, V-011/V-012 where applicable.

Exit gate: `AC-N0` plus the capture portion of `AC-N1`.

## Promotion posture

No latent semantic claim is currently promoted. All future semantic, mechanistic, alignment, or communication findings remain CANON-SHADOW until their declared gate and replication requirements are satisfied.
