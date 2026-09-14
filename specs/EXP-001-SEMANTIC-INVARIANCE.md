# EXP-001 — Semantic Invariance

Status: `DRAFT / CANON-SHADOW`

## Research question
Which latent structures remain stable when semantic content is preserved while surface form changes?

## Hypotheses

- `H1` Within-concept representation similarity exceeds between-concept similarity across controlled transformations.
- `H2` Some candidate features remain stable across lexical/register/language transformations while surface-sensitive features do not.
- `H3` Candidate semantic features that are only lexical artifacts will fail targeted trigger/falsification controls.

## Corpus
Initial target: 100 concepts spanning relation, agency, boundary, exchange, threat, identity, causality, temporal change, social role, and symbolic/archetypal categories. Concept selection must be frozen before execution.

## Transform classes

- literal paraphrase
- colloquial/slang
- metaphorical
- symbolic/emoji
- technical/register shift
- multilingual translation
- negation
- compositional role reversal
- adversarial paraphrase
- lexical-trigger controls

Each transform declares whether semantics are expected to be `PRESERVED`, `ALTERED`, or `CONTROL`.

## Procedure

1. Register manifest under `WF-001`.
2. Generate/freeze transform set; human or independent validator reviews semantic-intent labels.
3. Capture declared layers/sites under `WF-002`.
4. Compute within/between concept metrics under `WF-003`.
5. Train/load SAE only if the experiment includes sparse-feature analysis.
6. For each candidate feature, execute `WF-004` falsification sequence.
7. Bootstrap uncertainty and run permutation/null baselines.
8. Hold out at least one transformation class from any alignment/probe fitting.
9. Emit settlement under `WF-006`.

## Metrics

Required:
- cosine similarity or distance after declared normalization;
- within-vs-between effect size;
- bootstrap confidence interval;
- permutation/null comparison;
- nearest-neighbor concept preservation.

Recommended where appropriate:
- CKA/RSA;
- linear-probe transfer to held-out transform classes;
- SAE feature activation stability;
- SAE dictionary run-to-run consistency;
- causal intervention effect size.

## Contamination controls

- replace reasoning-associated lexical tokens with neutral alternatives;
- inject candidate-associated tokens into semantically unrelated text;
- use semantic-positive inputs that avoid candidate-associated lexical cues;
- create non-reasoning negatives that preserve likely surface correlates;
- hold out templates and transformation generators.

## Acceptance

A candidate may be described as a **representation invariant** only if:

1. predefined invariance metric beats between-concept/null baseline;
2. effect persists on held-out transformations;
3. lexical-trigger falsification does not explain the effect;
4. result reproduces across at least two seeds/runs;
5. uncertainty bounds and negative results are reported.

A candidate may be described as **functionally relevant** only with causal evidence. Without causal evidence, maximum claim is correlational `INFERRED`.

## Outputs

- experiment manifest
- observation index
- metric results
- optional SAE/probe artifacts
- falsification report
- settlement

## Optional registered profile — EXP-001-GEO

`specs/EXP-001-GEOMETRY-PROFILE.md` defines a curvature-aware profile for testing relational preservation in Euclidean, hyperbolic, spherical, product-manifold, and topological candidates. It is not active by default. A manifest that enables it must freeze candidate spaces, partitions, metrics, nulls, diagnostics, complexity penalties, and selection rules before confirmation data is accessed.

No geometric result establishes semantic truth. A geometry advantage is scoped to the registered model, site, corpus, relations, transforms, dimensions, and metrics.

## Failure modes

- semantic drift introduced by transformations;
- lexical artifacts dominating feature activation;
- SAE dictionary instability;
- layer-specific effects overgeneralized to model-wide claims;
- probe leakage/template memorization;
- translation changing pragmatics rather than surface form alone.

Any unresolved failure mode capable of explaining the main result forces `INCONCLUSIVE` or `NOT_COMPUTABLE`.
