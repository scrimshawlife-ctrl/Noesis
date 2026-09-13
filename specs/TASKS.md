# Noesis Implementation Tasks

Status: `CANON-SHADOW`
Version: `0.2.0`

Tasks are implementation units derived from requirements/workflows. No task may silently change doctrine.

## T-001 — Foundation completion
Depends on: none
Requirements: FR-060–094, NFR-001–053
Outputs: complete spec package, schemas, CI validation, traceability.
Exit: AC-G0.

## T-010 — Core domain package
Depends on: T-001
Requirements: FR-060–074
Outputs: typed IDs, ModelIdentity, RepresentationSite, InputFixture, Transform, Manifest, Run, Observation, Result, Settlement types; serialization helpers.
Verification: schema round-trip, invalid-object rejection, hash stability.

## T-020 — Runtime adapter protocol
Depends on: T-010
Requirements: FR-001–005, FR-082
Outputs: adapter interface, capability declaration, model identity resolver, supported-site registry.
Exit evidence: unsupported-site and revision-mismatch tests.

## T-021 — Hugging Face reference adapter
Depends on: T-020
Requirements: FR-001–005, NFR-040–042
Outputs: open-weight Transformers adapter supporting embeddings/hidden states for at least one reference model family.
Exit: AC-N1 adapter portion.

## T-030 — Deterministic capture runner
Depends on: T-010, T-020
Requirements: FR-003–005, FR-070–074
Outputs: manifest executor, seed/environment capture, tensor validator, artifact writer, FailureRecord emitter.
Exit: AC-N0 + capture portion AC-N1.

## T-040 — Metric engine
Depends on: T-010, T-030
Requirements: FR-020–025
Outputs: cosine, Euclidean, CKA where valid, neighborhood overlap, bootstrap/permutation/null utilities.
Exit: AC-N0.

## T-050 — Hyperlexical transform boundary
Depends on: T-010
Requirements: FR-010–013, FR-080
Outputs: transform contract, deterministic fixture import/export, transform provenance validation.
Invariant: Hyperlexical cannot set latent truth labels.

## T-060 — Sparse dictionary lab
Depends on: T-030, T-040
Requirements: FR-030–033
Outputs: SAE/dictionary adapter, training/load path, reconstruction/sparsity/dead-feature reporting, consistency analysis.
Exit contribution: AC-N2.

## T-061 — Probe lab
Depends on: T-030, T-040
Requirements: FR-034–035
Outputs: probe training/eval harness, leakage checks, held-out metrics, baselines.
Exit contribution: AC-N2.

## T-062 — Falsification suite
Depends on: T-050, T-060/061
Requirements: FR-032–035
Outputs: lexical-trigger tests, semantic positives without trigger, negative/confound controls, adversarial fixture support.
Exit: must demonstrate at least one candidate can be rejected/weakened.

## T-070 — Intervention lab
Depends on: T-021, T-030
Requirements: FR-040–043
Outputs: patch/ablate/steer/inject protocol where adapter supports it, matched controls, InterventionResult.
Exit contribution: AC-N2.

## T-080 — Alignment lab
Depends on: T-030, T-040
Requirements: FR-050–054
Outputs: train/val/test alignment harness, map artifact, null mappings, held-out/shift metrics.
Exit: AC-N4.

## T-090 — Settlement engine
Depends on: T-010, T-040
Requirements: FR-060–065
Outputs: evidence bundling, contradiction preservation, provenance assignment rules, promotion recommendation, supersession records.
Verification: unsupported claim returns NOT_COMPUTABLE/WEAK rather than fabricated evidence.

## T-100 — EXP-001 execution
Depends on: T-050, T-060/061, T-090
Requirements: FR-001–082 excluding N5-only
Outputs: semantic invariance evidence bundle and settlement.
Exit: AC-N3.

## T-110 — Independent replication harness
Depends on: T-090, T-100
Requirements: FR-065, FR-072–074
Outputs: independent rerun/falsification workflow, comparison envelope, replication settlement.
Exit: AC-R1/AC-R2.

## T-120 — Audit and security controls
Depends on: T-010
Requirements: NFR-010–012, NFR-050–053
Outputs: classification validation, secret scan hooks, artifact integrity verifier, authorization metadata, synthetic incident/supersession test.
Exit: AC-S1.

## T-200 — Latent channel prototype
Status: BLOCKED
Depends on: accepted AC-N4, explicit operator authorization
Requirements: FR-090–094
Outputs: sender/receiver channel abstraction, text baseline, serialized-vector baseline, latent channel, information/latency/task metrics.
Exit contribution: AC-N5.

## T-210 — Latent channel adversarial suite
Status: BLOCKED
Depends on: T-200
Outputs: leakage/covert-transfer probes, distribution shift, semantic mismatch evaluation, compression sweeps.
Exit: AC-N5.

## Ordering

```text
T-001
  -> T-010
     -> T-020 -> T-021 -> T-030 -> T-040
     -> T-050 ---------------------|
     -> T-090 ---------------------|
                                   v
                         T-060/T-061 -> T-062 -> T-070
                                   |
                                   v
                                 T-100 -> T-110
                                   |
                         T-080 -----|
                                   v
                          AC-N4 decision
                                   |
                    [operator authorization]
                                   v
                              T-200 -> T-210
```

## Task completion rule

A task is complete only when implementation, tests, traceability, evidence artifacts, and relevant acceptance references are all present. A merged code path without verification evidence remains incomplete.