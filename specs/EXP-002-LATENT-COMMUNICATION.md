# EXP-002 — Latent Communication

Status: `BLOCKED / RESEARCH-ONLY`
Entry gate: `AC-N4` accepted plus explicit operator approval.

## Purpose
Test whether direct latent-state transfer between agents/models can preserve task-relevant information more efficiently or effectively than text or serialized-vector baselines.

## Non-claims
Success does not establish a universal neuralese, shared subjective semantics, consciousness, or faithful transmission of internal reasoning.

## Required baselines

1. natural-language message;
2. compressed natural-language message;
3. serialized vector/feature payload if applicable;
4. sender-only and receiver-only task baselines;
5. shuffled/random latent control.

## Variables

- sender model/revision/site;
- receiver model/revision/site;
- alignment/adapter revision;
- latent dimensionality and compression ratio;
- task family;
- communication budget;
- latency and compute budget.

## Metrics

- held-out task accuracy/utility;
- communication bytes/dimensions;
- inference latency;
- compression ratio;
- robustness under distribution shift;
- ablation sensitivity;
- alignment quality;
- information leakage/privacy probes where relevant.

## Workflow

Use `WF-007` only after entry gate. Fit any alignment exclusively on training data. Evaluate held-out tasks and at least one task-family or domain shift. Preserve unsuccessful communication trials and null results.

## Acceptance

A latent channel may be called **operationally useful** only if it beats a declared baseline on a pre-registered utility/efficiency criterion and reproduces independently.

A latent channel may be called **semantically aligned** only if separate N4 alignment evidence supports that claim on held-out data. Task success alone is insufficient.

## Research basis

Interlat (ACL 2026) establishes feasibility of direct last-hidden-state inter-agent communication and reports competitive performance plus large inference compression benefits, including heterogeneous-model experiments. Noesis treats that result as precedent for feasibility, not as proof that arbitrary models share a native language.
