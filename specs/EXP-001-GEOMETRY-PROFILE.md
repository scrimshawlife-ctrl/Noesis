# EXP-001-GEO — Curvature-Aware Semantic Invariance Profile

Status: `DRAFT / CANON-SHADOW / ADVISORY_ONLY`
Version: `0.1.0`
Parent experiment: `EXP-001 — Semantic Invariance`

## 1. Purpose and boundary

This profile tests whether declared semantic relations are preserved under controlled surface transformation more reliably in a registered non-Euclidean or topological representation than in the Euclidean baseline.

The profile is an experiment-owned consumer of Noesis. It does not assert that meaning, cognition, culture, or model representations intrinsically form a manifold. It does not add a preferred geometry to Noesis core.

## 2. Research question

Which geometric or topological properties, if any, remain stable when surface form changes while declared semantic content is intended to remain stable?

## 3. Preregistered hypotheses

- `H-GEO-1`: at least one registered non-Euclidean candidate reduces held-out relational distortion relative to the dimension-matched Euclidean baseline.
- `H-GEO-2`: declared meaning-preserving transforms conserve neighborhood, order, and topology more strongly than meaning-altering controls.
- `H-GEO-3`: geometry advantage persists across held-out transform classes and is not explained by lexical overlap, radial collapse, projection dimension, or metric tuning.
- `H-GEO-NULL`: no registered geometry provides a reproducible held-out advantage after complexity penalties and controls.

Failure to reject `H-GEO-NULL` is a valid result.

## 4. Candidate spaces

Every candidate declares curvature, dimension, metric, fitting method, precision, initialization, constraints, and complexity cost.

| Candidate | Registered use | Required control |
|---|---|---|
| Euclidean | Flat reference and local similarity | Dimension-matched baseline |
| Hyperbolic | Hierarchy, branching, partial order | Fixed-radius Euclidean control and boundary-collapse diagnostic |
| Spherical | Cyclic, bounded, or angular relations | Normalized Euclidean/angular control |
| Product manifold | Mixed relational structures | Component ablation and complexity penalty |
| Topological profile | Multiscale connectivity, loops, and components | Label permutation and distance-preserving synthetic controls |

Unsupported or empirically unjustified candidates resolve to `NOT_COMPUTABLE`; they are not replaced after results are inspected.

## 5. Measurement objects

- `GeometryProfile`: preregistered candidate spaces, selection rule, controls, thresholds, and failure policy.
- `GeometricMetricResult`: direct result for one metric/candidate/split with nulls, uncertainty, diagnostics, and evidence references.
- `ProjectionLoss`: loss of registered relations after projection or compression.
- `GeometricRupture`: experiment-owned label for a preregistered failure of relational preservation. It is not a claim of semantic destruction.

## 6. Required metrics

All runs include:

- geodesic-distance distortion;
- `k`-nearest-neighbor retention;
- rank/order preservation for registered directed relations;
- held-out link or relation prediction where labels permit it;
- bootstrap uncertainty;
- shuffled-label and random-pair nulls;
- dimension- and parameter-matched Euclidean control;
- numerical stability and boundary/radius diagnostics;
- compute and model-complexity accounting.

When sample size and metric assumptions permit, runs may include persistent-homology summaries, local intrinsic-dimension estimates, curvature estimates, or path/transport measurements. Failure of their assumptions yields `NOT_COMPUTABLE`.

## 7. Flatland operationalization

The historical Flatland Effect is tested only as `ProjectionLoss`:

1. Register relations that the source representation must preserve.
2. Project or compress the representation.
3. measure preserved and lost relations on held-out data;
4. compare expressed confidence with measured preservation;
5. report loss without inferring intent, legitimacy, or social cause.

`ProjectionLoss` may support a later research interpretation. It cannot establish the full Flatland Effect by itself.

## 8. Dataset and partitions

The parent EXP-001 corpus supplies source fixtures and transform/control roles. `EXP-001-GEO` additionally requires:

- registered relational annotations or graph edges;
- `discovery`, `selection`, `confirmation`, and `control` partitions;
- at least one held-out concept family;
- at least one held-out transform family;
- meaning-altering controls including negation or role reversal;
- lexical-overlap-matched controls where feasible;
- synthetic fixtures with known Euclidean, hierarchical, cyclic, and mixed structure.

No geometry may be selected or tuned on the confirmation partition.

## 9. Workflow

1. Freeze the parent EXP-001 corpus and transform catalog.
2. Register `GeometryProfile` and candidate-space budgets.
3. Validate sample adequacy and candidate assumptions.
4. Capture or resolve immutable observations.
5. Fit candidates on discovery data only.
6. Select hyperparameters on the selection partition.
7. Freeze fitted artifacts and selection decision.
8. Evaluate once on confirmation and control partitions.
9. Execute component, dimension, lexical, radius, and shuffled nulls.
10. Emit `GeometricMetricResult` records and settle under `WF-007`.
11. Independently replicate before any promotion recommendation.

## 10. Selection rule

A non-Euclidean candidate is `SUPPORTED` only when it:

1. improves a preregistered primary held-out metric over the strongest dimension/parameter-matched Euclidean control;
2. exceeds the preregistered uncertainty and practical-effect threshold;
3. survives held-out concepts and transforms;
4. survives candidate-specific diagnostics;
5. provides improvement after complexity and compute penalties;
6. reproduces across required seeds and an independent run.

Possible decisions are `SUPPORTED`, `EQUIVALENT`, `REJECTED`, `INCONCLUSIVE`, and `NOT_COMPUTABLE`. `SUPPORTED` is scoped to the registered dataset, model, representation site, relations, transforms, and metric.

## 11. Failure and anti-overclaim rules

- High cosine similarity cannot substitute for relational preservation.
- Low geometric distortion cannot establish semantic truth.
- A visualization is not evidence unless its underlying metric is preregistered.
- Curvature fitted after confirmation-data inspection invalidates the run.
- Boundary concentration, numerical instability, or radius collapse must remain visible.
- Product-manifold improvement without component ablation is inconclusive.
- In-sample improvement without held-out gain is rejected.
- Model-specific results cannot be generalized to humans or other models.
- Topological similarity cannot establish causal or mechanistic identity.
- No result may be described as evidence of consciousness, hidden intent, or universal neuralese.

## 12. Acceptance evidence

`AC-N3-GEO` requires:

- schema-valid frozen `GeometryProfile`;
- resolved corpus, transform, observation, and relation hashes;
- complete Euclidean and registered non-Euclidean candidate results;
- confirmation partition untouched before freeze;
- negative and meaning-altering controls;
- candidate-specific diagnostics and ablations;
- uncertainty and practical-effect thresholds;
- independent replication classification;
- bounded settlement containing failures and contradictions.

Passing `AC-N3-GEO` accepts the measurement profile, not any universal geometry of meaning.

## 13. Outputs

- geometry profile and content hash;
- fitted candidate artifacts and hashes;
- geometric metric results;
- projection-loss report;
- null/control and diagnostic report;
- geometry-selection decision;
- independent replication settlement.

## 14. Initial posture

`SPECULATIVE`: semantic relations may exhibit reproducible mixed geometric structure.

`OBSERVED`: no repository evidence currently establishes a winning geometry.

`NOT_COMPUTABLE`: the winning geometry, effect magnitude, cross-model stability, and downstream utility remain unknown until the profile is executed after AC-N0/AC-N1 evidence is accepted.
