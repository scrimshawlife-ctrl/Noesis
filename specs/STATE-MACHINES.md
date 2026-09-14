# Noesis State Machines

Status: `CANON-SHADOW`
Version: `0.2.0`

## SM-001 — Experiment lifecycle

States:
- `DRAFT`
- `NOT_READY`
- `REGISTERED`
- `AUTHORIZED` (only where policy requires)
- `RUNNING`
- `ANALYZED`
- `INCONCLUSIVE`
- `SETTLED`
- `FAILED`
- `SUPERSEDED`

Allowed transitions:
- `DRAFT -> REGISTERED`
- `DRAFT -> NOT_READY`
- `NOT_READY -> DRAFT`
- `REGISTERED -> AUTHORIZED` when explicit authorization is required
- `REGISTERED -> RUNNING` when no additional authorization is required
- `AUTHORIZED -> RUNNING`
- `RUNNING -> ANALYZED`
- `RUNNING -> FAILED`
- `ANALYZED -> SETTLED`
- `ANALYZED -> INCONCLUSIVE`
- `INCONCLUSIVE -> SUPERSEDED`
- `SETTLED -> SUPERSEDED`

Forbidden:
- `DRAFT -> RUNNING`
- `FAILED -> SETTLED` without a new run/evidence path
- `SUPERSEDED -> SETTLED`

## SM-002 — Observation lifecycle

`PLANNED -> CAPTURED -> VALIDATED -> BUNDLED`

Exceptional:
- `PLANNED -> CAPTURE_FAILED`
- `CAPTURED -> INVALID`

Observations are immutable after `CAPTURED`; validation can only change lifecycle metadata, not content.

## SM-003 — Candidate feature lifecycle

`DISCOVERED -> DESCRIBED -> CONTROL_TESTED -> FALSIFICATION_TESTED -> CAUSAL_TESTED -> REPLICATED -> PROMOTION_ELIGIBLE`

Optional skips:
- `FALSIFICATION_TESTED -> REPLICATED` only for non-causal descriptive claims.

Terminal alternatives from any evaluative state:
- `REJECTED`
- `INCONCLUSIVE`
- `SUPERSEDED`

Constraint: `PROMOTION_ELIGIBLE` does not mean promoted; external governance decides promotion.

## SM-004 — Alignment lifecycle

`PROPOSED -> FIT -> VALIDATED -> HELD_OUT_TESTED -> SHIFT_TESTED -> SETTLED`

Exceptional:
- any pre-settlement state -> `REJECTED`
- any state -> `INVALIDATED` if leakage or methodological defect is discovered

Constraint: test partition access before map freezing invalidates the run.

## SM-005 — Settlement lifecycle

`DRAFT -> VALIDATED -> ISSUED -> REPLICATED? -> SUPERSEDED?`

Settlement epistemic labels are orthogonal to lifecycle state:
- `OBSERVED`
- `INFERRED`
- `SPECULATIVE`
- `NOT_COMPUTABLE`

Issued settlement content is immutable. Supersession is represented by a new record.

## SM-006 — Capability maturity

`N0 -> N1 -> N2 -> N3 -> N4 -> N5`

- `N0`: deterministic representation comparison
- `N1`: hidden-state capture
- `N2`: feature/probe/intervention lab
- `N3`: semantic invariance evidence
- `N4`: held-out cross-space alignment
- `N5`: latent communication research

Advancement requires acceptance evidence for the current tier. Implementation presence alone cannot advance state.

## SM-007 — Evidence classification

Evidence relation to a proposition:
- `UNCLASSIFIED -> SUPPORTING`
- `UNCLASSIFIED -> CONTRADICTING`
- `UNCLASSIFIED -> CONTROL`
- `UNCLASSIFIED -> NEGATIVE_RESULT`

Classification may be corrected only through an audit record; original evidence bytes remain unchanged.

## SM-008 — Latent channel experiment

`BLOCKED -> ELIGIBLE -> AUTHORIZED -> BASELINED -> LATENT_TESTED -> CONTROL_TESTED -> SETTLED`

Transitions:
- `BLOCKED -> ELIGIBLE` only after AC-N4 acceptance.
- `ELIGIBLE -> AUTHORIZED` only by explicit operator approval.
- Any execution state may terminate in `REJECTED`, `FAILED`, or `INCONCLUSIVE`.

Invariant: a successful task result does not transition any semantic-equivalence claim automatically.

## SM-009 — Geometry candidate lifecycle

`PROPOSED -> REGISTERED -> ASSUMPTIONS_VALIDATED -> FIT -> FROZEN -> CONFIRMATION_TESTED -> DIAGNOSTIC_TESTED -> SETTLED`

Terminal alternatives:
- `REJECTED`
- `INCONCLUSIVE`
- `NOT_COMPUTABLE`
- `INVALID`

Constraints:
- accessing confirmation labels before `FROZEN` invalidates the run;
- failure of candidate assumptions cannot trigger silent substitution;
- `SETTLED` geometry remains scoped to the registered experiment and does not become core ontology.
