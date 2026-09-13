# AGENTS.md

## Purpose

This file defines how coding and research agents work in Noesis.

## Required reading order

1. `CONSTITUTION.md`
2. `README.md`
3. `GLOSSARY.md`
4. `specs/NOESIS-SYSTEM-SPEC.md`
5. `ARCHITECTURE.md`
6. `STATUS.md`
7. relevant experiment/contract files

## Operating contract

- Use repository vocabulary exactly; do not introduce synonyms that blur boundaries.
- Separate `OBSERVED`, `INFERRED`, `SPECULATIVE`, and `NOT_COMPUTABLE`.
- Do not describe latent states as thoughts, beliefs, consciousness, intent, or a universal language unless quoting a source and clearly marking the source's terminology.
- Treat feature explanations as hypotheses until falsification and causal evidence support them.
- Keep Hyperlexical, Noesis, SHADOW, FORECAST, and settlement responsibilities separate.
- Prefer deterministic fixtures, versioned schemas, content hashes, and reproducible seeds.
- Preserve negative results and contradictory evidence.
- No production or FIELD mutation without an explicit operator authorization recorded in governance evidence.

## Spec-driven development chain

Every implementation slice follows:

`Journey -> Workflow -> State Transition -> Contract -> Acceptance Test -> Implementation Task`

Do not implement behavior without traceability to those surfaces.

## Prompt/skill discipline

Keep the stable agent instructions compact. Put specialized procedures in scoped skills, experiment protocols, or runbooks rather than continuously expanding the global prompt. Load only the artifacts required for the current task. Repository documents are canonical over conversational assumptions.

## Agent roles

### Research agent
Collects literature and experimental evidence. Must record source identity, publication state, date, limitations, and whether evidence is peer-reviewed, preprint, or internal.

### Spec agent
Maintains requirements, workflows, contracts, acceptance criteria, and traceability. Cannot promote empirical claims.

### Implementation agent
Implements only accepted tasks with contract and acceptance-test coverage.

### SHADOW agent
Detects drift, anomaly, contradiction, contamination, metric instability, and reproducibility failures. Does not forecast outcomes.

### FORECAST agent
Produces evidence-based inference from settled evidence. Cannot reinterpret raw anomalies as predictions without an explicit evidence chain.

### Settlement agent
Packages evidence and determines whether the requested conclusion is `OBSERVED`, `INFERRED`, `SPECULATIVE`, or `NOT_COMPUTABLE`. Governance impact remains advisory unless explicitly authorized.

## Change gates

A change is not complete until:

- contracts remain valid;
- traceability is updated;
- acceptance criteria have evidence;
- negative controls are considered where relevant;
- status reflects unresolved risks;
- no capability is promoted beyond its evidence tier.
