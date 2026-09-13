# Status

## Current state

- Project posture: `CANON-SHADOW`
- Governance effect: `ADVISORY_ONLY`
- Runtime implementation: `NOT_STARTED`
- Foundation spec: `IN_PROGRESS`
- N0 embedding/representation comparison: `NOT_IMPLEMENTED`
- N1 hidden-state capture: `NOT_IMPLEMENTED`
- N2 sparse-feature/probe/causal lab: `NOT_IMPLEMENTED`
- N3 semantic invariance: `SPECIFIED / NOT_EXECUTED`
- N4 cross-model alignment: `SPECIFIED AT SYSTEM LEVEL / NOT_EXECUTED`
- N5 latent communication: `BLOCKED`

## Current blockers

1. Reference runtime/model selection has not been settled.
2. No fixture corpus has been frozen for EXP-001.
3. Hyperlexical transform contract is specified conceptually but not implemented.
4. No independent replication evidence exists.
5. No FIELD authorization exists.

## Next executable slice

`SLICE-001 — Reproducible representation capture`

Scope:
- Python package skeleton;
- open-weight Hugging Face-compatible adapter;
- experiment manifest contract;
- deterministic fixture runner;
- hidden-state/embedding capture;
- observation writer;
- basic cosine/CKA comparison;
- schema and replay tests.

Exit gate: `AC-N0` plus the capture portion of `AC-N1`.

## Promotion posture

No latent semantic claim is currently promoted. `EXP-001` results, once executed, remain CANON-SHADOW until independently replicated and reviewed.
