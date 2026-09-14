# NOESIS-SYSTEM-SPEC

Status: `CANON-SHADOW`
Version: `0.2.1`
Specification state: `COMPLETE`
Runtime state: `IMPLEMENTED / EVIDENCE-GATED`

This document is the canonical system overview. Normative details are decomposed into the referenced specifications below.

## 1. Doctrine

Noesis is the Abraxas latent-representation research module. It measures, compares, falsifies, aligns, and settles claims about model representations without assuming that latent states form a universal hidden language or a faithful transcript of internal reasoning.

Noesis is an experimental instrument, not a scientific theory. It provides reusable operations for observing, comparing, perturbing, aligning, and settling evidence about model representations. The existence of a Noesis capability does not assert that the phenomenon being measured exists.

Examples:

```text
Noesis can measure invariance
!= semantic invariance exists

Noesis can align spaces
!= the spaces share meaning

Noesis can inspect features
!= features correspond to human concepts

Noesis can transmit latent states
!= models share a universal latent language
```

### Invariants

- Evidence precedes interpretation.
- `OBSERVED` is distinct from `INFERRED`, `SPECULATIVE`, and `NOT_COMPUTABLE`.
- Correlation is not causal evidence.
- Natural-language feature descriptions are hypotheses, not latent ground truth.
- Missing or weak signal yields `NOT_COMPUTABLE` or an explicitly inconclusive settlement.
- Negative, failed, contradictory, and null evidence is first-class.
- Noesis is `ADVISORY_ONLY`; it cannot mutate Abraxas canon.
- Hyperlexical owns lexical/symbolic transformation, not latent truth.
- Latent communication is blocked until AC-N4 plus explicit operator authorization.
- Research hypotheses, semantic ontologies, transform taxonomies, and expected invariants are experiment inputs, not Noesis core truth.
- A rejected hypothesis does not invalidate the measurement apparatus unless it exposes an instrument defect.

Primary doctrine: `CONSTITUTION.md`.

## 2. Domain model

Core entities:

`ModelIdentity`, `RepresentationSite`, `InputFixture`, `Transform`, `ExperimentManifest`, `Run`, `Observation`, `FeatureDictionary`, `FeatureHypothesis`, `Probe`, `MetricResult`, `InterventionResult`, `AlignmentMap`, `EvidenceBundle`, `Settlement`, `FailureRecord`, `SupersessionRecord`, `LatentChannelResult`.

Primary relationship:

`ExperimentManifest -> Run -> Observation -> Metric/Feature/Intervention/Alignment evidence -> EvidenceBundle -> Settlement`

Normative model: `specs/DATA-MODEL.md`.

## 3. Requirements

The complete normative requirement catalog is `specs/REQUIREMENTS.md`.

Requirement families:
- `FR-001–005`: capture and identity;
- `FR-010–013`: controlled transforms and fixtures;
- `FR-020–025`: representation metrics and null controls;
- `FR-030–035`: sparse features and probes;
- `FR-040–043`: causal intervention;
- `FR-050–054`: cross-space alignment;
- `FR-060–065`: settlement/evidence;
- `FR-070–074`: reproducibility;
- `FR-080–082`: external boundaries;
- `FR-083–088`: research neutrality and ontology isolation;
- `FR-090–094`: gated latent communication;
- `NFR-*`: reproducibility, auditability, modularity, hypothesis neutrality, failure semantics, portability, privacy/security, and storage/performance.

## 4. Journeys

Normative actor journeys are defined in `specs/JOURNEYS.md`:
- `J-001` semantic invariance;
- `J-002` candidate feature evaluation;
- `J-003` cross-space alignment;
- `J-004` Abraxas evidence consumption;
- `J-005` reproducible capture;
- `J-006` independent falsification;
- `J-007` latent communication;
- `J-008` evidence supersession.

Journeys are research consumers of Noesis capabilities; no journey defines core truth.

## 5. Workflows

Normative workflows are defined in `specs/WORKFLOWS.md`:
- `WF-001` register experiment;
- `WF-002` capture representations;
- `WF-003` compare representations;
- `WF-004` evaluate sparse feature/probe;
- `WF-005` fit alignment;
- `WF-006` causal intervention;
- `WF-007` settle evidence;
- `WF-008` independent replication/falsification;
- `WF-009` supersede evidence;
- `WF-010` latent communication experiment.

Each workflow defines purpose, actors, trigger, preconditions, inputs, deterministic path, alternatives, failure/recovery, state transitions, terminal states, side effects, invariants, permissions, observability, acceptance, dependencies, and unresolved items.

## 6. State machines

Normative state machines are `specs/STATE-MACHINES.md`:
- `SM-001` experiment lifecycle;
- `SM-002` observation lifecycle;
- `SM-003` candidate feature lifecycle;
- `SM-004` alignment lifecycle;
- `SM-005` settlement lifecycle;
- `SM-006` capability maturity;
- `SM-007` evidence classification;
- `SM-008` latent-channel lifecycle.

Capability maturity remains:

`N0 -> N1 -> N2 -> N3 -> N4 -> N5`

No tier advances from code existence alone.

## 7. Contracts

Normative semantics: `specs/CONTRACTS.md`.

Contracts are layered as:
- core research-neutral evidence contracts;
- integration contracts for external systems/adapters;
- research contracts for experiment-specific hypotheses and ontologies.

Research contracts may evolve or disappear without redefining core Noesis evidence semantics.

## 8. Data model

Normative data ownership, lineage, artifact storage, identity rules, relationships, and retention classes are in `specs/DATA-MODEL.md`.

Large tensors and model-derived artifacts are content-addressed and separated from transactional metadata. Evidence objects are immutable after issuance.

## 9. Security, privacy, governance

Normative policy and threat model: `specs/SECURITY-GOVERNANCE.md`.

Key posture:
- default environments: LAB/RESEARCH;
- FIELD: blocked pending explicit governance;
- sensitive data: explicit classification/retention/access scope required;
- N5: explicit authorization required;
- production steering: outside default authority;
- Noesis cannot directly promote Abraxas canon.

## 10. Architecture

Normative architecture: `ARCHITECTURE.md`.

Boundary:

```text
Research Programs -> versioned manifests/contracts -> Noesis Core -> settlements/evidence -> Abraxas
Hyperlexical -> versioned transforms/fixtures -> Noesis Core
```

Canonical dependency direction is `Noesis Core <- Integrations <- Research Programs`. Noesis core must not depend on EXP-001, semantic-invariance theory, Hyperlex ontology, or funding/research-program framing.

Reference runtime direction is Python with adapter-based access to open-weight transformer models because hidden-state access is required for N1+ experiments.

## 11. Acceptance criteria

Normative gates: `specs/ACCEPTANCE.md`.

- `AC-G0`: specification foundation;
- `AC-N0`: deterministic representation comparison;
- `AC-N1`: hidden-state capture;
- `AC-N2`: feature/probe/intervention lab;
- `AC-N3`: semantic invariance;
- `AC-N4`: cross-space alignment;
- `AC-N5`: latent communication;
- `AC-R1`: reproducibility;
- `AC-R2`: independent replication;
- `AC-S1`: security/privacy.

Acceptance of a Noesis capability demonstrates that the measurement capability functions as specified. It does not constitute acceptance of every scientific hypothesis that uses that capability.

## 12. Traceability

Canonical end-to-end mapping: `TRACEABILITY.md`.

Required chain:

`Journey -> Workflow -> State Transition -> Contract -> Acceptance Test -> Implementation Task -> Verification`

Every implementation PR must identify affected IDs and unresolved `NOT_COMPUTABLE` items.

## 13. Implementation task families

Normative task graph: `specs/TASKS.md`.

Major groups:
- foundation/domain/contracts;
- runtime adapters and deterministic capture;
- metric engine;
- Hyperlexical boundary;
- SAE/probe/falsification;
- causal intervention;
- alignment;
- settlement/replication/security;
- experiment execution;
- gated N5 latent channel.

Research-program packages depend on Noesis core; Noesis core does not depend on research-program packages.

## 14. Verification

Normative verification plan: `specs/VERIFICATION.md`.

Verification covers schema correctness, deterministic unit fixtures, adapter behavior, capture replay, metric correctness, falsification, causal interventions, alignment leakage/nulls, settlement epistemics, security/privacy, traceability, reproducibility, independent replication, gated N5 channel controls, hypothesis-neutrality, and ontology leakage.

CI entry point:

```bash
python scripts/validate_specs.py
```

## Research program

- `specs/EXP-001-SEMANTIC-INVARIANCE.md`: one research consumer of Noesis capabilities, not core doctrine.
- `specs/EXP-002-LATENT-COMMUNICATION.md`: fully specified but `BLOCKED` until AC-N4 + operator authorization.
- `docs/RESEARCH.md`: current evidence baseline and limitations.

## Settlement

Noesis is specified as a hypothesis-neutral research instrument. Runtime and research programs may test competing theories without changing core evidence semantics. Scientific results remain governed by their declared acceptance, reproducibility, and settlement requirements.
