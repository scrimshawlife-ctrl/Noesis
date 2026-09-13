# Noesis Security, Privacy, and Governance

Status: `CANON-SHADOW`
Version: `0.2.0`

## 1. Governance posture

Noesis is a research evidence subsystem. It is `ADVISORY_ONLY` by default. It may recommend, never directly enact, canon promotion or production steering.

## 2. Authority model

### Allowed without additional governance
- local/public research fixtures;
- open-weight model capture under valid license;
- N0-N4 analysis in LAB/RESEARCH environments;
- schema-valid settlement issuance;
- independent replication and falsification.

### Requires explicit operator authorization
- sensitive/private datasets;
- FIELD execution;
- latent communication experiments at N5;
- any intervention intended to change production behavior;
- any external publication claiming mechanistic or semantic findings beyond CANON-SHADOW.

### Prohibited by default
- secret/token persistence;
- unauthorized proprietary data ingestion;
- covert hidden-state collection from users;
- training-data extraction as a project objective;
- direct mutation of Abraxas canon;
- representing correlation as consciousness, intent, or subjective state.

## 3. Threat model

### TM-001 — Provenance spoofing
Threat: incorrect model, tokenizer, fixture, or artifact is presented as canonical evidence.
Controls: content hashes, exact revision fields, immutable manifests, environment fingerprints, schema validation.

### TM-002 — Data leakage
Threat: sensitive prompts, credentials, proprietary data, or private user content becomes embedded in fixtures/artifacts.
Controls: classification gate, secret scanning, fixture review, minimization, retention/deletion policy, PROHIBITED class.

### TM-003 — Interpretability overclaim
Threat: natural-language feature explanations are mistaken for latent ground truth.
Controls: hypothesis typing, falsification workflow, causal-evidence distinction, provenance labels, CANON-SHADOW default.

### TM-004 — Train/test contamination
Threat: held-out data influences feature/alignment fitting or threshold selection.
Controls: immutable partition hashes, manifest preregistration, separate train/validation/test roles, audit trail.

### TM-005 — Cherry-picking
Threat: negative, contradictory, or failed results disappear from the evidence narrative.
Controls: first-class failure records, evidence-relation typing, settlement requirement to preserve contradictions.

### TM-006 — Artifact substitution
Threat: tensor/model/map artifact changes after measurement.
Controls: content-addressed storage, hash verification before analysis and settlement.

### TM-007 — Cross-model semantic overreach
Threat: geometric alignment is described as semantic equivalence.
Controls: separate alignment and semantic claims, held-out and shift tests, explicit null baselines.

### TM-008 — Latent-channel covert transfer
Threat: a latent channel carries unintended/private information beyond the declared task.
Controls: N5 authorization gate, information-budget measurement, adversarial probes, channel logging by hash/metadata, baseline comparison, restricted fixtures.

### TM-009 — Intervention misuse
Threat: causal/steering tooling becomes an uncontrolled production manipulation mechanism.
Controls: LAB/RESEARCH default, explicit authorization for FIELD, adapter capability boundary, no automatic deployment path.

### TM-010 — Dependency drift
Threat: model/library changes make reruns incomparable while appearing equivalent.
Controls: environment fingerprint, exact dependency lock where practical, new run identity for material changes.

## 4. Privacy model

- Default to public/synthetic/research-approved fixtures.
- Store only the minimum raw text required for reproducibility.
- Prefer hashes/references when full content is not required.
- Sensitive fixture use requires purpose, legal/organizational authorization, retention duration, deletion method, and access scope.
- Do not claim that latent artifacts are anonymous merely because they are vectors.
- Any experiment designed to test memorization/privacy leakage requires separate explicit authorization and containment.

## 5. Environment classes

### LAB
Synthetic/public fixtures; unrestricted local experimentation within repo doctrine.

### RESEARCH
Curated datasets and formal experiments; stronger audit, retention, and replication requirements.

### FIELD
Real-world/production/user-linked execution. `BLOCKED` until a separate governance decision authorizes exact scope.

## 6. Promotion governance

Promotion recommendation levels:
- `KEEP_SHADOW`
- `REPLICATE`
- `RESEARCH_CANDIDATE`
- `PROMOTION_ELIGIBLE`
- `REJECT`

Noesis may output these recommendations. External Abraxas governance owns any actual canonical transition.

Minimum evidence for `PROMOTION_ELIGIBLE`:
1. preregistered claim;
2. reproducible evidence;
3. relevant null/negative controls;
4. contradictory evidence accounted for;
5. independent replication;
6. no unresolved critical provenance/security defects;
7. causal evidence when a causal/mechanistic claim is made.

## 7. Audit requirements

Audit records SHALL include:
- actor/producer;
- action;
- object IDs/hashes;
- UTC time;
- source and resulting lifecycle states;
- reason for supersession/correction;
- authorization reference when required.

## 8. Incident rules

If evidence corruption, leakage, or provenance defect is discovered:
1. stop promotion/use of affected settlement;
2. preserve affected artifacts for forensic review unless privacy policy requires secure deletion;
3. issue defect/supersession record;
4. identify downstream settlements;
5. rerun only under a new run identity;
6. document whether prior claims remain valid, weakened, rejected, or NOT_COMPUTABLE.