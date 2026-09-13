# Noesis Contracts

Status: `CANON-SHADOW`
Version: `0.2.0`

## Contract rules

1. Contracts are versioned JSON Schemas under `contracts/`.
2. IDs are stable and immutable after issuance.
3. Required provenance cannot be inferred from adjacent files.
4. Unknown/missing required evidence fails closed.
5. Additive schema changes require compatibility review; breaking changes require a new major schema version.
6. Tensor payloads are referenced by content-addressed artifact URIs and hashes rather than embedded by default.

## C-001 — ExperimentManifest

Purpose: immutable executable experiment registration.
Required semantic fields: experiment ID, schema version, research question, hypotheses, model identities, fixtures, transforms, representation sites, metrics, seeds, thresholds, environment requirements, data classification, creation time.
Invariants: hypothesis/threshold changes after registration produce a new manifest identity.

## C-002 — Observation

Purpose: immutable direct measurement record.
Required semantics: observation ID, run ID, manifest ID, fixture ID, model identity, representation site, tensor artifact reference/hash, shape/dtype, producer/environment, `OBSERVED` provenance.
Forbidden: inferred semantic labels as observation truth.

## C-003 — MetricResult

Purpose: deterministic measurement derived from observations.
Required semantics: metric ID/version, input observation IDs, preprocessing identity, value(s), units/aggregation, tolerance, null/control references, status.
Statuses: `MEASURED`, `NOT_COMPUTABLE`, `INVALID`.

## C-004 — InterventionResult

Purpose: record causal manipulation and measured effect.
Required semantics: baseline, intervention operation, source/target sites, magnitude/configuration, control condition, outcome metric, effect estimate, uncertainty, failures/limitations.

## C-005 — AlignmentMap

Purpose: versioned map between representation spaces.
Required semantics: source/target model/site identities, algorithm, fitting split/hash, learned artifact reference/hash, hyperparameters, validation/test results, null baseline, shift test, limitations.
Invariant: held-out test data cannot be used to fit or select the map.

## C-006 — Settlement

Purpose: durable epistemic conclusion.
Required semantics: proposition, provenance label, evidence references, evidence relation, confidence basis, limitations, promotion recommendation, creation metadata.
Allowed provenance: `OBSERVED`, `INFERRED`, `SPECULATIVE`, `NOT_COMPUTABLE`.
Invariant: contradictions and negative evidence must remain addressable from the settlement.

## C-007 — LatentChannelResult

Purpose: evaluate sender-to-receiver latent communication.
Required semantics: sender/receiver identities, channel representation, alignment/encoder/decoder references, task set, text baseline, serialized-vector baseline, compression budget, latency/information/task metrics, adversarial controls, semantic-equivalence result, settlement reference.
Invariant: task utility and semantic equivalence are separate fields.

## C-008 — FailureRecord

Purpose: make failures first-class rather than absent observations.
Required semantics: failure ID, run/manifest/fixture IDs, stage, error class, deterministic code, environment fingerprint, retry relationship if any.

## C-009 — SupersessionRecord

Purpose: preserve immutable history while identifying obsolete evidence.
Required semantics: old object ID, new object/defect reference, reason, operator/producer, UTC time.

## Boundary contracts

### Hyperlexical -> Noesis
Hyperlexical may provide immutable transform specifications and generated fixtures. It may not assign latent semantic truth.

### Noesis -> Abraxas
Noesis exposes settlements, evidence bundles, artifact hashes, and provenance. Noesis may recommend promotion but cannot mutate canon.

### Runtime adapter -> Noesis core
Adapters expose model identity, supported representation sites, capture capability, deterministic settings, and normalized observation metadata. Adapter-specific details must not leak into settlement semantics.
