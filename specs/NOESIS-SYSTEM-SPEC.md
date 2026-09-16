# NOESIS-SYSTEM-SPEC

Status: `CANON-SHADOW`
Version: `0.3.0`
Specification state: `COMPLETE`
Runtime state: `SLICE-001 + SLICE-002A + SLICE-003 + SLICE-004 + SLICE-005 + SLICE-006 IMPLEMENTED`

This document is the canonical system overview. Normative details are decomposed into the referenced specifications below.

## 1. Doctrine

Noesis is the Abraxas latent-representation research module. It measures, compares, falsifies, aligns, and settles claims about model representations without assuming that latent states form a universal hidden language or a faithful transcript of internal reasoning.

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
- `FR-020–029`: representation metrics, geometry profiles, null controls, and fail-closed assumptions;
- `FR-030–035`: sparse features and probes;
- `FR-040–043`: causal intervention;
- `FR-050–054`: cross-space alignment;
- `FR-060–065`: settlement/evidence;
- `FR-070–074`: reproducibility;
- `FR-080–082`: external boundaries;
- `FR-090–094`: gated latent communication;
- `NFR-*`: reproducibility, auditability, modularity, failure semantics, portability, privacy/security, and storage/performance.

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
- `J-009` curvature-aware semantic invariance.

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
- `WF-011` profile and compare candidate geometries.

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
- `SM-009` geometry-candidate lifecycle.

Capability maturity remains:

`N0 -> N1 -> N2 -> N3 -> N4 -> N5`

No tier advances from code existence alone.

## 7. Contracts

Normative semantics: `specs/CONTRACTS.md`.
Machine-readable JSON Schemas:
- `contracts/experiment-manifest.schema.json`;
- `contracts/observation.schema.json`;
- `contracts/metric-result.schema.json`;
- `contracts/intervention-result.schema.json`;
- `contracts/alignment-map.schema.json`;
- `contracts/settlement.schema.json`;
- `contracts/latent-channel-result.schema.json`;
- `contracts/exp001-source-corpus.schema.json`;
- `contracts/exp001-transform-catalog.schema.json`;
- `contracts/exp001-freeze-receipt.schema.json`.

`FailureRecord` remains semantically specified; its JSON Schema may be added with the first FailureRecord interchange slice. `SupersessionRecord` uses `contracts/supersession.schema.json`.

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
Hyperlexical -> versioned transforms/fixtures -> Noesis -> settlements/evidence -> Abraxas
```

Reference runtime direction is Python with adapter-based access to open-weight transformer models because hidden-state access is required for N1+ experiments.

## 11. Acceptance criteria

Normative gates: `specs/ACCEPTANCE.md`.

- `AC-G0`: specification foundation;
- `AC-N0`: deterministic representation comparison;
- `AC-N1`: hidden-state capture;
- `AC-N2`: feature/probe/intervention lab;
- `AC-N3`: semantic invariance;
- `AC-N3-GEO`: optional curvature-aware semantic-invariance profile;
- `AC-N4`: cross-space alignment;
- `AC-N5`: latent communication;
- `AC-R1`: reproducibility;
- `AC-R2`: independent replication;
- `AC-S1`: security/privacy.

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
- EXP-001 execution;
- optional EXP-001-GEO geometry profiling;
- gated N5 latent channel.

Current gate: operator-approved, hash-bound EXP-001 source corpus and transform/control catalog as defined in `STATUS.md`.

## 14. Verification

Normative verification plan: `specs/VERIFICATION.md`.

Verification covers schema correctness, deterministic unit fixtures, adapter behavior, capture replay, metric correctness, falsification, causal interventions, alignment leakage/nulls, settlement epistemics, security/privacy, traceability, reproducibility, independent replication, and gated N5 channel controls.

CI entry point:

```bash
python scripts/validate_specs.py
```

## Research program

- `specs/EXP-001-SEMANTIC-INVARIANCE.md`: canonical first experiment.
- `specs/EXP-001-GEOMETRY-PROFILE.md`: optional experiment-owned geometry profile.
- `specs/EXP-002-LATENT-COMMUNICATION.md`: fully specified but `BLOCKED` until AC-N4 + operator authorization.
- `docs/RESEARCH.md`: current evidence baseline and limitations.

## Settlement

The specification is complete. AC-N0 and AC-N1 have bounded pinned-model acceptance evidence. Semantic invariance, geometry, alignment, and latent-communication claims remain `NOT_EXECUTED`, `NOT_COMPUTABLE`, or `BLOCKED` as recorded in `STATUS.md`.
