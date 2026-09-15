# Noesis Verification Plan

Status: `CANON-SHADOW`
Version: `0.2.1`

## 1. Verification doctrine

Verification must test both correctness and epistemic behavior. A technically correct pipeline that overstates evidence fails verification.

## 2. Layers

### V-001 — Schema verification
- all JSON Schemas parse;
- required fields enforced;
- invalid provenance rejected;
- unknown required-contract versions fail closed;
- representative valid and invalid fixtures committed.

### V-002 — Deterministic unit verification
- hash generation stable;
- ID and timestamp handling valid;
- deterministic transforms reproduce exact expected content;
- deterministic metrics reproduce expected values within tolerance;
- preprocessing identity contributes to metric identity.

### V-003 — Adapter verification
- exact model/tokenizer revision reported;
- supported/unsupported sites declared correctly;
- known fixture captures expected tensor ranks/shapes;
- non-finite tensor detection works;
- revision mismatch fails explicitly.

### V-004 — Capture replay verification
- same manifest on equivalent environment reproduces metadata and expected numeric envelope;
- environment changes produce new fingerprint/run identity;
- artifact hashes verify before analysis;
- failed captures create FailureRecord objects.

### V-005 — Metric verification
- cosine/Euclidean checked against hand-computable vectors;
- CKA checked against trusted small fixture;
- shuffled/random null behaves as expected;
- incompatible dimensions or insufficient sample count produce NOT_COMPUTABLE;
- uncertainty calculations tested against deterministic synthetic distributions.

### V-006 — Feature/probe falsification verification
- lexical cue alone can be intentionally constructed to expose contamination;
- semantic-positive-without-cue fixtures exist;
- negative/confound fixtures exist;
- train/test leakage detector has a positive test case;
- at least one candidate is rejected/weakened by the pipeline.

### V-007 — Causal intervention verification
- baseline/control/intervention ordering and identities preserved;
- null intervention yields near-zero expected effect on synthetic fixture;
- known synthetic intervention produces expected direction;
- failed/unstable interventions remain visible.

### V-008 — Alignment verification
- synthetic spaces with known linear mapping recover expected map;
- shuffled pairing fails null threshold;
- train/validation/test isolation enforced;
- held-out and shift metrics separately reported;
- semantic-equivalence fields never auto-populate from geometric metrics.

### V-009 — Settlement verification
- settlement cannot cite nonexistent evidence;
- contradictions remain represented;
- missing required evidence yields NOT_COMPUTABLE/INCONCLUSIVE;
- causal claim without intervention evidence is bounded;
- recommendation does not mutate external canon.

### V-010 — Security/privacy verification
- secret-scanning fixture catches synthetic credential patterns;
- PROHIBITED data class rejected;
- sensitive experiment without retention/access scope rejected;
- unauthorized FIELD/N5 execution rejected;
- artifact substitution detected by hash mismatch.

### V-011 — Traceability verification
Every implementation PR must identify:
- requirement IDs;
- journey/workflow IDs;
- affected state transitions;
- contract IDs;
- acceptance gate(s);
- verification evidence.

CI SHALL fail when canonical spec references drift or required documents disappear.

### V-012 — Reproducibility verification
- rerun a representative manifest from clean environment;
- compare dependency fingerprint;
- compare observation/metric envelopes;
- settle discrepancies explicitly.

### V-013 — Independent replication
For promotion-worthy claims:
- independent fixture/control generation where practical;
- separate run identity;
- source result not editable;
- result classified as `REPLICATED`, `PARTIAL`, `FAILED_REPLICATION`, or `NOT_COMPUTABLE`.

### V-014 — N5 latent-channel verification
Only after authorization:
- baseline parity checks;
- compression/latency/task metrics;
- channel ablation;
- randomized channel control;
- covert-transfer/leakage probes;
- semantic mismatch controls;
- held-out task and distribution-shift sets.

### V-015 — Curvature-aware geometry verification
- synthetic Euclidean, tree, cyclic, and mixed-structure fixtures recover their registered control structure within tolerance;
- confirmation partition access is blocked until fitted artifacts and selection decision are frozen;
- every non-Euclidean result has a dimension/parameter-matched Euclidean control;
- shuffled labels and random pairs fail the registered preservation threshold;
- hyperbolic boundary/radius collapse and non-finite operations are detected;
- spherical normalization and antipodal ambiguities are reported where applicable;
- product-manifold component ablations are required;
- topological metrics enforce sample and filtration assumptions;
- selection includes uncertainty, practical effect, complexity, and compute cost;
- failure of assumptions emits `NOT_COMPUTABLE` or `INVALID`;
- settlement cannot infer semantic truth or universal geometry from geometric fit.

### V-017 — Hypothesis-neutrality verification
PASS requires:
- core modules execute without importing experiment-specific packages;
- replacing an experiment transform taxonomy does not change Observation semantics;
- rejecting an experiment hypothesis does not invalidate raw capture artifacts;
- experiment labels cannot populate `OBSERVED` latent-semantic fields;
- integration adapters cannot issue settlements;
- core tests contain at least one fixture whose experiment-level expected invariant is deliberately false;
- the resulting system preserves the observation and records the failed hypothesis without treating the instrument as failed.

### V-018 — Ontology leakage verification
PASS requires structural verification that core modules do not depend on:
- EXP-001-specific concepts;
- Hyperlex-specific semantic categories;
- research-program-specific labels;
- theory-specific settlement assumptions.

Any such dependency requires explicit architectural justification or relocation behind an external contract.

## 3. CI gates

Minimum pre-merge CI:
1. spec validator;
2. JSON Schema validation;
3. unit tests;
4. type/static checks when runtime exists;
5. contract example tests;
6. traceability check;
7. hypothesis-neutrality and ontology-leakage checks where applicable.

Research-result PRs additionally require experiment-specific verification artifacts and settlement validation.

## 4. Evidence packet

Every gate packet should contain:
- code commit SHA;
- manifest hash;
- environment fingerprint;
- fixture/partition hashes;
- result artifact hashes;
- test/verification output;
- negative/contradictory evidence;
- settlement ID;
- reviewer/operator decision where required.

## 5. Non-verifiable claims

The following are not accepted merely from Noesis measurements and should resolve to `NOT_COMPUTABLE` unless separately operationalized with valid evidence:
- consciousness;
- subjective experience;
- hidden intent;
- universal neuralese;
- faithful transcript of private chain-of-thought;
- semantic identity inferred solely from vector similarity;
- truth of any experiment-specific ontology merely because Noesis can measure against it.
