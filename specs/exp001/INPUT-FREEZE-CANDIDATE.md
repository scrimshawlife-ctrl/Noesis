# EXP-001 Input Freeze Candidate

Status: `DRAFT / OPERATOR_APPROVAL_REQUIRED`

## Decision requested

Approve, reject, or revise the exact EXP-001 source corpus and transform/control catalog. Approval must identify the operator, UTC decision time, scope, constraints, and canonical SHA-256 digest of each input.

## Required corpus coverage

The candidate must contain 100 independently reviewable concepts across relation, agency, boundary, exchange, threat, identity, causality, temporal change, social role, and symbolic/archetypal categories.

Partitions must be assigned before execution:

- `discovery`: hypothesis formation and diagnostic analysis;
- `confirmation`: inaccessible during fitting or threshold selection;
- `control`: negative, altered-meaning, contamination, and lexical-trigger cases.

Noesis does not generate or approve the semantic content. Each fixture requires operator-supplied text, a stable fixture ID, hypothesis tags, and a partition.

## Required transform/control coverage

- literal paraphrase;
- colloquial/slang;
- metaphorical;
- symbolic/emoji;
- technical/register shift;
- multilingual translation;
- negation;
- compositional role reversal;
- adversarial paraphrase;
- lexical-trigger controls.

Each entry must declare semantic intent, expected invariants, expected changed attributes, parameters, and experimental role. These fields are preregistered hypotheses, not observed semantic truth.

## Approval receipt

Use `contracts/exp001-freeze-receipt.schema.json`. The receipt binds approval to the canonical JSON digest of both inputs. Any byte-level semantic change that changes canonical JSON requires a new receipt.

Compilation fails closed unless all three documents validate and the receipt hashes and identities match:

```bash
python scripts/compile_exp001_plan.py \
  --corpus path/to/corpus.json \
  --catalog path/to/catalog.json \
  --approval path/to/freeze-receipt.json \
  --seed 17 \
  --output out/exp001-plan.json
```

## Current result

- `OBSERVED`: the approval contract and hash-binding verifier exist and are testable.
- `NOT_COMPUTABLE`: corpus fitness, semantic-label quality, transform validity, and AC-N3 remain unavailable until the operator supplies and approves the inputs.
