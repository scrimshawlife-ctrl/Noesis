# Roadmap — Noesis

Latent structural evidence: reads captured activations and reports structure. It computes nothing
about a model it was not handed, which is what keeps its output attributable.

Three words are used in one sense each, and they are not interchangeable:

- **shipped** — merged, and something runs it.
- **in progress** — being worked on now.
- **not planned** — deliberately not being built, with the reason given.

Anything that would require a claim this repository cannot evidence is listed as not planned rather than
deferred, because a roadmap that quietly carries an unmet promise is worse than a short one.

_Last reviewed: 2026-10-07._

## Shipped

- `NoesisEvidenceProvider` emitting `LATENT_STRUCTURAL` evidence.
- Runtime validation and a real-model acceptance workflow in CI.

## In progress

- Keeping capture ingestion honest as capture formats move.

## Next

- Wider capture-format coverage, driven by whichever consumers actually supply captures.

## Not planned

- **Loading a model to generate its own captures.** Noesis consumes captures supplied to it; an engine that
  produced its own inputs would be scoring itself.
