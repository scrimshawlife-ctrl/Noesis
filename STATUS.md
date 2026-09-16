# Status

## Current state

- Project posture: `CANON-SHADOW`
- Governance effect: `ADVISORY_ONLY`
- Foundation spec: `COMPLETE`
- Canonical requirements/journeys/workflows/state machines/contracts/data/security/acceptance/tasks/verification: `COMPLETE`
- Runtime implementation: `SLICE-001 + SLICE-002A + SLICE-003 + SLICE-004 + SLICE-005 + SLICE-006 + SLICE-007 IMPLEMENTED`
- Hyperlex integration: `ADAPTER + PREREGISTRATION BOUNDARY IMPLEMENTED / TRAINED MODEL BINDING PENDING`
- N0 embedding/representation comparison: `AC-N0 ACCEPTED / PINNED REAL-MODEL EVIDENCE`
- N1 hidden-state capture: `AC-N1 ACCEPTED / PINNED REAL-MODEL EVIDENCE`
- N2 sparse-feature/probe/causal lab: `SLICE-004/005/006 IMPLEMENTED / AC-N2 NOT ACCEPTED`
- N3 semantic invariance: `FULLY_SPECIFIED / PREREGISTRATION TOOLING IMPLEMENTED / NOT_EXECUTED`
- EXP-001-GEO curvature-aware profile: `FULLY_SPECIFIED / NOT_IMPLEMENTED / NOT_EXECUTED`
- N4 cross-model alignment: `SLICE-007 LINEAR MAP IMPLEMENTED / AC-N4 NOT ACCEPTED`
- N5 latent communication: `FULLY_SPECIFIED / BLOCKED`

## Implemented evidence surfaces

### SLICE-001 — Representation capture
- typed capture-domain objects and adapter capabilities;
- deterministic test adapter and optional Hugging Face reference adapter;
- immutable manifest validation/execution;
- content-addressed SHA-256 artifacts;
- Observation + FailureRecord semantics;
- cosine, Euclidean, linear CKA, neighborhood overlap;
- permutation-null and bootstrap uncertainty utilities;
- deterministic replay, contract, numeric, artifact-integrity, and failure tests.

The fake adapter is test infrastructure only and is not scientific latent evidence.

### SLICE-001A — Pinned real-model acceptance readiness
Implemented:
- `N01AcceptanceConfig` and executable AC-N0/AC-N1 acceptance harness;
- single-capture persistence so compared tensors are the exact tensors recorded as observations;
- `N01AcceptanceEvidence` contract;
- pinned-revision CLI that rejects obvious floating revisions;
- manual GitHub Actions workflow for open-weight Hugging Face acceptance runs;
- uploaded acceptance artifact packet on manual execution.

Executed in [workflow run 34826673897](https://github.com/scrimshawlife-ctrl/Noesis/actions/runs/34826673897) against the pinned model/tokenizer revision. AC-N0 and AC-N1 are accepted for the bounded reference run. See `specs/acceptance/N01-ACCEPTANCE-SETTLEMENT-2026-09-14.md`. This does not establish semantic invariance, mechanistic interpretation, or layer distinctness.

### SLICE-002A — Hyperlex adapter/preregistration readiness
Implemented without binding to the still-training Hyperlex model:
- `HyperlexTransformRequest` / `HyperlexTransformResult` contracts;
- callable/in-process, HTTP, and deterministic test adapters;
- transform provenance/hash validation and immutable fixture materialization;
- deterministic request IDs and transform/control classes;
- replayable transform bundles;
- `EXP001SourceCorpus` contract with discovery/confirmation/control partitions;
- `EXP001TransformCatalog` contract for operator-owned transform/control hypotheses;
- deterministic EXP-001 preregistration compiler from frozen corpus + transform catalog.

Invariant: Hyperlex may declare intended semantic invariants; Hyperlex may not assert latent truth labels or settle Noesis evidence.

### SLICE-003 — Settlement engine
Implemented:
- `settle_evidence` emits schema-valid `C-006` settlements from classified evidence refs;
- missing required evidence yields `NOT_COMPUTABLE` rather than fabricated completion;
- payload/hash mismatch fails closed (cannot cite nonexistent evidence);
- contradicting/negative evidence remains addressable on the issued settlement;
- causal claims without intervention evidence are bounded below `OBSERVED`;
- `governance_effect` is always `ADVISORY_ONLY`;
- `ELIGIBLE_FOR_REVIEW` requires independent replication evidence (`FR-065`);
- `supersede_settlement` emits schema-valid `C-009` without mutating the original settlement.

This does not execute EXP-001, accept AC-N2/N3/N4, or authorize promotion beyond CANON-SHADOW.

### SLICE-004 — Sparse dictionary lab and control evaluation
Implemented:
- tied SVD+ReLU dictionary fit with versioned identity and source-activation hash;
- reconstruction R², mean L0 sparsity, and dead-feature rate as schema-valid `C-003` metrics;
- seed-reproducible fit and run-to-run decoder consistency (optional row bootstrap);
- feature descriptions as `FeatureHypothesis` only (`canonical=false`); they are not dictionary labels;
- lexical-trigger / semantic-positive / negative control evaluation that can `WEAKEN` or `REJECT` a candidate;
- weakened candidates settle below `OBSERVED`.

### SLICE-005 — Probe lab
Implemented:
- ridge-linear probe with declared regularization, train/held-out partition hashes, and seed;
- held-out accuracy as schema-valid `C-003`;
- majority and shuffled-label baselines;
- leakage detector for overlapping IDs and identical activation rows (positive test included);
- leaked fits fail closed;
- probe accuracy alone cannot settle an `OBSERVED` causal claim (`FR-035`).

### SLICE-006 — Intervention lab
Implemented:
- `run_intervention` emits schema-valid `C-004` records with baseline → control → intervention order;
- synthetic STEER on the deterministic fake adapter when `causal_intervention=True`;
- null (magnitude 0) effect near zero; positive steer moves the declared outcome in the expected direction;
- adapters without causal access record `NOT_COMPUTABLE` with an explicit unavailable limitation (no fabricated effect);
- failed interventions remain visible as `FAILED`;
- null effects are preserved on the record;
- causal settlements citing intervention evidence remain `INFERRED`, not `OBSERVED` mechanism.

This does not accept AC-N2: no independent replication, no real-model causal access, and the fake adapter is not scientific evidence.

### SLICE-007 — Alignment lab
Implemented:
- least-squares map fit on train only;
- disjoint train/validation/test hashes with leakage fail-closed;
- held-out CKA, shuffled-pairing null, and distribution-shift metrics as schema-valid `C-003`;
- `C-005` AlignmentMap with `SUPPORTED` / `WEAK` / `REJECTED`;
- geometric CKA never writes a semantic-equivalence field.

AC-N4 is not accepted: this is a synthetic linear map, not a cross-model checkpoint study.

## Remaining blockers

1. Freeze an operator-approved EXP-001 source corpus; Noesis does not invent that semantic corpus.
2. Freeze the initial EXP-001 transform/control catalog.
3. Keep EXP-001-GEO inactive until its relational corpus/profile receive operator approval.
4. Bind the trained Hyperlex model to the callable or HTTP adapter when its inference surface stabilizes.
5. No independent replication evidence exists.
6. No FIELD authorization exists.
7. N5 remains blocked until AC-N4 acceptance plus explicit operator authorization.

The EXP-001 compiler now requires a schema-valid `EXP001FreezeReceipt` that binds an identified operator approval to the exact corpus and catalog canonical hashes. A draft review packet exists at `specs/exp001/INPUT-FREEZE-CANDIDATE.md`; it contains no invented corpus fixtures.

## Next executable actions

### A — Preserve SLICE-001A settlement
Keep the accepted reference run, evidence JSON, archive/evidence hashes, limitations, and source workflow linked. Any materially different model, revision, fixture, site, environment, or tolerance requires a new acceptance identity.

### B — Freeze EXP-001 inputs
Create operator-approved `EXP001SourceCorpus` and `EXP001TransformCatalog`, then run `scripts/compile_exp001_plan.py`. This may proceed while Hyperlex training continues.

### C — Bind Hyperlex when ready
Attach the trained model behind `CallableHyperlexAdapter` or `HttpHyperlexAdapter`; no Noesis evidence semantics should change.

### D — AC-N2 packet
T-060/T-061/T-062/T-070 runtime paths exist. AC-N2 is still not accepted: fake-adapter interventions are not scientific evidence, and AC-R2 replication is absent.

## Promotion posture

No latent semantic claim is currently promoted. All semantic, mechanistic, alignment, or communication findings remain CANON-SHADOW until their declared evidence and replication gates are satisfied.
