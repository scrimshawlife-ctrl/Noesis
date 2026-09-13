# Noesis

Noesis is the Abraxas latent-representation research module: a contract-first system for measuring, comparing, falsifying, aligning, and settling claims about model representations without assuming those representations form a universal hidden language.

## Posture

- Canonical status: `CANON-SHADOW`
- Governance effect: `ADVISORY_ONLY`
- Runtime: `NOT_STARTED`
- Specification: `COMPLETE`
- N5 latent communication: `BLOCKED` pending AC-N4 + explicit operator authorization

## System boundary

```text
Hyperlexical        Noesis                  Abraxas
------------        ------                  -------
lexical forms  ->   latent evidence   ->    settlement/governance
slang               embeddings              SHADOW
symbols             hidden states           FORECAST
register            sparse features         canon decisions
transforms           probes/interventions
                    alignment/channels
```

Hyperlexical does not own latent truth. Noesis does not own Abraxas canon.

## Canonical specification

Read in this order:

1. `CONSTITUTION.md`
2. `specs/NOESIS-SYSTEM-SPEC.md`
3. `specs/REQUIREMENTS.md`
4. `specs/JOURNEYS.md`
5. `specs/WORKFLOWS.md`
6. `specs/STATE-MACHINES.md`
7. `specs/CONTRACTS.md`
8. `specs/DATA-MODEL.md`
9. `specs/SECURITY-GOVERNANCE.md`
10. `ARCHITECTURE.md`
11. `specs/ACCEPTANCE.md`
12. `TRACEABILITY.md`
13. `specs/TASKS.md`
14. `specs/VERIFICATION.md`
15. `docs/RESEARCH.md`
16. `STATUS.md` and `PLANS.md`

Experiments:
- `specs/EXP-001-SEMANTIC-INVARIANCE.md`
- `specs/EXP-002-LATENT-COMMUNICATION.md`

Machine-readable contracts live under `contracts/`.

## Provenance vocabulary

- `OBSERVED`: direct measured/recorded evidence.
- `INFERRED`: conclusion supported by evidence but not directly observed.
- `SPECULATIVE`: explicit hypothesis with insufficient confirming evidence.
- `NOT_COMPUTABLE`: required signal/evidence is missing or inadequate.

## Scientific guardrails

Noesis does **not** treat vector similarity, SAE feature labels, probe accuracy, steering success, latent task performance, or cross-model alignment as automatic evidence of consciousness, intent, semantic identity, universal neuralese, or a faithful hidden chain-of-thought transcript.

Negative evidence, failed captures, contradictory controls, and failed replications are first-class outputs.

## Current next slice

`SLICE-001 — Reproducible Representation Capture`

Build the typed core, adapter protocol, Hugging Face reference adapter, immutable experiment-manifest runner, hidden-state/embedding capture, content-addressed observations, baseline metrics, and replay/failure tests.

Exit gate: `AC-N0` plus the capture portion of `AC-N1`.

## Validation

Run:

```bash
python scripts/validate_specs.py
```

CI runs the same canonical specification validation on pull requests and pushes.