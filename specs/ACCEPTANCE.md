# Noesis Acceptance Criteria

Status: `CANON-SHADOW`
Version: `0.2.1`

Acceptance is evidence-based. A capability does not pass because code exists.

Acceptance of a Noesis capability demonstrates that the measurement capability functions as specified. It does not constitute acceptance of every scientific hypothesis that uses that capability.

## AC-G0 — Specification foundation

PASS requires all:
- Constitution, architecture, requirements, journeys, workflows, state machines, contracts, data model, security/governance, acceptance, tasks, verification, glossary, roadmap/status, research basis, and traceability exist.
- Canonical schemas parse and enforce required provenance.
- Every FR/NFR is traceable to at least one workflow/task/verification route or explicitly marked governance-only.
- `OBSERVED`, `INFERRED`, `SPECULATIVE`, `NOT_COMPUTABLE` are used consistently.
- No document claims universal neuralese, latent thought transcripts, consciousness, or hidden intent as established fact.
- No core runtime contract requires an experiment-specific semantic theory.
- Experiment-specific hypotheses and ontologies remain externally replaceable.
- At least one rejected-hypothesis path demonstrates that scientific falsification does not invalidate the measurement apparatus.

## AC-N0 — Deterministic representation comparison

PASS requires:
- deterministic fixture set;
- exact model/tokenizer revision metadata;
- repeat capture/compare within declared numeric tolerance;
- at least cosine and one second metric verified against hand-checkable fixture;
- null/shuffled baseline implementation;
- malformed/incompatible input produces explicit failure/NOT_COMPUTABLE;
- artifact hashes verified before analysis.

Evidence: test log, fixture hashes, MetricResult examples, reproducibility report.

## AC-N1 — Hidden-state capture

PASS requires:
- at least one open-weight model adapter captures declared hidden-state sites;
- layer/site metadata is unambiguous and replayable;
- tensor shape/dtype/token-position metadata persisted;
- OOM/unsupported-site/non-finite failures explicitly represented;
- same manifest can be replayed on equivalent environment with expected tolerance;
- no undeclared representation sites captured.

Evidence: Observation examples, replay run, failure fixtures.

## AC-N2 — Feature/probe/intervention lab

PASS requires:
- at least one versioned feature dictionary or equivalent sparse representation;
- reconstruction/sparsity/dead-feature metrics recorded;
- run-to-run consistency measured when dictionary training is stochastic;
- lexical-trigger controls and semantic-positive-without-trigger controls executed;
- held-out probe evaluation with leakage control;
- at least one candidate feature/probe is rejected or weakened, demonstrating negative-evidence preservation;
- at least one causal intervention or explicit statement that causal access is unavailable and claim is bounded accordingly.

Evidence: FeatureHypothesis, MetricResult, InterventionResult/limitation, Settlement.

## AC-N3 — Semantic invariance

PASS requires EXP-001:
- preregistered concept set and transformations;
- expected invariant and changed attributes per transform class;
- discovery/confirmation or train/test separation where hypotheses were tuned;
- within-concept vs between-concept comparisons;
- lexical, adversarial, negation/role, multilingual or equivalent registered controls;
- uncertainty estimate for aggregate claims;
- at least one held-out transform family;
- explicit settlement of what is invariant, what is surface-sensitive, and what remains NOT_COMPUTABLE.

Passing AC-N3 validates the declared EXP-001 result under its evidence and controls. It does not make semantic invariance a core Noesis assumption.

## AC-N4 — Cross-space alignment

PASS requires:
- preregistered source/target spaces;
- train/validation/test partition hashes;
- map frozen before held-out test;
- beats shuffled/random/null mapping by preregistered threshold;
- neighborhood/geometry preservation metric;
- at least one distribution shift;
- semantic equivalence evaluated separately from geometric alignment;
- failure to pass threshold yields REJECTED/WEAK, not narrative downgrade.

## AC-N3-GEO — Curvature-aware semantic invariance profile

PASS requires:
- frozen schema-valid `GeometryProfile` with Euclidean baseline;
- discovery/selection/confirmation/control partition hashes;
- confirmation partition inaccessible before fitted artifacts and selection are frozen;
- geodesic distortion, neighborhood retention, registered relation preservation, uncertainty, and nulls;
- meaning-altering and lexical-overlap controls;
- candidate-specific stability and degeneracy diagnostics;
- dimension/parameter matching, compute accounting, and complexity penalty;
- component ablation for product manifolds;
- held-out concept and transform evaluation;
- independent replication classification;
- settlement explicitly scopes the result and preserves rejected, invalid, and `NOT_COMPUTABLE` candidates.

PASS accepts the profile's measurement validity. It does not accept a universal geometry of meaning.

## AC-N5 — Latent communication research

ENTRY requires:
- AC-N4 accepted;
- explicit operator authorization;
- sender/receiver identities and channel contract frozen;
- information/privacy controls defined.

PASS requires:
- text baseline;
- serialized-vector baseline;
- latent-channel run;
- held-out task set;
- latency, compression/information budget, and task-quality metrics;
- adversarial/distribution controls;
- leakage/covert-transfer evaluation;
- semantic-equivalence claim separately tested;
- task success not described as proof of universal neuralese.

## AC-R1 — Reproducibility

PASS requires:
- independent rerun from manifest;
- required artifacts resolvable by hash;
- environment differences disclosed;
- result envelope within registered tolerance or discrepancy settled explicitly.

## AC-R2 — Independent replication

PASS requires:
- reviewer/operator independent from original evidence production where practical;
- replication manifest references but does not mutate original;
- at least one new control or independently generated fixture set;
- result categorized as replicated, partially replicated, failed replication, or NOT_COMPUTABLE.

Required before `PROMOTION_ELIGIBLE`.

## AC-S1 — Security/privacy

PASS requires:
- no secrets in tracked fixtures/config;
- data classification declared;
- sensitive data has retention/deletion/access scope;
- artifact integrity checks pass;
- authorization exists for FIELD/N5/sensitive scopes;
- incident/supersession path tested at least once with synthetic evidence.

## Gate settlement template

```text
Gate ID:
Decision: ACCEPT | REJECT | DEFER | NOT_COMPUTABLE
UTC time:
Scope:
Evidence IDs/hashes:
Contradictions/negative results:
Known limitations:
Operator/reviewer:
Next permitted capability/state:
```
