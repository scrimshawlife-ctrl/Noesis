# Noesis Requirements

Status: `CANON-SHADOW`
Version: `0.2.1`

## 1. Scope

This document is the normative requirement catalog for Noesis. Requirements are implementation-independent unless explicitly constrained by reproducibility, evidence, or safety needs.

## 2. Functional requirements

### Capture and identity
- `FR-001` Noesis SHALL capture embeddings and hidden-state representations from supported runtimes.
- `FR-002` Every capture SHALL identify model family, exact revision where available, tokenizer revision, representation site, layer, dtype, device class, and runtime version.
- `FR-003` Every input fixture SHALL be immutable after experiment registration and SHALL have a stable content hash.
- `FR-004` Noesis SHALL distinguish model output text from latent observations.
- `FR-005` Failed capture attempts SHALL be persisted as explicit failure records rather than omitted.

### Transformations and fixtures
- `FR-010` Noesis SHALL accept deterministic fixture transforms defined locally or supplied by Hyperlexical through a versioned contract.
- `FR-011` Every transform SHALL declare transformation class, semantic intent, expected invariants, and expected changed attributes.
- `FR-012` Transform provenance SHALL include transform version and content hash.
- `FR-013` Evaluation sets SHALL support train/validation/test or discovery/confirmation separation where hypothesis fitting occurs.

### Comparison and metrics
- `FR-020` Noesis SHALL compute experiment-declared representation metrics.
- `FR-021` Noesis SHALL support at minimum cosine similarity, Euclidean distance, centered kernel alignment where mathematically valid, and neighborhood-overlap metrics.
- `FR-022` Metrics SHALL declare preprocessing, aggregation, precision, and tolerance.
- `FR-023` Metric execution SHALL reject incompatible inputs rather than coerce them silently.
- `FR-024` Null, shuffled, or random baselines SHALL be supported for every metric family used to make an inferential claim.
- `FR-025` Uncertainty estimates SHALL accompany aggregate invariance or alignment claims when repeated samples permit estimation.
- `FR-026` Registered geometry profiles SHALL include a dimension-matched Euclidean baseline and SHALL NOT privilege a non-Euclidean candidate before measurement.
- `FR-027` Geometry selection SHALL use separated discovery, selection, confirmation, and control partitions when fitting or model selection occurs.
- `FR-028` Geometric claims SHALL report candidate-specific degeneracy, numerical-stability, and complexity diagnostics.
- `FR-029` Failure of manifold, sample-adequacy, metric, or numerical assumptions SHALL yield `NOT_COMPUTABLE` or `INVALID`, not a substituted geometry.

### Sparse features and probes
- `FR-030` Noesis SHALL support versioned sparse feature dictionaries, including SAE-derived dictionaries.
- `FR-031` Feature dictionaries SHALL report reconstruction quality, sparsity, dead-feature rate, training configuration, and source activation distribution.
- `FR-032` Candidate semantic feature descriptions SHALL be stored as hypotheses, never as intrinsic labels.
- `FR-033` Feature promotion SHALL require lexical-trigger controls, semantic-positive controls, negative controls, and run-to-run consistency evidence.
- `FR-034` Learned probes SHALL declare training data, held-out evaluation data, baselines, regularization, and leakage controls.
- `FR-035` Probe accuracy alone SHALL NOT authorize a mechanistic or causal claim.

### Causal intervention
- `FR-040` Noesis SHALL support intervention records for patching, ablation, steering, injection, or equivalent causal manipulation where runtime access permits.
- `FR-041` Every intervention SHALL identify source site, target site, magnitude/operation, control condition, and measured outcome.
- `FR-042` Noesis SHALL preserve null and contradictory causal outcomes.
- `FR-043` A semantic/function claim SHALL NOT exceed `INFERRED` without causal evidence when a causal mechanism is asserted.

### Alignment
- `FR-050` Noesis SHALL support explicit learned or analytic maps between representation spaces.
- `FR-051` Alignment fitting SHALL use a declared training partition and SHALL evaluate on held-out data.
- `FR-052` Alignment claims SHALL be compared with null/shuffled mappings.
- `FR-053` Cross-model semantic equivalence SHALL remain distinct from geometric alignment.
- `FR-054` Distribution-shift evaluation SHALL be required before N4 acceptance.

### Settlement and evidence
- `FR-060` Noesis SHALL emit immutable `Observation`, `MetricResult`, `InterventionResult`, `AlignmentMap`, and `Settlement` records under versioned schemas.
- `FR-061` Every settlement SHALL cite the exact evidence objects used.
- `FR-062` Evidence SHALL be classified as supporting, contradicting, control, or negative result where applicable.
- `FR-063` Missing or insufficient signal SHALL yield `NOT_COMPUTABLE` or `INCONCLUSIVE`, never fabricated completion.
- `FR-064` Settlement promotion SHALL be advisory-only to Abraxas unless separately authorized.
- `FR-065` Independent replication SHALL be required for promotion-worthy claims beyond CANON-SHADOW.

### Reproducibility
- `FR-070` Experiments SHALL be registered through an immutable `ExperimentManifest`.
- `FR-071` The manifest SHALL record seeds, software/runtime versions, model revisions, fixture hashes, transform hashes, metrics, thresholds, and declared hypotheses.
- `FR-072` Noesis SHALL support deterministic replay when dependencies remain available.
- `FR-073` Replays under materially different dependencies SHALL receive a new run identity and environment fingerprint.
- `FR-074` Artifact hashes SHALL detect mutation or mismatch.

### External interfaces
- `FR-080` Hyperlexical integration SHALL be contract-based and SHALL NOT grant Hyperlexical authority over latent settlements.
- `FR-081` Abraxas integration SHALL expose settlements and evidence references without allowing Noesis to mutate Abraxas canon directly.
- `FR-082` Adapter implementations SHALL be replaceable without changing canonical evidence semantics.

### Research neutrality
- `FR-083` Noesis SHALL accept experiment-specific hypotheses, semantic labels, transform classes, expected invariants, and interpretation frameworks through versioned external contracts rather than core runtime assumptions.
- `FR-084` Noesis SHALL preserve experiment-defined semantics as declared metadata and SHALL NOT promote them to observed latent truth.
- `FR-085` Core measurement operations SHALL remain executable when an experiment hypothesis is false, rejected, superseded, or replaced.
- `FR-086` Experiment-specific ontologies SHALL be replaceable without changing canonical observation, metric, failure, intervention, alignment, or settlement semantics.
- `FR-087` Noesis SHALL distinguish instrument outputs from theory-dependent interpretations of those outputs.
- `FR-088` A research-specific construct SHALL require explicit architecture review before promotion into core Noesis ontology.

### Latent communication
- `FR-090` Latent agent communication SHALL remain disabled by default.
- `FR-091` Latent communication experiments SHALL require accepted N4 evidence plus explicit operator authorization.
- `FR-092` Latent communication SHALL include text and serialized-vector baselines.
- `FR-093` Compression/task utility SHALL be evaluated independently from semantic-equivalence claims.
- `FR-094` Receiver-side task success SHALL NOT be interpreted as proof of universal neuralese.

## 3. Non-functional requirements

### Reproducibility and determinism
- `NFR-001` Deterministic operations SHALL reproduce within declared numeric tolerance.
- `NFR-002` Sources of nondeterminism SHALL be recorded when exact reproduction is unavailable.
- `NFR-003` Content-addressed artifacts SHALL use SHA-256 or stronger hashes.

### Auditability
- `NFR-010` Every evidence object SHALL carry schema version, creation time in UTC, producer identity/version, and provenance.
- `NFR-011` Evidence lineage SHALL be queryable from settlement back to source fixture.
- `NFR-012` Contradictory evidence SHALL NOT be silently removed from a settled bundle.

### Modularity
- `NFR-020` Runtime adapters, metrics, transforms, and experiment methods SHALL be separately replaceable modules.
- `NFR-021` No hidden coupling SHALL exist between SHADOW and FORECAST lanes.
- `NFR-022` Abraxas, Hyperlexical, and Noesis SHALL exchange only explicit versioned contracts.
- `NFR-023` The Noesis core SHALL remain hypothesis-neutral and SHALL NOT require any specific semantic theory, interpretability framework, or research-program ontology.
- `NFR-024` Research-program packages SHALL depend on Noesis core; Noesis core SHALL NOT depend on research-program packages.
- `NFR-025` Rejection or supersession of a scientific hypothesis SHALL NOT invalidate previously valid raw observations or theory-independent metric results.

### Failure semantics
- `NFR-030` Invalid or incomplete evidence SHALL fail closed.
- `NFR-031` Unsupported operations SHALL return explicit capability errors.
- `NFR-032` Numeric overflow, NaN, or infinite values SHALL be detected and surfaced.

### Portability
- `NFR-040` Reference implementation SHALL target Python and open-weight transformer runtimes.
- `NFR-041` Core contracts SHALL NOT depend on a single model vendor.
- `NFR-042` Hardware-specific optimization SHALL NOT change evidence meaning.

### Privacy and security
- `NFR-050` Data minimization SHALL be the default.
- `NFR-051` Secrets and credentials SHALL never be persisted in experiment fixtures or evidence artifacts.
- `NFR-052` Sensitive experiments SHALL declare retention and deletion rules.
- `NFR-053` FIELD execution SHALL remain blocked until explicitly governed.

### Performance
- `NFR-060` Performance optimization SHALL not bypass provenance, validation, or evidence persistence.
- `NFR-061` Large tensors SHALL be stored outside transactional metadata when practical.

## 4. Out of scope for initial implementation

- Universal neuralese decoding.
- Claims of consciousness, subjective state, or hidden intent.
- Closed-model hidden-state extraction without explicit supported access.
- Autonomous production behavior steering.
- Canon mutation.
- Training-data reconstruction as a product feature.
- Privileging one research thesis, semantic ontology, or funding framing as core Noesis doctrine.

## 5. Requirement change rule

Any change that alters claim strength, promotion criteria, provenance semantics, governance authority, experimental gate conditions, or core-vs-research ontology boundaries requires explicit spec review and traceability update.
