# Plans

## Phase 0 — Foundation

Goal: repository doctrine, system specification, contracts, research baseline, traceability, and validation.

Deliverables:
- constitution;
- architecture;
- system spec;
- experiment specs;
- observation/settlement schemas;
- glossary/status;
- research baseline;
- validation automation.

Gate: `AC-G0`.

## Phase 1 — N0/N1 Capture kernel

Goal: reproducible representation capture from one open-weight model family.

Deliverables:
- Python package and CLI;
- model adapter protocol;
- Hugging Face reference adapter;
- experiment manifest;
- deterministic fixture runner;
- embedding/hidden-state capture;
- artifact hashing and observation writer;
- baseline similarity metrics.

Gate: `AC-N0` + `AC-N1`.

## Phase 2 — N2 Falsification lab

Goal: make interpretability claims difficult to fool.

Deliverables:
- probe protocol;
- SAE/dictionary adapter;
- reconstruction/sparsity/dead-feature metrics;
- run-to-run feature consistency;
- lexical-trigger attacks;
- adversarial positive/negative fixtures;
- activation patching/steering adapters where supported.

Gate: `AC-N2`.

## Phase 3 — N3 Semantic invariance

Goal: execute EXP-001.

Deliverables:
- frozen concept corpus;
- Hyperlexical transform contract implementation;
- transformed fixture set;
- within/between metrics and uncertainty;
- held-out transform evaluation;
- falsification report;
- first Noesis settlement.

Gate: `AC-N3`.

Optional subtrack: `EXP-001-GEO` may begin only after AC-N0/AC-N1 acceptance and an operator-approved relational corpus plus `GeometryProfile`. Its separate exit gate is `AC-N3-GEO`; no geometry is presumed to win.

## Phase 4 — N4 Cross-model alignment

Goal: determine which geometry transfers across model families/checkpoints.

Deliverables:
- alignment protocol and contract;
- train/validation/test discipline;
- null mapping baselines;
- distribution-shift evaluation;
- cross-layer and cross-model experiments.

Gate: `AC-N4`.

## Phase 5 — N5 Latent communication

Goal: evaluate direct latent communication only after N4.

Deliverables:
- sender/receiver interface;
- text/compressed-text/serialized-vector baselines;
- latent adapters and compression variants;
- task, latency, communication-budget, and robustness evaluation;
- information-leak controls;
- EXP-002 settlement.

Gate: `AC-N5`.

## Deferred

- universal-neuralese claims;
- production decision authority;
- FIELD capture;
- automated semantic canon promotion;
- consciousness/sentience inference;
- opaque closed-model hidden-state claims without instrument access.
