# Noesis Traceability

Status: `CANON-SHADOW`
Version: `0.2.1`

Traceability follows:

`Journey -> Workflow -> State Transition -> Contract -> Acceptance Test -> Implementation Task -> Verification`

## 1. Functional requirement traceability

| Requirement family | Journeys | Workflows | Contracts | Acceptance | Tasks | Verification |
|---|---|---|---|---|---|---|
| FR-001–005 capture/identity | J-001/J-005 | WF-001/WF-002 | C-001/C-002/C-008 | AC-N0/AC-N1 | T-010/T-020/T-021/T-030 | V-002/V-003/V-004 |
| FR-010–013 transforms/fixtures | J-001 | WF-001/WF-003 | C-001/C-002/C-010/C-011 | AC-N3 | T-050/T-100 | V-002/V-006/V-015 |
| FR-020–025 metrics | J-001/J-003 | WF-003/WF-005 | C-003 | AC-N0/AC-N3/AC-N4 | T-040/T-080 | V-005/V-008 |
| FR-030–035 sparse features/probes | J-002/J-006 | WF-004/WF-008 | C-003/C-006 | AC-N2/AC-R2 | T-060/T-061/T-062/T-110 | V-006/V-013 |
| FR-040–043 causal intervention | J-002/J-006 | WF-006/WF-008 | C-004/C-006 | AC-N2/AC-R2 | T-070/T-110 | V-007/V-013 |
| FR-050–054 alignment | J-003/J-006 | WF-005/WF-008 | C-005/C-003/C-006 | AC-N4/AC-R2 | T-080/T-110 | V-008/V-013 |
| FR-060–065 settlement/evidence | J-004/J-006/J-008 | WF-007/WF-008/WF-009 | C-006/C-008/C-009 | AC-G0/AC-R2 | T-010/T-090/T-110 | V-001/V-009/V-011/V-013 |
| FR-070–074 reproducibility | J-005/J-006 | WF-001/WF-002/WF-008 | C-001/C-002/C-008 | AC-R1 | T-030/T-110 | V-004/V-012 |
| FR-080–082 external boundaries | J-001/J-004 | WF-001/WF-007 | integration contracts | AC-G0 | T-020/T-050/T-090 | V-009/V-011/V-016 |
| FR-083–088 research neutrality | all research journeys | all evidence workflows | core/integration/research contract layering | AC-G0 | architecture review + affected task | V-015/V-016 |
| FR-090–094 latent communication | J-007 | WF-010 | C-007/C-005/C-006 | AC-N5 | T-200/T-210 | V-014 |

## 2. Non-functional traceability

| Requirement family | Primary controls | Acceptance | Tasks | Verification |
|---|---|---|---|---|
| NFR-001–003 reproducibility/determinism | manifests, fingerprints, hashes, numeric tolerances | AC-N0/AC-R1 | T-010/T-030/T-040 | V-002/V-004/V-005/V-012 |
| NFR-010–012 auditability | immutable evidence lineage, contradiction preservation | AC-G0/AC-R2 | T-090/T-110/T-120 | V-009/V-011/V-013 |
| NFR-020–022 modularity | adapter/metric/transform boundaries | AC-G0 | T-010/T-020/T-050 | V-003/V-011 |
| NFR-023–025 hypothesis neutrality | dependency inversion, ontology isolation, theory/instrument separation | AC-G0 | architecture review + affected task | V-015/V-016 |
| NFR-030–032 failure semantics | FailureRecord, NOT_COMPUTABLE, finite checks | AC-N0/AC-N1 | T-030/T-090 | V-003/V-004/V-009 |
| NFR-040–042 portability | Python/open-weight reference runtime, vendor-neutral contracts | AC-N1 | T-020/T-021 | V-003 |
| NFR-050–053 privacy/security | classification, authorization, retention, FIELD/N5 gate | AC-S1 | T-120 | V-010 |
| NFR-060–061 performance/storage | artifact references, content-addressed tensor storage | AC-N0 | T-010/T-030 | V-004 |

## 3. Journey traceability

| Journey | Objective | Workflow chain | Terminal evidence |
|---|---|---|---|
| J-001 semantic invariance | test representation stability across surface variation | WF-001 -> WF-002 -> WF-003 -> WF-004? -> WF-007 | EXP-001 Settlement / AC-N3 |
| J-002 candidate feature | determine whether feature tracks hypothesized property | WF-004 -> WF-006? -> WF-007 | AC-N2 Settlement |
| J-003 alignment | test useful cross-space map | WF-001 -> WF-002 -> WF-005 -> WF-007 | AlignmentMap + AC-N4 |
| J-004 Abraxas consumption | consume advisory evidence without authority transfer | WF-007 | schema-valid Settlement |
| J-005 capture | produce replayable latent observations | WF-001 -> WF-002 | Observation + AC-N0/N1 |
| J-006 falsification | independently challenge claim | WF-008 -> WF-007 | replication settlement / AC-R2 |
| J-007 latent communication | evaluate latent channel utility | WF-010 -> WF-007 | LatentChannelResult + AC-N5 |
| J-008 supersession | retire obsolete evidence without deletion | WF-009 | SupersessionRecord |

Journeys are research consumers. No journey or experiment-specific objective is permitted to become an implicit core dependency.

## 4. State-machine traceability

| State machine | Workflows | Contracts | Verification |
|---|---|---|---|
| SM-001 Experiment lifecycle | WF-001/WF-002/WF-007/WF-009 | C-001/C-006/C-009 | V-004/V-009 |
| SM-002 Observation lifecycle | WF-002 | C-002/C-008 | V-003/V-004 |
| SM-003 Candidate feature lifecycle | WF-004/WF-006/WF-008 | C-003/C-004/C-006 | V-006/V-007/V-013 |
| SM-004 Alignment lifecycle | WF-005 | C-005 | V-008 |
| SM-005 Settlement lifecycle | WF-007/WF-009 | C-006/C-009 | V-009 |
| SM-006 Capability maturity | all | gate settlements | V-011/V-015 |
| SM-007 Evidence classification | WF-007 | C-006 | V-009 |
| SM-008 Latent channel | WF-010 | C-007 | V-014 |

## 5. Contract traceability

| Contract | Layer | Schema | Produced by | Consumed by |
|---|---|---|---|---|
| C-001 ExperimentManifest | core | `contracts/experiment-manifest.schema.json` | WF-001 | evidence workflows |
| C-002 Observation | core | `contracts/observation.schema.json` | WF-002 | comparison/analysis workflows |
| C-003 MetricResult | core | `contracts/metric-result.schema.json` | measurement workflows | WF-007 |
| C-004 InterventionResult | core | `contracts/intervention-result.schema.json` | WF-006 | WF-007/008 |
| C-005 AlignmentMap | core | `contracts/alignment-map.schema.json` | WF-005 | WF-007/WF-010 |
| C-006 Settlement | core | `contracts/settlement.schema.json` | WF-007/WF-008 | Abraxas/operator/governance |
| C-007 LatentChannelResult | core | `contracts/latent-channel-result.schema.json` | WF-010 | WF-007 |
| C-008 FailureRecord | core | semantic contract | failure-producing workflows | audit/replay |
| C-009 SupersessionRecord | core | semantic contract | WF-009 | audit/governance |
| C-010 HyperlexTransformRequest | integration | `contracts/hyperlex-transform-request.schema.json` | research program | Hyperlex adapter |
| C-011 HyperlexTransformResult | integration | `contracts/hyperlex-transform-result.schema.json` | Hyperlex adapter | fixture materialization |
| C-012 EXP001SourceCorpus | research | `contracts/exp001-source-corpus.schema.json` | EXP-001 operator | EXP-001 compiler |
| C-013 N01AcceptanceEvidence | core capability evidence | `contracts/n01-acceptance-evidence.schema.json` | N0/N1 acceptance runner | gate review |
| C-014 EXP001TransformCatalog | research | `contracts/exp001-transform-catalog.schema.json` | EXP-001 operator | EXP-001 compiler |

## 6. Experiment traceability

### EXP-001 — Semantic Invariance
- Classification: research consumer; not core doctrine.
- Journeys: J-001, J-002, J-004, J-005, J-006.
- Workflows: WF-001, WF-002, WF-003, WF-004, WF-006 where applicable, WF-007, WF-008 for replication.
- Requirements: core measurement requirements plus experiment-owned research contracts.
- Gates: AC-N0, AC-N1, AC-N2, AC-N3, AC-R1; AC-R2 before promotion eligibility.
- Verification: V-001 through V-016 as applicable.
- Falsification of EXP-001 does not invalidate core observations or theory-independent metrics.

### EXP-002 — Latent Communication
- Status: `BLOCKED`.
- Classification: research consumer; not core doctrine.
- Entry: accepted AC-N4 + explicit operator authorization.
- Journey: J-007.
- Workflow: WF-010 + WF-007.
- Requirements: FR-050–054, FR-060–094, relevant NFRs.
- Contracts: core channel/alignment/settlement contracts plus experiment-owned task definitions.
- Verification: V-014 plus V-009/V-010/V-011/V-015/V-016.
- Exit: AC-N5.

## 7. Implementation PR rule

Every implementation PR is incomplete unless it names:
1. requirement IDs;
2. journey/workflow IDs;
3. affected state transitions;
4. contract IDs and contract layer;
5. acceptance gate(s);
6. implementation task IDs;
7. verification evidence;
8. any unresolved `NOT_COMPUTABLE` items;
9. whether the change introduces or promotes any research-specific ontology into core.
