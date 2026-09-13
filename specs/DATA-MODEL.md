# Noesis Data Model

Status: `CANON-SHADOW`
Version: `0.2.0`

## Principles

- Metadata and large tensor artifacts are separate concerns.
- Evidence is append-only after issuance.
- Content hashes identify bytes; logical IDs identify domain objects.
- Every derived object points to exact parent evidence.
- No semantic interpretation is stored as raw observation truth.

## Core entities

### ModelIdentity
Fields: `model_id`, provider/source, family, revision, weights hash where available, tokenizer ID/revision, license/provenance, architecture metadata, supported adapter version.

### RepresentationSite
Fields: `site_id`, model family, module path/logical site, layer index, tensor role, token alignment rule, expected rank/shape pattern.

### InputFixture
Fields: `fixture_id`, source content or external content hash, modality, concept/task labels used for experiment design, data classification, provenance, immutable content hash.

### Transform
Fields: `transform_id`, class, implementation/version, semantic intent, expected preserved attributes, expected modified attributes, source fixture ID, output fixture ID, hash.

### ExperimentManifest
Fields: experiment ID, version, research question, hypotheses/nulls, fixtures, transforms, models, sites, metrics, thresholds, seeds, partition definitions, environment requirements, governance classification, status.

### Run
Fields: `run_id`, manifest ID, environment fingerprint, start/end UTC, runtime versions, hardware class, deterministic flags, status.

### Observation
Fields: observation ID, run ID, fixture ID, model/site IDs, artifact URI/hash, tensor shape/dtype, token-position metadata, capture status, provenance.

### FeatureDictionary
Fields: dictionary ID, source observation distribution, training manifest, architecture, dimensions, sparsity settings, seed, artifact hash, reconstruction metrics, dead-feature rate, consistency metrics.

### FeatureHypothesis
Fields: hypothesis ID, dictionary/feature ID, proposed description, proposer, creation time, supporting discovery examples. The description is explicitly non-canonical.

### Probe
Fields: probe ID, target hypothesis, training/validation/test partition hashes, algorithm, hyperparameters, baselines, artifact hash, metrics.

### InterventionResult
Fields: intervention ID, parent hypothesis, baseline observation/result refs, operation, source/target sites, magnitude/config, controls, outcome metrics, uncertainty, status.

### AlignmentMap
Fields: alignment ID, source/target representation spaces, train/validation/test partition hashes, algorithm, hyperparameters, artifact hash, held-out results, null results, shift results, status.

### MetricResult
Fields: metric result ID, metric definition/version, input refs, preprocessing ID, values, uncertainty, null/control refs, tolerance, status.

### EvidenceBundle
Fields: bundle ID, proposition/question, typed evidence refs, bundle hash, creator, UTC time.

### Settlement
Fields: settlement ID, proposition, provenance label, evidence relations, confidence basis, limitations, recommendation, lifecycle status, supersession refs.

### FailureRecord
Fields: failure ID, run/fixture/operation references, stage, code, message-safe details, environment fingerprint, retry-of ID.

### SupersessionRecord
Fields: supersession ID, original object ID, successor/defect reference, reason, timestamp, actor.

## Relationships

```text
ExperimentManifest 1---* Run
ExperimentManifest *---* InputFixture
InputFixture 1---* Transform
Run 1---* Observation
Observation *---* MetricResult
Observation *---* FeatureDictionary
FeatureDictionary 1---* FeatureHypothesis
FeatureHypothesis 1---* Probe
FeatureHypothesis 1---* InterventionResult
Observation *---* AlignmentMap
MetricResult/InterventionResult/AlignmentMap *---* EvidenceBundle
EvidenceBundle 1---* Settlement
Settlement 0..1---* SupersessionRecord
```

## Artifact storage

Large tensors, SAE weights, alignment matrices, and serialized channel payloads should be stored content-addressably outside transactional metadata. Metadata must carry URI/reference, hash algorithm, hash value, media type, size, and optional compression descriptor.

## Identity rules

- Logical IDs: UUIDv7/ULID-equivalent sortable opaque identifiers are acceptable.
- Hashes: SHA-256 minimum.
- Timestamps: UTC ISO-8601.
- Schema version: mandatory on every externally persisted contract.
- Parent relationships: immutable.

## Retention classes

- `PUBLIC_REPRODUCIBLE`: safe fixture/evidence intended for durable retention.
- `RESEARCH_INTERNAL`: non-public research artifacts; retention policy declared per experiment.
- `SENSITIVE`: explicit approval, minimization, retention/deletion policy required.
- `PROHIBITED`: credentials, secrets, unauthorized proprietary/training/user data.

`PROHIBITED` data may not enter Noesis evidence storage.