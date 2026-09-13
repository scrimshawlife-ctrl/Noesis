# NOESIS-SYSTEM-SPEC

Status: `CANON-SHADOW`
Version: `0.1.0`

## 1. Doctrine

Noesis is an experimental latent-representation evidence system. It measures and tests model representations without assuming that those representations form a universal language or faithful transcript of internal reasoning.

### Invariants

- Evidence precedes interpretation.
- Correlation is not causal evidence.
- Natural-language feature descriptions are annotations, not ground truth.
- Missing evidence yields `NOT_COMPUTABLE`.
- No experiment may silently mutate Abraxas governance or production behavior.
- Negative results are first-class evidence.

## 2. Domain model

### Entities

- `ModelIdentity`: provider/source, family, revision, weights hash where available, tokenizer revision.
- `RepresentationSite`: model component and layer/site from which a vector/tensor is captured.
- `InputFixture`: immutable experiment input and metadata.
- `Transform`: controlled modification of an input with declared semantic intent.
- `Observation`: immutable captured representation plus provenance.
- `FeatureDictionary`: versioned SAE/dictionary decomposition artifact.
- `Probe`: hypothesis-bound classifier/regressor/evaluator.
- `Intervention`: patch, ablation, steering, injection, or equivalent causal manipulation.
- `AlignmentMap`: fitted transform between representation spaces.
- `MetricResult`: deterministic result from a declared metric.
- `EvidenceBundle`: content-addressed set of observations/results.
- `Settlement`: durable conclusion and provenance label.

### Relationships

`InputFixture -> Transform* -> Observation* -> MetricResult* -> EvidenceBundle -> Settlement`

Optional branches:

`Observation -> FeatureDictionary -> candidate Feature -> Probe/Intervention`

`Observation(A), Observation(B) -> AlignmentMap -> aligned MetricResult`

## 3. Requirements

### Functional

- `FR-001` Capture embeddings and hidden-state representations from supported open-weight runtimes.
- `FR-002` Record exact model/tokenizer/revision/site metadata for every capture.
- `FR-003` Apply versioned controlled transformations from Hyperlexical or deterministic fixtures.
- `FR-004` Compare representations using experiment-declared metrics.
- `FR-005` Train/load versioned sparse feature dictionaries and report reconstruction, sparsity, dead-feature, and consistency metrics.
- `FR-006` Run pre-registered probes with baselines and distribution-shift controls.
- `FR-007` Run causal interventions where technically supported.
- `FR-008` Fit and evaluate explicit cross-layer/cross-model alignment maps.
- `FR-009` Preserve raw evidence references, negative results, and contradictions.
- `FR-010` Produce schema-valid settlements with provenance and promotion recommendation.
- `FR-011` Expose stable contracts to Hyperlexical and Abraxas without creating hidden coupling.
- `FR-012` Support deterministic replay of an experiment from its manifest where dependencies remain available.
- `FR-013` Keep latent agent communication disabled until its entry gate is satisfied.

### Non-functional

- `NFR-001` Reproducibility: seed, environment, hashes, revision IDs, metrics, and configs recorded.
- `NFR-002` Auditability: every settlement references evidence identifiers/hashes.
- `NFR-003` Modularity: adapters and experiment methods can change without changing settlement semantics.
- `NFR-004` Fail-closed semantics: malformed/missing evidence cannot be promoted.
- `NFR-005` Data minimization: raw sensitive input is not persisted unless explicitly required and authorized.
- `NFR-006` Determinism: deterministic methods must reproduce within declared numeric tolerance.
- `NFR-007` Portability: initial implementation should target Python and open-weight transformer runtimes without requiring a single vendor.

## 4. Journeys

### `J-001` Researcher tests semantic invariance
A researcher defines concepts and surface transformations, captures latent representations, compares invariance, falsifies candidate features, and obtains a settlement.

### `J-002` Researcher evaluates a candidate feature
A researcher discovers an SAE/probe feature, tests lexical contamination and distribution shift, performs causal intervention where possible, and settles functional relevance.

### `J-003` Researcher aligns two model spaces
A researcher captures paired fixtures from model A/B, fits an alignment on a training split, evaluates held-out transfer, tests null baselines, and settles whether alignment is supported.

### `J-004` Abraxas consumes a Noesis settlement
Abraxas reads a schema-valid immutable settlement and may treat it as advisory evidence. No automatic canon promotion occurs.

### `J-005` Researcher evaluates latent communication
Only after the N5 entry gate: a researcher configures sender/receiver models, latent encoder/decoder or alignment, baselines, compression budget, information-leak controls, and task metrics.

## 5. Workflows

### `WF-001` Register experiment
Purpose: create an immutable experiment manifest.
Actor: researcher/spec agent.
Trigger: approved research question.
Preconditions: supported model/data rights; explicit hypothesis and metrics.
Inputs: fixtures, transforms, model IDs, sites, metrics, seeds, acceptance thresholds.
Happy path:
1. Validate manifest schema.
2. Hash fixtures/transforms/config.
3. Record environment and model revisions.
4. Freeze acceptance criteria.
5. Assign experiment ID.
Alternate: unsupported capture site -> revise manifest.
Failure: missing required provenance -> terminal `NOT_READY`.
Terminal states: `REGISTERED`, `NOT_READY`.
Side effects: immutable manifest artifact.
Observability: manifest hash and creation record.

### `WF-002` Capture representations
Purpose: create observations.
Preconditions: `REGISTERED`; adapter supports site.
Happy path:
1. Load exact model/tokenizer revision.
2. Execute fixture deterministically where possible.
3. Capture declared sites only.
4. Persist tensor artifact or content-addressed reference.
5. Emit `Observation` metadata.
Failures: OOM, revision unavailable, unsupported hook, non-finite values.
Recovery: record failure; retry only under new run ID if execution conditions change.
Terminal: `CAPTURED`, `CAPTURE_FAILED`.
Invariant: failed runs never masquerade as missing-at-random observations.

### `WF-003` Compare representations
Purpose: compute declared metrics.
Preconditions: compatible observations.
Happy path: normalize as declared -> compute metrics -> bootstrap/permutation/null controls where specified -> persist results.
Failure: dimensional incompatibility or metric preconditions unmet -> `NOT_COMPUTABLE`.
Terminal: `MEASURED`, `NOT_COMPUTABLE`.

### `WF-004` Evaluate sparse feature
Purpose: determine whether an interpretable feature claim survives falsification.
Preconditions: versioned dictionary + candidate feature.
Happy path:
1. Measure reconstruction/sparsity/dead-feature and run-to-run consistency.
2. Identify candidate activation contexts.
3. Run lexical-trigger controls.
4. Run non-reasoning/negative examples designed to activate candidate correlates.
5. Run expected-positive examples under surface perturbation.
6. Run causal intervention where supported.
7. Record contradictions.
8. Settle claim strength.
Promotion rule: semantic/function claim cannot exceed `INFERRED` without causal support and cannot exceed CANON-SHADOW without independent replication.

### `WF-005` Fit cross-model alignment
Purpose: test shared geometry without assuming equivalence.
Happy path:
1. Define paired fixtures and train/validation/test split.
2. Fit map on train only.
3. Select hyperparameters on validation only.
4. Evaluate held-out alignment, neighborhood preservation, and task transfer.
5. Compare against shuffled/null mappings.
6. Test at least one distribution shift.
7. Persist alignment map and limits.
Terminal: `SUPPORTED`, `WEAK`, `REJECTED`, `NOT_COMPUTABLE`.

### `WF-006` Settle evidence
Purpose: produce a durable conclusion.
Inputs: evidence bundle + requested proposition.
Happy path:
1. Validate evidence completeness.
2. Separate observations from interpretation.
3. Assess contradictions and negative controls.
4. Assign provenance label.
5. Record confidence basis and limitations.
6. Emit settlement.
Invariant: no unsupported field may be synthesized.

### `WF-007` Run latent communication experiment
Entry gate: N0–N4 evidence stack accepted; explicit experiment approval; sender/receiver compatibility path defined.
Happy path: establish text baseline -> latent channel -> compression variants -> held-out tasks -> information/latency/task metrics -> adversarial controls -> settlement.
Invariant: latent performance is never interpreted as proof of shared semantics without independent alignment evidence.

## 6. State machines

### Experiment
`DRAFT -> REGISTERED -> RUNNING -> ANALYZED -> SETTLED`
Exceptional: `DRAFT|REGISTERED -> NOT_READY`; `RUNNING -> FAILED`; `ANALYZED -> INCONCLUSIVE`.

### Candidate feature
`DISCOVERED -> CONTROL_TESTED -> FALSIFICATION_TESTED -> CAUSAL_TESTED -> REPLICATED -> PROMOTION_ELIGIBLE`
Any state may transition to `REJECTED` or `INCONCLUSIVE`.

### Capability tier
`N0 -> N1 -> N2 -> N3 -> N4 -> N5`
Advancement requires explicit acceptance evidence; tiers cannot be inferred from code existence.

## 7. Contracts

Canonical JSON schemas live under `contracts/`.

Minimum contracts:
- `Observation`
- `Settlement`
- future: `ExperimentManifest`, `MetricResult`, `AlignmentMap`, `InterventionResult`

Contracts are versioned and additive changes require compatibility review.

## 8. Data model

Metadata storage must support:

- stable UUID/ULID-style IDs;
- SHA-256 or stronger content hashes;
- explicit schema version;
- UTC timestamps;
- model and dataset revision strings;
- artifact URI/reference separated from metadata;
- provenance and environment records.

Large tensors should use content-addressed files or object storage rather than transactional metadata rows.

## 9. Security, privacy, governance

- No secrets, access tokens, private prompts, or proprietary training data in fixtures.
- Capture only declared representation sites.
- Sensitive experiments require explicit data classification, retention, and deletion policy.
- External model artifacts must record license/provenance.
- No latent trace may be treated as a reliable method for recovering private training data or hidden user data.
- FIELD execution is blocked until governance defines authorization and retention.
- Settlements are advisory-only to Abraxas by default.

## 10. Architecture

See `ARCHITECTURE.md`. Implementation target is adapter-based and contract-first. Initial reference runtime should favor open-weight Hugging Face-compatible models because hidden-state access is required.

## 11. Acceptance criteria

### Foundation gate `AC-G0`
- Constitution, architecture, system spec, glossary, status, roadmap, research basis, contracts, and traceability exist.
- JSON schemas parse and reject missing required fields.
- AGENTS instructions preserve provenance and doctrine.

### N0 `AC-N0`
- Same input/revision produces representation metadata reproducibly within tolerance.
- Comparison metrics have deterministic fixtures and null controls.

### N1 `AC-N1`
- Hidden-state capture works at declared sites for at least one open-weight model.
- Capture failures are explicit and replayable.

### N2 `AC-N2`
- SAE/probe experiment records contamination controls and feature consistency.
- At least one candidate is falsified or rejected; the pipeline must demonstrate ability to preserve negative evidence.

### N3 `AC-N3`
- EXP-001 completes with preregistered transformations and held-out perturbations.
- Invariance estimates include uncertainty and between-concept baselines.

### N4 `AC-N4`
- Cross-model alignment beats null baselines on held-out data and survives at least one distribution shift.
- Failure to meet threshold produces `REJECTED`, not a weaker semantic claim.

### N5 `AC-N5`
- Text and serialized-vector baselines exist.
- Latent channel provides measurable task/latency/compression benefit on held-out tasks.
- Semantic-equivalence claims remain separately tested.

## 12. Traceability

Every task must cite at least one requirement and one acceptance criterion. Every experiment must cite its workflow(s), state transitions, and output contract(s). See `TRACEABILITY.md`.

## 13. Implementation task families

- `T-001` repository/spec foundation
- `T-010` core contracts/types
- `T-020` Hugging Face model adapter
- `T-030` deterministic capture harness
- `T-040` representation comparison metrics
- `T-050` Hyperlexical transform interface
- `T-060` SAE/probe/falsification lab
- `T-070` causal intervention lab
- `T-080` cross-model alignment lab
- `T-090` settlement writer
- `T-100` EXP-001 execution
- `T-200` N5 latent channel research after gate

## 14. Verification

Verification requires:

- schema validation;
- deterministic unit fixtures;
- property tests for invalid/missing metadata;
- numerical tolerance tests;
- negative controls;
- reproducibility reruns;
- independent replication for promotion-worthy claims;
- explicit SHADOW review for drift/contamination;
- traceability completeness before merge.
