# Noesis Contracts

Status: `CANON-SHADOW`
Version: `0.2.4`

## Contract rules

1. Contracts are versioned JSON Schemas under `contracts/`.
2. IDs are stable and immutable after issuance.
3. Required provenance cannot be inferred from adjacent files.
4. Unknown/missing required evidence fails closed.
5. Additive schema changes require compatibility review; breaking changes require a new major schema version.
6. Tensor payloads are referenced by content-addressed artifact URIs and hashes rather than embedded by default.
7. Contract presence records an interface or hypothesis surface; it does not establish the scientific truth of experiment-owned fields.

## Contract layering

### Core contracts
Stable, research-neutral evidence primitives whose semantics remain valid across competing hypotheses and unrelated research programs.

Core contracts include:
- `C-001` ExperimentManifest
- `C-002` Observation
- `C-003` MetricResult
- `C-004` InterventionResult
- `C-005` AlignmentMap
- `C-006` Settlement
- `C-007` LatentChannelResult
- `C-008` FailureRecord
- `C-009` SupersessionRecord

### Integration contracts
External-system boundaries that transport inputs or outputs without defining scientific truth.

Integration contracts include:
- `C-010` HyperlexTransformRequest
- `C-011` HyperlexTransformResult
- runtime/model adapter capability surfaces
- fixture import/export boundaries

### Research contracts
Experiment- or program-specific schemas. These may evolve, be replaced, or disappear without redefining Noesis core evidence semantics.

Research contracts currently include:
- `C-012` EXP001SourceCorpus
- `C-014` EXP001TransformCatalog
- experiment-specific semantic taxonomies, task hypotheses, and benchmark definitions

`C-013` N01AcceptanceEvidence is a gate-evidence contract for a core capability and does not assert a research thesis.

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

## C-010 — HyperlexTransformRequest
Purpose: request a controlled lexical/symbolic transformation without granting Hyperlex latent-settlement authority.
Required semantics: request ID, source fixture ID/text, transform class, semantic intent, expected invariants, expected changed attributes, seed, optional parameters.
Invariant: semantic intent and expected invariants are hypotheses supplied to the experiment, not latent truth labels.
Schema: `contracts/hyperlex-transform-request.schema.json`.

## C-011 — HyperlexTransformResult
Purpose: immutable, versioned transform output that can be materialized as a Noesis input fixture.
Required semantics: transform/request/source identities, output text, transform class/version, output SHA-256, semantic intent, expected invariants, expected changed attributes, provider metadata, `OBSERVED` provenance.
Invariant: the output hash must match the exact transformed text before fixture materialization.
Schema: `contracts/hyperlex-transform-result.schema.json`.

## C-012 — EXP001SourceCorpus
Purpose: freeze operator-approved EXP-001 source fixtures without inventing semantic content inside Noesis.
Required semantics: corpus/version identity, data classification, fixture IDs/text/hashes, hypothesis tags, discovery/confirmation/control partition, creation time.
Invariant: fixture text or partition changes require a new corpus version; duplicate fixture IDs fail closed.
Schema: `contracts/exp001-source-corpus.schema.json`.

## C-013 — N01AcceptanceEvidence
Purpose: durable AC-N0/AC-N1 acceptance evidence from repeated captures against one declared model/runtime identity.
Required semantics: model/revision identity, fixture and seed, numeric tolerance, per-site observations/failures/comparisons, gate decisions, limitations.
Invariant: this contract settles capture reproducibility only; it cannot establish semantic invariance or mechanistic interpretation.
Schema: `contracts/n01-acceptance-evidence.schema.json`.

## C-014 — EXP001TransformCatalog
Purpose: preregister the operator-owned transform/control hypotheses that Hyperlex will execute.
Required semantics: catalog/version identity and transform entries containing class, semantic intent, expected invariants, expected changed attributes, optional parameters, and experimental role.
Invariant: the catalog states hypotheses and controls only; it does not establish that a transformation actually preserved its intended meaning.
Schema: `contracts/exp001-transform-catalog.schema.json`.

## Research-owned metadata rule

The following are experiment-owned claims or expectations unless independently observed:
- `semantic_intent`
- `expected_invariants`
- `expected_changed_attributes`
- concept labels
- hypothesis tags
- transform taxonomies
- theoretical categories
- predicted relationships

Their presence in a versioned contract records what the experiment intends to test. It does not make those statements Noesis observations.

Noesis preserves the distinction:

```text
DECLARED HYPOTHESIS
        !=
OBSERVATION
        !=
INFERENCE
        !=
SETTLEMENT
```

## Boundary contracts

### Hyperlex -> Noesis
Hyperlex may provide immutable transform specifications and generated fixtures. It may declare intended semantic invariants and expected changed attributes. It may not assign latent semantic truth, feature meaning, mechanistic interpretation, or settlement status.

Current transport bindings:
- callable/in-process adapter;
- JSON-over-HTTP adapter;
- deterministic CI adapter (test-only).

The trained Hyperlex model remains replaceable behind the adapter protocol until its inference surface stabilizes.

### Noesis -> Abraxas
Noesis exposes settlements, evidence bundles, artifact hashes, and provenance. Noesis may recommend promotion but cannot mutate canon.

### Runtime adapter -> Noesis core
Adapters expose model identity, supported representation sites, capture capability, deterministic settings, and normalized observation metadata. Adapter-specific details must not leak into settlement semantics.
