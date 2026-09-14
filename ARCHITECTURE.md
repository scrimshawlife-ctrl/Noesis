# Noesis Architecture

## System position

```text
Hyperlexical ── lexical transforms ──┐
                                     │
Model Adapter ─ activations/latents ─┼─> Capture -> Normalize -> Compare -> Probe -> Falsify -> Settle
                                     │                                      │
Semiotic Surface ─ labels/relations ─┘                                      ├-> SHADOW
                                                                            └-> FORECAST
```

Noesis does not own lexical meaning or Abraxas governance. It owns experimental latent-representation evidence and contracts.

## Research-program boundary

Noesis is a domain-general representation-measurement system. Research programs supply hypotheses and interpretation frameworks through versioned external contracts; Noesis supplies measurement and evidence primitives.

```text
Research Program
  hypothesis
  semantic ontology
  transform taxonomy
  expected relationships
  acceptance thresholds
         │
         │ versioned external contracts
         ▼
Noesis
  capture
  compare
  align
  intervene
  falsify
  quantify uncertainty
  preserve evidence
  settle
```

Noesis may support research into invariance, robustness, semantic preservation, model drift, interpretability, agent communication, translation, memory, or other representation-level phenomena. None of those research programs define the meaning or architecture of the Noesis core.

### Core-owned semantics

Noesis core owns model and representation identity, observation provenance, artifact identity, capture sites, measurement procedures, metric execution, control/null execution, uncertainty, intervention records, alignment records, failures, evidence relations, settlements, and reproducibility.

### Experiment-owned semantics

Experiments own concepts, semantic categories, hypotheses, expected invariants, expected changes, transform classes, behavioral interpretations, domain-specific labels, and theory-specific metrics or thresholds where they are not generally applicable.

### Promotion rule

A construct may move from experiment-owned semantics into Noesis core only when:
1. it is useful across materially different research questions;
2. it does not imply the truth of one research theory;
3. its semantics can be defined operationally;
4. its inclusion reduces ambiguity or hidden coupling;
5. backward compatibility and evidence meaning are preserved.

Otherwise it remains external.

## Modules

### A-001 Model Adapter
Normalizes model-specific hooks for embeddings, residual stream/hidden states, attention/MLP sites where supported, tokenizer metadata, and revision identity.

### A-002 Capture
Produces immutable `Observation` records for selected representation sites. Raw tensors may be external artifacts referenced by content hash rather than embedded in metadata.

### A-003 Transform Harness
Receives controlled surface transformations from Hyperlexical or fixture generators. Each transform has a stable ID, semantic-intent expectation, and contamination tags. Transform semantics remain experiment-owned hypotheses.

### A-004 Representation Comparator
Computes predeclared metrics such as cosine similarity, centered-kernel alignment, representational similarity analysis, neighborhood preservation, linear-probe transfer, or task-specific statistics. Metric choice is experiment-defined.

### A-005 Sparse Feature Lab
Trains or loads versioned SAE/dictionary models. Stores reconstruction, sparsity, dead-feature, feature-consistency, and run-to-run stability metrics. Human-readable feature descriptions remain hypotheses.

### A-006 Probe Lab
Runs pre-registered probes. Probe performance must be compared against controls and distribution shifts; probe success is not sufficient evidence of causal encoding.

### A-007 Causal Lab
Supports activation patching, ablation, steering, counterfactual feature injection, and equivalent interventions where the model/runtime allows them.

### A-008 Alignment Lab
Maps representations across layers, checkpoints, or models using explicitly fitted transforms. Alignment evidence is versioned and never assumed transitive.

### A-009 Latent Channel Lab
Research-only surface for encoded model-to-model latent communication. Disabled by default until N0–N4 acceptance gates are met.

### A-010 Settlement Engine
Packages evidence into deterministic `Settlement` records with provenance label, confidence basis, negative results, unresolved contradictions, and promotion recommendation.

## Storage classes

1. **Metadata** — experiment definitions, model revisions, transforms, metrics, provenance.
2. **Evidence artifacts** — tensors, feature dictionaries, plots, intervention outputs; content-addressed.
3. **Settlements** — compact immutable conclusions referencing evidence hashes.

## Trust boundaries

- Closed APIs that do not expose internal states cannot satisfy hidden-state capture requirements.
- Model-generated explanations are untrusted annotations.
- Third-party SAE dictionaries are external evidence until reproduced or independently validated.
- Cross-model adapters are experimental components, not neutral transports.
- Research-program labels and semantic expectations are declared hypotheses, not core truth.

## Execution environments

- `LAB`: synthetic or public fixtures; development and falsification.
- `RESEARCH`: controlled benchmark/data studies; reproducibility required.
- `FIELD`: prohibited until explicit governance settlement defines allowed inputs, retention, privacy, and intervention boundaries.

## Dependency direction

```text
contracts <- core types <- adapters
contracts <- experiment definitions
core types <- comparison/probe/SAE/causal/alignment labs
settlement <- all evidence producers
Hyperlexical -> transform contract only
Abraxas <- settlement contract only

Noesis Core
   ↑
Integrations
   ↑
Research Programs
```

Allowed dependencies include `EXP-* -> Noesis`, external adapters -> Noesis contracts, and benchmarks -> Noesis.

Forbidden dependencies include Noesis core -> EXP-001, Noesis core -> semantic-invariance theory, Noesis core -> Hyperlex ontology, and Noesis core -> funding or research-program framing.

Noesis must remain usable as a standalone research package while exposing stable contracts to Abraxas and Hyperlexical.
