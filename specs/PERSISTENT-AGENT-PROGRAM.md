# Noesis participation in persistent-agent research

Program: `ABX-NOEMA-REP-001`  
Status: proposed / SHADOW / ADVISORY_ONLY  
Date: 2026-09-14  
Scope: specification review only; no runtime or permission change.

[Shared program draft](https://github.com/scrimshawlife-ctrl/Abraxas/blob/codex/persistent-agent-program-20260914/docs/research/persistent-agent-program/spec.md) owns cross-repository experiment coordination, workflows WF-P01 through WF-P05, acceptance AC-P01 through AC-P10, and the candidate sidecar. This document owns only this repository's participation mapping. The program is not a new specialist or a replacement for existing contracts. Draft branch links are review links; pin the accepted commit when adopted.

## Existing authority

[Constitution](../CONSTITUTION.md), [system spec](NOESIS-SYSTEM-SPEC.md), [architecture](../ARCHITECTURE.md), [contracts](CONTRACTS.md), [EXP-001](EXP-001-SEMANTIC-INVARIANCE.md), [acceptance](ACCEPTANCE.md), and [status](../STATUS.md) prevail. Noesis is an instrument in the Abraxas system and remains usable independently. This program adds no required Noema dependency to core and no provider dependency to an experiment contract.

## Role and mappings

| Program input | Noesis-owned artifact | Restriction |
|---|---|---|
| Approved model/site/configuration | ModelIdentity, RepresentationSite, ExperimentManifest | Chat API compatibility is not hidden-state access |
| Approved source/transform/control corpus | InputFixture and transform adapter records | Preserve exact corpus/catalog approval hashes |
| Captured tensors | Observation and content-addressed artifacts | Raw activations are distinct from interpretation |
| Hyperlexical or Semion annotations | External referenced metadata | Neither lexical confidence nor sign class establishes semantic truth |
| Comparison and controls | MetricResult, EvidenceBundle, Settlement | Findings remain bounded and advisory |

Do not relabel a model embedding as another model's hidden state. A Nemotron profile needs separate model-specific capture capability and acceptance evidence. The existing AC-N0/AC-N1 reference acceptance supports only its pinned model/configuration and scope.

## Workflows and traceability

J-P01/WF-P01 maps to local J-001 and WF-001 (registration). J-P03/WF-P03 maps to WF-002 capture and WF-003 comparison; the local experiment state machines stay authoritative. J-P04/WF-P04 maps to WF-007 settlement and WF-008 independent replication. EXP-001's settlement reference is aligned to WF-007 in this patch; WF-006 remains causal intervention.

T-NOE-P01 -> AC-P01/AC-P02: validate program source pointers against existing ExperimentManifest and the EXP001FreezeReceipt. Corpus, catalog and exact operator approval must exist; program approval is not input-freeze approval.

T-NOE-P02 -> AC-P05/AC-P06: reference actual permitted source artifacts and capture outputs in the external sidecar without changing existing packets. Unsupported sites or missing data return NOT_COMPUTABLE for latent claims. Preserve successful unrelated behavioral evidence.

T-NOE-P03 -> AC-P08/AC-P09: compare controlled conditions using the registered metric/null/partition definitions; measure capture overhead, tensor storage/transfer volume and reproducibility cost. Retain nulls, counterevidence and leakage checks. No empirical result is created by these tasks being specified.

## Scope and evidence limits

EXP-001 remains the first semantic-invariance experiment. The program does not create a competing experiment or change its model-independent form. Optional geometry requires its existing profile approval. N5 latent communication remains blocked under existing gates. Semion annotation is permitted only as data through approved contracts; no new Noesis specialist binding is inferred from Spec 009.

Noesis capture may justify GPU capacity when actual tensor/capture/probe workloads demonstrate need. The initial integration does not require an SAE, trained router, causal intervention module or multiple devices. Correlation remains INFERRED; functionally relevant interpretation needs the specified intervention evidence.

## Verification and unresolved work

Run python scripts/validate_specs.py plus local link/diff checks. The integration mapping is proposed and not a replacement for local TRACEABILITY.md. Before implementation, add approved task IDs to local traceability and preserve the required Journey -> Workflow -> State Transition -> Contract -> Acceptance Test -> Implementation Task chain.

Exact Noema-derived corpus, supported Nemotron capture site, operational scenario, approval receipt and cross-component compatibility are not yet supplied by this program. Their acceptance is NOT_COMPUTABLE. No independent replication, FIELD permission, trained Hyperlex binding or semantic-invariance acceptance is claimed.
