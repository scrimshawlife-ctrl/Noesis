# Traceability

## Requirements to journeys/workflows/gates

| Requirement | Journey | Workflow | Acceptance |
|---|---|---|---|
| FR-001 capture representations | J-001/J-002 | WF-002 | AC-N0, AC-N1 |
| FR-002 exact model/site provenance | J-001/J-003 | WF-001/WF-002 | AC-N0, AC-N1 |
| FR-003 controlled transforms | J-001 | WF-001/WF-003 | AC-N3 |
| FR-004 representation metrics | J-001/J-003 | WF-003 | AC-N0, AC-N3, AC-N4 |
| FR-005 sparse dictionaries | J-002 | WF-004 | AC-N2 |
| FR-006 probes and controls | J-002 | WF-004 | AC-N2 |
| FR-007 causal interventions | J-002 | WF-004 | AC-N2 |
| FR-008 cross-model alignment | J-003 | WF-005 | AC-N4 |
| FR-009 preserve negative evidence | all | WF-004/WF-006/WF-007 | all |
| FR-010 settlements | J-004 | WF-006 | AC-G0+ |
| FR-011 stable external contracts | J-001/J-004 | WF-001/WF-006 | AC-G0 |
| FR-012 deterministic replay | J-001/J-002/J-003 | WF-001/WF-002 | AC-N0/N1 |
| FR-013 gate latent communication | J-005 | WF-007 | AC-N5 |

## Experiment traceability

### EXP-001
- Journeys: J-001, J-002, J-004
- Workflows: WF-001, WF-002, WF-003, WF-004, WF-006
- Requirements: FR-001–FR-007, FR-009–FR-012
- Gates: AC-N0, AC-N1, AC-N2, AC-N3
- Contracts: Observation, Settlement; future ExperimentManifest/MetricResult

### EXP-002
- Journey: J-005
- Workflows: WF-005, WF-006, WF-007
- Requirements: FR-008–FR-013
- Entry gate: accepted AC-N4 + operator approval
- Exit gate: AC-N5
- Contracts: Settlement plus future AlignmentMap/LatentChannelResult

## Task traceability

| Task family | Requirements | Exit evidence |
|---|---|---|
| T-001 foundation | FR-009–FR-013, NFR-001–007 | AC-G0 |
| T-010 contracts/types | FR-002, FR-009–012 | schema tests |
| T-020 model adapter | FR-001/002 | AC-N1 |
| T-030 capture harness | FR-001/002/012 | AC-N0/N1 |
| T-040 comparison metrics | FR-004 | AC-N0 |
| T-050 Hyperlexical interface | FR-003/011 | AC-N3 prerequisite |
| T-060 SAE/probe/falsification | FR-005/006/009 | AC-N2 |
| T-070 causal lab | FR-007 | AC-N2 |
| T-080 alignment lab | FR-008 | AC-N4 |
| T-090 settlement writer | FR-009/010/011 | schema-valid settlement |
| T-100 EXP-001 | FR-001–012 | AC-N3 |
| T-200 latent channel | FR-008–013 | AC-N5 |

Any implementation PR lacking requirement, workflow, acceptance criterion, and verification evidence is incomplete.
