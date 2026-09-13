# Noesis Workflows

Status: `CANON-SHADOW`
Version: `0.2.0`

Every meaningful workflow defines purpose, actors, trigger, preconditions, inputs, deterministic path, alternates, failures, state transitions, terminal states, side effects, invariants, permissions, observability, acceptance, dependencies, and unresolved items.

## WF-001 — Register experiment

**Purpose:** Freeze an executable research question before collection.
**Actors:** Researcher, spec agent.
**Trigger:** New approved research question.
**Preconditions:** model/data rights known; hypothesis and metrics explicit.
**Inputs:** hypotheses, fixtures, transforms, models, representation sites, metrics, seeds, thresholds, environment requirements.
**Happy path:**
1. Validate `ExperimentManifest`.
2. Resolve and hash fixtures/transforms.
3. Record model/tokenizer revisions and environment fingerprint.
4. Freeze hypotheses, nulls, metrics, and acceptance thresholds.
5. Assign experiment ID and manifest hash.
6. Persist immutable manifest.
**Alternate paths:** unsupported representation site -> mark manifest `NOT_READY`; unavailable model revision -> `NOT_READY`.
**Failure/recovery:** malformed provenance -> reject; any material change after registration creates a new manifest revision and experiment run.
**State:** `DRAFT -> REGISTERED` or `DRAFT -> NOT_READY`.
**Terminal states:** `REGISTERED`, `NOT_READY`.
**Side effects:** immutable manifest only.
**Invariants:** no data collection counts toward preregistered evidence before registration.
**Permissions:** researcher may draft; operator policy may require approval for sensitive or N5 experiments.
**Observability:** manifest hash, creator, timestamp, schema version.
**Acceptance:** manifest validates and all required hashes resolve.
**Dependencies:** contract schemas, model registry.
**Unresolved:** none for N0-N4.

## WF-002 — Capture representations

**Purpose:** Produce immutable latent observations.
**Actors:** Capture runner.
**Trigger:** Registered manifest enters execution.
**Preconditions:** `REGISTERED`; adapter declares support for requested site.
**Inputs:** manifest, fixture, exact model/tokenizer revisions.
**Happy path:**
1. Resolve exact dependencies.
2. Seed deterministic libraries where applicable.
3. Execute fixture.
4. Capture declared tensor sites only.
5. Validate shape, dtype, finite values, and expected token alignment metadata.
6. Persist content-addressed tensor artifact.
7. Emit schema-valid `Observation`.
**Alternate:** embedding-only run where hidden state unavailable and manifest allows it.
**Failures:** OOM, unsupported hook, missing revision, NaN/Inf, artifact write failure.
**Recovery:** failure is recorded; rerun under new run ID after environment change.
**State:** `REGISTERED/RUNNING -> CAPTURED | CAPTURE_FAILED`.
**Terminal:** per-fixture `CAPTURED`, `CAPTURE_FAILED`.
**Side effects:** artifact + observation/failure record.
**Invariants:** failure cannot become absent data; undeclared sites cannot be captured silently.
**Permissions:** adapter runtime only.
**Observability:** run ID, environment fingerprint, duration, peak resource class, failure code.
**Acceptance:** AC-N0/AC-N1 capture checks.

## WF-003 — Compare representations

**Purpose:** Produce deterministic metric results.
**Actors:** Analysis runner.
**Trigger:** Compatible observations available.
**Preconditions:** metric prerequisites satisfied.
**Inputs:** observation IDs, metric configuration, null/control configuration.
**Happy path:** validate compatibility -> apply declared preprocessing -> compute primary metric -> compute null/control metrics -> uncertainty estimate if applicable -> persist `MetricResult`.
**Alternate:** metric skipped if preregistered precondition fails.
**Failures:** dimensional mismatch, insufficient samples, invalid numeric state.
**Recovery:** emit `NOT_COMPUTABLE`; do not coerce.
**State:** `CAPTURED -> MEASURED | NOT_COMPUTABLE`.
**Terminal:** `MEASURED`, `NOT_COMPUTABLE`.
**Invariant:** preprocessing must be part of metric identity.
**Acceptance:** deterministic fixture and null-control tests pass.

## WF-004 — Evaluate sparse feature or learned probe

**Purpose:** Determine whether an interpretation survives contamination and causal tests.
**Actors:** Interpretability researcher, independent reviewer.
**Trigger:** candidate feature/probe identified.
**Preconditions:** source dictionary/probe artifact and source observations versioned.
**Inputs:** candidate ID, interpretation hypothesis, positive/negative controls, lexical triggers, run-consistency evidence, optional intervention design.
**Happy path:**
1. Verify dictionary reconstruction/sparsity/dead-feature metrics.
2. Measure feature stability across independent training runs where applicable.
3. Record natural-language interpretation as hypothesis.
4. Execute lexical-trigger positive and negative controls.
5. Execute semantic-positive examples without target lexical cues.
6. Execute non-semantic confound controls.
7. Evaluate held-out data/distribution shift.
8. Run causal intervention if claim is mechanistic.
9. Record all contradictions.
10. Emit bounded settlement.
**Alternate:** no causal access -> semantic correlation claim remains bounded.
**Failures:** leakage, control failure, unstable feature, dictionary mismatch.
**Recovery:** `REJECTED`, `WEAK`, or `INCONCLUSIVE`; never relabel after seeing controls without new hypothesis ID.
**State:** `DISCOVERED -> CONTROL_TESTED -> FALSIFICATION_TESTED -> CAUSAL_TESTED? -> REPLICATED? -> SETTLED`.
**Invariant:** accuracy/activation correlation alone is not mechanistic evidence.
**Acceptance:** AC-N2.

## WF-005 — Fit cross-model or cross-layer alignment

**Purpose:** Test transferable geometry without assuming semantic identity.
**Actors:** Researcher.
**Trigger:** paired representation dataset available.
**Preconditions:** registered split and mapping family.
**Inputs:** paired observations, train/validation/test split, alignment algorithm, baselines.
**Happy path:** fit on train -> select on validation -> freeze map -> evaluate held-out metrics -> compare shuffled/random nulls -> evaluate neighborhood preservation -> evaluate at least one distribution shift -> persist `AlignmentMap` and metric bundle.
**Failures:** overfit, no null improvement, incompatible dimensionality without registered projection.
**Recovery:** `WEAK`, `REJECTED`, or `NOT_COMPUTABLE`.
**State:** `UNFIT -> FIT -> VALIDATED -> HELD_OUT_TESTED -> SETTLED`.
**Invariant:** test data cannot influence fitting or hyperparameter selection.
**Acceptance:** AC-N4.

## WF-006 — Run causal intervention

**Purpose:** Estimate whether a representation/component functionally affects declared behavior.
**Actors:** Researcher.
**Trigger:** registered causal hypothesis.
**Preconditions:** supported intervention access; control condition defined.
**Inputs:** source/target site, intervention operation, magnitude, fixtures, outcome metrics, controls.
**Happy path:** execute baseline -> intervention -> matched control -> quantify effect and uncertainty -> robustness sweep where specified -> persist `InterventionResult`.
**Failures:** model instability, target mismatch, intervention changes unrelated variables beyond declared tolerance.
**Recovery:** record failure or inconclusive result; never discard null effects.
**State:** `PLANNED -> EXECUTED -> MEASURED -> SETTLED`.
**Invariant:** steering effectiveness and semantic interpretation are separate claims.

## WF-007 — Settle evidence

**Purpose:** Create durable epistemic output.
**Actors:** Settlement engine/operator reviewer.
**Trigger:** analysis bundle complete or experiment terminates.
**Preconditions:** evidence references resolvable or explicitly recorded unavailable.
**Inputs:** proposition, evidence bundle, contradictions, controls, limitations.
**Happy path:** validate evidence -> separate observation/inference -> classify supporting/contradicting/control/negative evidence -> check acceptance rule -> assign `OBSERVED`, `INFERRED`, `SPECULATIVE`, or `NOT_COMPUTABLE` -> record limitations/confidence basis -> emit immutable settlement.
**Failures:** missing required evidence -> `NOT_COMPUTABLE`; contradictory evidence prevents requested claim strength -> downgrade/reject.
**State:** `ANALYZED -> SETTLED | INCONCLUSIVE`.
**Invariant:** unsupported fields are never synthesized.
**Side effects:** advisory evidence only.

## WF-008 — Independent replication / falsification

**Purpose:** Challenge an existing result without mutating it.
**Actors:** Independent scorer/researcher.
**Trigger:** promotion-worthy or contested settlement.
**Preconditions:** original manifest/evidence available.
**Inputs:** settlement ID, original evidence, independent controls or rerun plan.
**Happy path:** reproduce source result -> run independent controls -> compare result envelopes -> issue independent settlement -> link as replication/supersession evidence.
**Failure:** exact dependency unavailable -> document partial replication limits.
**Invariant:** original settlement remains immutable.
**Acceptance:** required before claims leave CANON-SHADOW.

## WF-009 — Supersede evidence

**Purpose:** Mark older evidence as outdated without deletion.
**Actors:** Maintainer/operator.
**Trigger:** stronger evidence, invalidated method, revoked model artifact, or discovered defect.
**Preconditions:** replacement or invalidation evidence exists.
**Happy path:** identify source settlement -> record reason -> reference superseding settlement/defect -> mark lifecycle metadata -> preserve original artifact.
**Invariant:** supersession changes status, not history.

## WF-010 — Execute latent communication experiment

**Purpose:** Evaluate machine-native latent channel utility after alignment maturity.
**Actors:** Authorized research operator.
**Trigger:** explicit N5 experiment approval.
**Preconditions:** AC-N4 accepted; sender/receiver identity fixed; channel contract and baselines registered.
**Inputs:** sender/receiver, channel representation, compression budget, tasks, text baseline, serialized-vector baseline, attack/control suite.
**Happy path:** run baselines -> latent channel -> compression sweep -> held-out tasks -> task/latency/information metrics -> distribution/adversarial controls -> semantic-equivalence tests -> emit `LatentChannelResult` + settlement.
**Failures:** channel incompatibility, no baseline advantage, leakage, semantic mismatch.
**Recovery:** reject or constrain claim.
**State:** `AUTHORIZED -> BASELINED -> LATENT_TESTED -> CONTROL_TESTED -> SETTLED`.
**Invariant:** task utility never proves universal neuralese.
**Acceptance:** AC-N5.
