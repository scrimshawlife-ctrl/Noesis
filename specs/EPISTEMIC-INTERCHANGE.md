# Zero State Epistemic Interchange Specification

Status: `CANON-SHADOW`
Version: `0.1.0`
Authority: advisory only

## 1. Purpose

Define the minimum research object and conformance gates required before Noesis participates in a multi-repository experiment with Hyperlex, Semion, Trutina, Abraxas, or Noema.

This specification delays ecosystem-wide EXP-001 execution until each participating instrument can preserve epistemic meaning across subsystem boundaries.

## 2. Doctrine

1. Integration readiness is not scientific validation.
2. Schema validity is not epistemic validity.
3. `OBSERVED != INTERPRETED != CALIBRATED != SETTLED`.
4. A receiver MUST NOT silently promote epistemic status.
5. Missing required evidence MUST fail closed as `NOT_COMPUTABLE` or a typed rejection.
6. Every transformation MUST preserve source provenance and append its own provenance.
7. Contradictory and negative evidence are first-class.
8. Round-trip reconstruction MUST recover the original observation, every interpretation/calibration/settlement step, and their authorities.
9. No participant may infer consciousness, hidden intent, universal neuralese, or semantic ground truth from interchange metadata.
10. EXP-001 input freeze remains blocked until ecosystem readiness is explicitly accepted.

## 3. Domain model

### EIC-001 — EpistemicInterchangeObject

A transport envelope containing:
- immutable object identity and schema version;
- proposition/research-object identity;
- current epistemic status;
- source observation references;
- provenance chain;
- declared interpretations;
- transformations;
- uncertainty/calibration records;
- controls and contradictions;
- evidence references;
- authority scope;
- lifecycle and supersession references.

Allowed epistemic statuses:
- `OBSERVED`
- `INTERPRETED`
- `CALIBRATED`
- `SETTLED`
- `NOT_COMPUTABLE`

No status implies the truth of another status.

### EIC-002 — ProvenanceEvent

Records actor/system, repository/component, operation, UTC time, input hashes, output hash, software/model revision when applicable, and authority.

### EIC-003 — EpistemicAssertion

Records an assertion separately from the observation that motivated it. It MUST identify assertion class, authoring component, evidence references, limitations, and status.

## 4. Component qualification

Passing Q1 means only that the component is trustworthy enough to participate in controlled integration testing.

### SEMION-Q1
Semion can emit versioned symbolic/semiotic relations without representing those relations as observed latent-model truth.

### HYPERLEX-Q1
Hyperlex can emit deterministic transformations with source/output hashes, transform identity, declared invariant, expected changed attributes, model/revision provenance, and contamination metadata. It cannot assign latent truth.

### NOESIS-Q1
Noesis can measure a declared invariant without trusting the provider's declaration, preserve negative evidence, and emit `NOT_COMPUTABLE` when evidence is insufficient.

### TRUTINA-Q1
Trutina can attach calibration evidence to an existing claim without rewriting the claim, observation, or evidence lineage. Missing calibration support does not become invented confidence.

### ABRAXAS-Q1
Abraxas can ingest an interchange object while preserving observation, interpretation, calibration, contradiction, and settlement as distinct records. It cannot convert upstream schema validity into governing truth.

### NOEMA-Q1
Noema can emit reproducible experimental observations with world state, agent state, operator intervention, clock/speed mode, and relevant environment provenance sufficient to identify contamination.

## 5. Journeys

### J-EIC-001 — Qualify one instrument
An operator executes a component-specific Q1 suite and obtains a reproducible qualification receipt.

### J-EIC-002 — Verify a pairwise boundary
A producer sends valid and adversarial interchange fixtures to a receiver; the receiver preserves or rejects epistemic meaning deterministically.

### J-EIC-003 — Reconstruct a round trip
An auditor reconstructs the source observation and every subsequent epistemic mutation after the object traverses multiple components.

### J-EIC-004 — Authorize EXP-001 integration
An operator reviews qualification, pairwise, and round-trip evidence and explicitly accepts or defers ecosystem readiness.

## 6. Workflows

### WF-EIC-001 — Register interchange object
Purpose: create an immutable research transport object.
Actors: producing instrument.
Trigger: evidence is exported across a repository boundary.
Preconditions: source evidence exists and is hash-addressable.
Inputs: proposition, observations, provenance, assertions, controls, authority.
Happy path: validate -> hash -> persist -> emit.
Failures: unresolved evidence, missing authority, invalid status transition -> reject.
Terminal states: `REGISTERED`, `NOT_COMPUTABLE`, `REJECTED`.
Invariant: transport cannot strengthen a claim.

### WF-EIC-002 — Component Q1 qualification
Purpose: determine whether one instrument preserves its epistemic boundary.
Actors: component runner, independent reviewer.
Trigger: component requests integration eligibility.
Happy path: run valid fixtures -> run missing/contradictory/contaminated fixtures -> verify outputs -> issue receipt.
Terminal states: `QUALIFIED`, `FAILED`, `NOT_COMPUTABLE`.
Invariant: qualification does not validate a scientific hypothesis.

### WF-EIC-003 — Pairwise conformance
Purpose: test meaning preservation at one boundary.
Actors: producer, receiver, reviewer.
Required fixture classes: valid, missing evidence, contradictory evidence, malformed provenance, unsupported interpretation, stale version, contamination, false invariance declaration.
Happy path: freeze fixtures -> transmit -> validate receiver behavior -> compare semantic diff -> issue receipt.
Invariant: receiver may preserve, bound, or reject; it may not silently promote.

Initial boundaries:
1. Semion -> Hyperlex
2. Hyperlex -> Noesis
3. Noesis -> Trutina
4. Noesis -> Abraxas
5. Trutina -> Abraxas
6. Noema -> Noesis

### WF-EIC-004 — Round-trip provenance
Purpose: prove deterministic reconstruction.
Path: Hyperlex -> Noesis -> Trutina -> Abraxas -> audit reconstruction.
Pass condition: auditor recovers original observations, transformations, assertions, calibration, contradictions, settlement, authority, and hashes without relying on narrative context.
Failure: any lost or silently changed epistemic field fails the gate.

### WF-EIC-005 — Ecosystem readiness settlement
Purpose: authorize or defer integrated research.
Preconditions: all required Q1 receipts; required pairwise receipts; round-trip receipt.
Decision: `ACCEPT | REJECT | DEFER | NOT_COMPUTABLE`.
Side effect on ACCEPT only: EXP-001 input-freeze work may resume.
Invariant: acceptance authorizes integration; it does not accept EXP-001's hypothesis.

## 7. State transitions

```text
UNQUALIFIED
  -> Q1_TESTING
  -> QUALIFIED | FAILED | NOT_COMPUTABLE

QUALIFIED
  -> PAIRWISE_TESTING
  -> CONFORMANT | NONCONFORMANT | NOT_COMPUTABLE

CONFORMANT
  -> ROUND_TRIP_TESTING
  -> RECONSTRUCTABLE | FAILED | NOT_COMPUTABLE

RECONSTRUCTABLE
  -> READINESS_REVIEW
  -> INTEGRATION_ACCEPTED | DEFERRED | REJECTED | NOT_COMPUTABLE
```

No later state may be entered by code existence alone.

## 8. Contract

The canonical transport schema is `contracts/epistemic-interchange-object.schema.json`.

Required invariants:
- immutable identity;
- explicit epistemic status;
- at least one evidence or failure reference;
- append-only provenance;
- assertions separated from observations;
- explicit authority;
- contradictions preserved;
- status transitions auditable.

## 9. Acceptance

### AC-EIC-Q1
Each participating component has a Q1 receipt with fixture hashes, code revision, result hashes, failures, reviewer, and UTC time.

### AC-EIC-P1
Each required pairwise boundary passes all required adversarial fixture classes. Unsupported cases fail explicitly.

### AC-EIC-R1
Round-trip reconstruction recovers all epistemically material information and all content hashes verify.

### AC-EIC-G1
Operator settlement explicitly accepts ecosystem integration. Until then:
- EXP-001 ecosystem execution: `BLOCKED`;
- EXP-001 corpus/transform approval: `DEFERRED`;
- N5: remains `BLOCKED`.

## 10. Traceability

```text
J-EIC-001 -> WF-EIC-002 -> AC-EIC-Q1 -> T-EIC-010
J-EIC-002 -> WF-EIC-003 -> AC-EIC-P1 -> T-EIC-020
J-EIC-003 -> WF-EIC-004 -> AC-EIC-R1 -> T-EIC-030
J-EIC-004 -> WF-EIC-005 -> AC-EIC-G1 -> T-EIC-040
```

## 11. Tasks

### T-EIC-001 — Contract foundation
Implement EIC-001 schema, examples, deterministic canonical hashing, and invalid fixtures.

### T-EIC-010 — Noesis-Q1 first
Implement Noesis qualification runner first because Noesis owns the initial interchange reference implementation.

### T-EIC-011 — Hyperlex-Q1 adapter fixtures
Define deterministic transform fixtures and false-invariance/contamination cases.

### T-EIC-012 — Semion-Q1 fixtures
Define symbolic-relation fixtures that cannot populate latent truth.

### T-EIC-013 — Trutina-Q1 fixtures
Define calibration attachment and missing-support cases.

### T-EIC-014 — Abraxas-Q1 fixtures
Define preservation and anti-promotion cases.

### T-EIC-015 — Noema-Q1 fixtures
Define environment/agent/operator contamination provenance cases.

### T-EIC-020 — Pairwise conformance harness
Execute boundaries independently; no all-system orchestration.

### T-EIC-030 — Round-trip reconstruction harness
Execute only after required pairwise gates pass.

### T-EIC-040 — Readiness settlement
Produce operator review packet and gate receipt.

## 12. Verification

- V-EIC-001: schema valid/invalid fixtures.
- V-EIC-002: canonical hash stability.
- V-EIC-003: epistemic status cannot silently strengthen.
- V-EIC-004: missing evidence -> explicit failure/NOT_COMPUTABLE.
- V-EIC-005: contradiction survives every supported serialization.
- V-EIC-006: provenance is append-only and reconstructable.
- V-EIC-007: stale schema/revision rejected or explicitly migrated.
- V-EIC-008: round-trip semantic diff is empty for required fields.

## 13. Roadmap

### R0 — Contract foundation
Exit: EIC schema + examples + validation tests.

### R1 — Instrument qualification
Order: Noesis -> Hyperlex -> Semion -> Trutina -> Abraxas -> Noema.
Exit: required Q1 receipts.

### R2 — Pairwise conformance
Test only the six declared boundaries.
Exit: AC-EIC-P1.

### R3 — Round-trip provenance
Run Hyperlex -> Noesis -> Trutina -> Abraxas reconstruction.
Exit: AC-EIC-R1.

### R4 — Ecosystem readiness review
Operator decides AC-EIC-G1.

### R5 — Resume EXP-001
Only after AC-EIC-G1 ACCEPT: freeze EXP-001 inputs, execute, falsify, replicate, settle.

## 14. Explicit deferrals

Until AC-EIC-G1:
- no ecosystem-wide EXP-001 run;
- no new Noesis subsystem justified solely for integration;
- no N5 latent communication;
- no automated canon mutation;
- no claim that component interoperability establishes scientific validity.
