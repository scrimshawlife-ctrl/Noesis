# Hyperlex Integration Boundary

Status: `CANON-SHADOW / ADAPTER_READY / MODEL_BINDING_PENDING`

## Purpose

Noesis consumes Hyperlex outputs as controlled lexical/symbolic transformations. Hyperlex is an external experimental instrument. It does not own latent evidence semantics, feature labels, Noesis settlements, or the scientific truth of its own declared transform intent.

## Current adapter surfaces

- `CallableHyperlexAdapter`: wraps an in-process Python function or local inference object.
- `HttpHyperlexAdapter`: posts/receives versioned JSON for a separately served Hyperlex runtime.
- `DeterministicHyperlexAdapter`: CI/test-only adapter; never scientific evidence.

All adapters implement the same `HyperlexAdapter` protocol and must emit a schema-valid `HyperlexTransformResult`.

## Contract flow

`HyperlexTransformRequest -> HyperlexAdapter -> HyperlexTransformResult -> MaterializedFixture -> ExperimentManifest/Capture`

Request metadata includes:
- source fixture identity and text;
- transform class;
- semantic intent;
- expected invariants;
- expected changed attributes;
- seed and optional parameters.

Result metadata includes:
- transform identity/version;
- transformed text;
- SHA-256 content hash;
- transform class and declared intent;
- expected invariants/changed attributes;
- provider metadata;
- `OBSERVED` provenance for the transform output itself.

## Authority boundary

Hyperlex may state: `this transformation is intended to preserve X`.

Hyperlex may not state: `Noesis latent feature Y means X`.

Noesis does not assume:
- that Hyperlex preserved meaning;
- that Hyperlex transform classes are scientifically valid;
- that declared invariants were actually preserved;
- that Hyperlex labels correspond to latent structure.

Hyperlex output is experimental input. Its quality and semantic fidelity are separately measurable propositions.

Noesis independently measures whether the declared invariant survives representation capture and controls. Settlement authority remains in Noesis/Abraxas governance.

## Hypothesis-neutral integration rule

The Hyperlex adapter exists to transport versioned transform requests and results. Hyperlex-specific ontologies, class names, training objectives, or semantic theories do not become Noesis core ontology merely because the adapter supports them.

A different transformation system may implement the same integration role without changing core Noesis evidence semantics.

## Training-period posture

While Hyperlex is still training:
1. keep model transport behind the adapter protocol;
2. use the deterministic adapter only for contract/replay tests;
3. compile EXP-001 plans from operator-supplied source fixtures and transform hypotheses;
4. generate canonical and control transform bundles without treating their content as scientific evidence;
5. bind the real model only when its inference request/response surface stabilizes;
6. record the final Hyperlex model/version/hash in provider metadata before any research run.

## Binding checklist

A trained Hyperlex runtime is ready to bind when:
- its inference API is deterministic or declares nondeterminism;
- exact model/training snapshot identity is available;
- request and output encoding are stable;
- transform classes map cleanly to the versioned Noesis contract;
- output hashes can be reproduced;
- failures are explicit;
- no field attempts to assert latent truth or settlement authority.

Until then, model binding remains `NOT_COMPUTABLE` rather than inferred.
