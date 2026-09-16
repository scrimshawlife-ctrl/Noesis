# Notion parity card

**Authority:** this repo (`STATUS.md`). Notion is a mirror, not a second canon.

**Repo:** https://github.com/scrimshawlife-ctrl/Noesis  
**Observed:** 2026-09-16  
**Posture:** `CANON-SHADOW` / `ADVISORY_ONLY`

Paste the block below onto the Noesis / Abraxas operator hub card. Do not mark AC-N2, AC-N3, AC-N4, AC-N5, or AC-R2 accepted from this card.

---

## Noesis — operator snapshot

Spec complete. Runtime through **SLICE-027** on `main` (PRs #12–#29). Tests: 129 passed locally at last slice; spec validation PASS.

| Gate | State |
|---|---|
| AC-N0 / AC-N1 | **Accepted** (pinned real-model run [34826673897](https://github.com/scrimshawlife-ctrl/Noesis/actions/runs/34826673897)) |
| Hyperlex | Adapter + preregistration **implemented**. Trained-model binding **pending**. |
| N2 dictionary/probes/interventions | Runtime **implemented**. AC-N2 **not accepted** (fake adapter ≠ science). |
| N3 EXP-001 | Compiler fail-closed without operator freeze receipt. **Not executed**. |
| EXP-001-GEO | Geometry runtime **implemented**. **Not executed**. AC-N3-GEO **not accepted**. |
| N4 alignment | Linear map **implemented**. AC-N4 **not accepted**. |
| N5 | **Blocked** until AC-N4 + explicit operator auth. |
| AC-R2 | Harness only. No independent scientific replication. |

### Operator-owned next (not agent-inventable)

1. Freeze EXP-001 source corpus + transform/control catalog + freeze receipt (`specs/exp001/INPUT-FREEZE-CANDIDATE.md`).
2. Keep EXP-001-GEO inactive until a relational corpus is approved.
3. Bind Hyperlex when its inference surface is stable.
4. Independent operator rerun of N0/N1 with new controls.

### Runtime inventory (implemented, advisory)

Capture kernel · settlement engine · SAE/probe/intervention labs · geometry profile (Euclidean/hyperbolic/spherical/product/topological) · ProjectionLoss · GeometricRupture · relation-prediction AUC · classification/secret gates · verified artifact load · environment fingerprints · FIELD/N5 capture authorization gate (not N5 science).

No latent semantic claim is promoted.

---

## Parity rule

If Notion and `STATUS.md` disagree, **`STATUS.md` wins**. Update Notion from this file; do not update the repo from a Hub paraphrase.
