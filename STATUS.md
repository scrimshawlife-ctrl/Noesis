# Status

## Current state

- Project posture: `CANON-SHADOW`
- Governance effect: `ADVISORY_ONLY`
- Foundation spec: `COMPLETE`
- Canonical requirements/journeys/workflows/state machines/contracts/data/security/acceptance/tasks/verification: `COMPLETE`
- Runtime implementation: `SLICE-001 + SLICE-002A + SLICE-003 + SLICE-004 + SLICE-005 + SLICE-006 + SLICE-007 + SLICE-008 + SLICE-009 + SLICE-010 + SLICE-011 + SLICE-012 + SLICE-013 + SLICE-014 + SLICE-015 + SLICE-016 + SLICE-017 + SLICE-018 + SLICE-019 + SLICE-020 + SLICE-021 + SLICE-022 + SLICE-023 + SLICE-024 + SLICE-025 + SLICE-026 + SLICE-027 IMPLEMENTED`
- Hyperlex integration: `ADAPTER + PREREGISTRATION BOUNDARY IMPLEMENTED / TRAINED MODEL BINDING PENDING`
- N0 embedding/representation comparison: `AC-N0 ACCEPTED / PINNED REAL-MODEL EVIDENCE`
- N1 hidden-state capture: `AC-N1 ACCEPTED / PINNED REAL-MODEL EVIDENCE`
- N2 sparse-feature/probe/causal lab: `SLICE-004/005/006 IMPLEMENTED / AC-N2 NOT ACCEPTED`
- N3 semantic invariance: `FULLY_SPECIFIED / PREREGISTRATION TOOLING IMPLEMENTED / NOT_EXECUTED`
- EXP-001-GEO curvature-aware profile: `SLICE-009 RUNTIME IMPLEMENTED / NOT_EXECUTED / AC-N3-GEO NOT ACCEPTED`
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

### SLICE-008 — Independent replication harness
Implemented:
- `replicate_settlement` compares original/replica metric envelopes against a registered tolerance;
- classifications: `REPLICATED`, `PARTIAL`, `FAILED_REPLICATION`, `NOT_COMPUTABLE`;
- original settlement is not mutated;
- full `REPLICATED` requires an independent operator, a new control, resolvable artifacts, and an in-tolerance envelope;
- replica settlement is a new `C-006` record; `ELIGIBLE_FOR_REVIEW` only on `REPLICATED`;
- environment deltas are disclosed on the report.

AC-R1/AC-R2 are not accepted: this is the harness, not an independent scientific replication of N0/N1 or EXP-001.

### SLICE-009 — Geometry profile runtime
Implemented:
- `GeometryProfile` validation with mandatory Euclidean baseline;
- geodesic-distortion evaluation for Euclidean and Poincaré hyperbolic candidates;
- confirmation blocked until selection is frozen;
- out-of-ball hyperbolic points emit `NOT_COMPUTABLE`;
- selection uses the selection split only and applies a complexity penalty;
- geometric results never populate semantic-truth or universal-geometry fields.

AC-N3-GEO is not accepted: no operator-approved relational corpus, and no geometry is privileged in core.

### SLICE-010 — Audit and security controls
Implemented:
- secret-pattern scan over fixture text;
- `PROHIBITED` classification rejected;
- `SENSITIVE` requires retention and access scope;
- FIELD/N5 require explicit operator authorization;
- artifact substitution detected via content-hash mismatch;
- synthetic incident records plus supersession without deleting the original.

AC-S1 is not a production authorization. FIELD remains blocked without an operator receipt.

### SLICE-011 — FailureRecord interchange and extra geometry families
Implemented:
- schema-valid `C-008` FailureRecord; executor validates before persist;
- spherical great-circle geodesic distortion;
- product-manifold geodesic as hypot of component Euclidean distances.

Topological candidates remain `NOT_COMPUTABLE` until a filtration is registered.

### SLICE-012 — Topological filtration, shuffled nulls, product ablation
Implemented:
- graph-path topological geodesic under `fit_config.max_scale`;
- missing filtration or disconnected graphs emit `NOT_COMPUTABLE`;
- shuffled-relation null raises Euclidean distortion;
- product-manifold component ablations are required and increase distortion.

### SLICE-013 — Neighborhood and rank preservation metrics
Implemented:
- `knn_retention` vs registered relation neighborhoods;
- `rank_order_preservation` (Spearman of measured vs registered distances);
- invalid k / degenerate ranks fail closed as `NOT_COMPUTABLE`.

### SLICE-014 — Random-pair nulls and bootstrap uncertainty
Implemented:
- random-pair null raises geodesic distortion versus registered relations;
- bootstrap mean/lo/hi interval on pairwise geodesic errors;
- fewer than two relations fail closed as `NOT_COMPUTABLE`.

### SLICE-015 — Spherical diagnostics and compute-aware selection
Implemented:
- spherical renormalization and antipodal-pair diagnostics;
- `compute_cost` on geodesic evaluations;
- selection applies an optional `compute_penalty`.

### SLICE-016 — ProjectionLoss
Implemented:
- PCA/truncate projection of a representation to a lower dimension;
- geodesic distortion of registered relations after compression;
- invalid target dimension fails closed;
- no intent, legitimacy, or social-cause fields.

This operationalizes Flatland only as `ProjectionLoss`. It does not establish the full Flatland Effect.

### SLICE-017 — GeometricRupture label
Implemented:
- preregistered distortion threshold labels a metric as `RUPTURED`, `INTACT`, or `NOT_COMPUTABLE`;
- the label is experiment-owned (`canonical=false`);
- it is not a claim of semantic destruction.

### SLICE-018 — Held-out relation prediction
Implemented:
- AUC of geodesic ranking for held-out true pairs versus non-edges;
- missing positives or negatives fail closed as `NOT_COMPUTABLE`;
- ranking is not treated as semantic truth.

### SLICE-019 — Capture-path classification gate
Implemented:
- `ManifestExecutor` classifies fixtures before capture;
- secret-like text and `PROHIBITED` class become `FailureRecord`s, not observations;
- default classification remains `PUBLIC_REPRODUCIBLE`.

### SLICE-020 — Verified analysis load
Implemented:
- `ContentAddressedStore.load_vector` verifies hash and shape before returning bytes;
- `cosine_of_observations` refuses substituted artifacts;
- analysis cannot silently measure a mutated tensor.

### SLICE-021 — Environment fingerprints
Implemented:
- SHA-256 fingerprint of capture environment (excluding the fingerprint field itself);
- material dependency changes require a new run identity;
- observations record the fingerprint.

### SLICE-022 — FIELD/N5 capture authorization
Implemented:
- `ManifestExecutor` reads `environment_requirements.execution_scope` (default `LAB`);
- FIELD/N5 require explicit operator authorization before any capture cell runs.

This does not authorize N5 science. It only enforces the gate.

### SLICE-023 — Replication environment fingerprints
Implemented:
- optional original/replica environment maps on `replicate_settlement`;
- `require_equivalent_environment` blocks full `REPLICATED` when fingerprints differ (FR-073);
- fingerprint deltas are disclosed on the report.

### SLICE-024 — Verified Euclidean and CKA
Implemented: `euclidean_of_observations` and `cka_of_observation_sets` load tensors only after hash checks.

### SLICE-025 — Replay envelope
Implemented: `replay_envelope` checks cosine, Euclidean, and artifact-hash equality against manifest thresholds.

### SLICE-026 — Manifest/fixture classification consistency
Implemented: a fixture whose `data_classification` differs from the manifest becomes a `FailureRecord`.

### SLICE-027 — Failure environment fingerprint
Implemented: capture failures record a Python environment fingerprint.

## Remaining blockers

1. Freeze an operator-approved EXP-001 source corpus; Noesis does not invent that semantic corpus.
2. Freeze the initial EXP-001 transform/control catalog.
3. Keep EXP-001-GEO inactive until its relational corpus/profile receive operator approval.
4. Bind the trained Hyperlex model to the callable or HTTP adapter when its inference surface stabilizes.
5. No independent scientific replication evidence exists (harness only).
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

### D — Replication and gates
T-110 harness exists. AC-R2 still requires an independent operator rerun with new controls on real evidence. AC-N2/N3/N4 remain unaccepted.

## Notion parity

Repo is source of truth. Paste-ready hub card: `docs/NOTION-PARITY.md`.

Observed 2026-09-16: this host could not reach `api.notion.com` (TLS/connect timeout), so live Hub writeback was **not** performed. Until an operator pastes that card, Notion may lag `main` (SLICE-027 / PR #29).

## Promotion posture

No latent semantic claim is currently promoted. All semantic, mechanistic, alignment, or communication findings remain CANON-SHADOW until their declared evidence and replication gates are satisfied.
