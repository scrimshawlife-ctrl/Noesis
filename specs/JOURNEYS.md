# Noesis Journeys

Status: `CANON-SHADOW`
Version: `0.2.0`

Journeys describe end-to-end actor objectives. They do not replace workflows.

## J-001 — Test semantic invariance

**Actor:** Researcher
**Objective:** Determine whether a concept retains measurable representational structure across controlled surface transformations.
**Entry conditions:** approved hypothesis, fixture set, model/runtime access, registered metrics.
**Path:**
1. Define concept set and expected invariant/changing attributes.
2. Register source fixtures and transformations.
3. Capture representations at declared sites.
4. Compute within-concept and between-concept baselines.
5. Evaluate held-out transformations.
6. Test lexical and semantic controls.
7. Settle evidence as supported, weak, rejected, inconclusive, or not computable.
**Success:** AC-N3 evidence packet exists.
**Failure:** insufficient provenance, invalid controls, or non-reproducible capture.

## J-002 — Evaluate a candidate latent feature

**Actor:** Mechanistic-interpretability researcher
**Objective:** Determine whether a discovered feature tracks a hypothesized property rather than a superficial correlate.
**Path:** discovery → description hypothesis → lexical-trigger controls → semantic-positive controls → negative controls → run consistency → causal intervention → replication → settlement.
**Success:** feature receives a bounded claim with explicit limitations.
**Invariant:** feature explanation never becomes intrinsic ontology merely by annotation.

## J-003 — Align two representation spaces

**Actor:** Researcher
**Objective:** Test whether two layers/models admit a useful, held-out alignment map.
**Path:** paired corpus → split → fit mapping → validation selection → held-out evaluation → null mapping → distribution shift → settlement.
**Success:** AC-N4 evidence packet exists.
**Failure:** alignment only works in-sample, does not beat null, or collapses under shift.

## J-004 — Consume Noesis evidence in Abraxas

**Actor:** Abraxas operator or evidence consumer
**Objective:** Use a Noesis settlement without granting it canonical authority.
**Path:** validate settlement schema → resolve evidence references → inspect contradictions/controls → consume as advisory evidence → independently decide whether any external promotion process should begin.
**Invariant:** Noesis cannot directly mutate Abraxas canon.

## J-005 — Execute reproducible representation capture

**Actor:** Research engineer
**Objective:** Produce replayable, content-addressed observations for a registered manifest.
**Path:** validate manifest → resolve exact dependencies → load model/tokenizer → execute fixture → capture declared sites → validate tensor values → persist artifact → emit observation → replay sample.
**Success:** AC-N0/AC-N1 capture evidence.

## J-006 — Falsify an existing Noesis claim

**Actor:** Independent scorer/reviewer
**Objective:** Attempt to break an existing interpretation or alignment claim.
**Path:** select settlement → reproduce source evidence → define adversarial or null test → execute without changing original evidence → append contradicting/negative evidence → issue independent settlement.
**Success:** invariance or failure is independently documented.
**Invariant:** original evidence remains immutable.

## J-007 — Evaluate latent communication

**Actor:** Authorized research operator
**Objective:** Determine whether a latent channel produces measurable benefit over explicit baselines without overclaiming shared semantics.
**Entry conditions:** N4 accepted; experiment explicitly authorized.
**Path:** text baseline → serialized-vector baseline → latent channel → compression sweep → held-out task tests → latency/information metrics → adversarial controls → semantic-equivalence tests → settlement.
**Success:** AC-N5 evidence packet.

## J-008 — Retire or supersede evidence

**Actor:** Maintainer/operator
**Objective:** Preserve historical evidence while marking it obsolete due to model, method, or research change.
**Path:** identify superseding evidence → verify immutable source → issue supersession record → update status/traceability → retain original artifacts.
**Invariant:** evidence is never rewritten to match newer conclusions.

## J-009 — Test curvature-aware semantic invariance

**Actor:** Representation researcher
**Objective:** Determine whether a registered geometry preserves held-out semantic relations better than a matched Euclidean baseline.
**Entry conditions:** EXP-001 corpus and relational annotations frozen; AC-N0/AC-N1 accepted; geometry profile registered.
**Path:** register candidates and nulls -> validate assumptions -> fit on discovery -> select on selection partition -> freeze -> evaluate confirmation/control partitions -> run diagnostics and ablations -> independently replicate -> settle bounded result.
**Success:** schema-valid `AC-N3-GEO` evidence packet and replication settlement.
**Failure:** confirmation leakage, absent matched baseline, unstable fit, failed assumptions, or no resolvable evidence.
**Invariant:** winning geometry remains scoped evidence and never becomes Noesis ontology.
