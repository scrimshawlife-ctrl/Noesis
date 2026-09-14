# N01 Acceptance Settlement — 2026-09-14

Status: `ACCEPTED / CANON-SHADOW / ADVISORY_ONLY`

## Decision

- `AC-N0: ACCEPT`
- `AC-N1: ACCEPT`

This settlement accepts deterministic representation comparison and pinned hidden-state capture for the declared model, fixture, environment, sites, seed, and tolerance. It does not accept semantic invariance, mechanistic interpretation, layer distinctness, cross-model alignment, or any EXP-001-GEO hypothesis.

## Execution provenance

- Workflow: `n01-real-model-acceptance`
- Run: [GitHub Actions 34826673897](https://github.com/scrimshawlife-ctrl/Noesis/actions/runs/34826673897)
- Run attempt: `1`
- Source commit: `fad04bcfeb171bae5893c32b023621140f8a9e63`
- Generated UTC: `2026-09-14T09:13:53.281397+00:00`
- Artifact ID: `10340582177`
- Archive SHA-256: `f917a1c014a9b156ab4e45d25e54dca4153b55f68ec07bf310eabfac7ffd8bd0`
- Evidence JSON SHA-256: `402f3d4d11d041226df90d803ce51000053601ed92df919cbde6f55e3ca6b264`
- Artifact retention expiry reported by GitHub: `2026-12-13T09:12:23Z`

## Frozen inputs

- Model: `sshleifer/tiny-distilbert-base-cased`
- Model revision: `657df2b83a6986d88e4f528740259c9b49f796b1`
- Tokenizer revision: `657df2b83a6986d88e4f528740259c9b49f796b1`
- Fixture ID: `n01-manual-fixture`
- Fixture SHA-256: `ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c`
- Seed: `0`
- Repeats: `2`
- Environment: Python `3.12.14`, Transformers `4.57.6`, Torch `2.14.0+cu130`, CPU
- Tolerance: cosine >= `0.999999`; Euclidean <= `1e-9`

## Results

| Site | Cosine | Euclidean | Decision |
|---|---:|---:|---|
| `embedding:token=-1` | `1.0` | `0.0` | ACCEPT |
| `hidden_state:layer=1:token=-1` | `0.9999999999999998` | `0.0` | ACCEPT |
| `hidden_state:layer=2:token=-1` | `0.9999999999999998` | `0.0` | ACCEPT |

Validation:

- top-level N01 evidence schema: PASS;
- six Observation schemas: PASS;
- six artifact references and SHA-256 checks: PASS;
- three site decisions: ACCEPT;
- workflow and artifact-upload steps: SUCCESS.

## SHADOW findings and limitations

1. Hidden-state layers 1 and 2 produced the same artifact SHA-256: `723f1c3eac1d2c306857db9f4466b219af88d13fb056836892154fcd058c55d5`.
2. Each captured artifact has shape `[2]`; this tiny model is suitable for pipeline reproducibility but not evidence of rich or layer-distinct semantic geometry.
3. `weights_sha256` is null. Reproducibility is bound to the immutable Hugging Face model/tokenizer revision rather than a separately recorded weight-file digest.
4. The GitHub artifact is retention-limited. The canonical top-level evidence JSON is committed with this settlement; its referenced binary and observation artifacts remain in the workflow archive until expiry.
5. The run uses one fixture, one seed, and two repeats. It satisfies the registered gate but does not establish cross-fixture, cross-seed, cross-device, or cross-version stability.

## Epistemic classification

- `OBSERVED`: the declared embedding and hidden-state captures reproduced within registered tolerance in workflow run 34826673897.
- `INFERRED`: the Noesis N0/N1 pipeline is ready to support bounded follow-on experiment preparation under the same evidence controls.
- `NOT_COMPUTABLE`: semantic invariance, feature meaning, layer distinctness, cross-model equivalence, winning geometry, and downstream scientific utility.

## Next permitted state

- N0 and N1 may be recorded as accepted for this pinned reference run.
- EXP-001 corpus and transform/control preparation may proceed.
- EXP-001-GEO remains inactive until its relational corpus and GeometryProfile receive operator approval.
- N2, N3, N4, N5, FIELD authority, promotion, and Abraxas canon mutation remain ungranted.
