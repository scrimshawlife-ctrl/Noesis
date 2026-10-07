# Kanban — Noesis

Board state as measured, not as remembered. Every item below was true on the date at the bottom.

| | Backlog | In progress | Blocked | Done |
|---|---|---|---|---|
| **Count** | 1 | 0 | 0 | 3 |

**Blocked** matters more than the other columns: an item sits there when it is waiting on something this
repository cannot supply, and the blocker is named rather than implied.

_Last reviewed: 2026-10-07._

## Backlog

- Broaden capture-format coverage, driven by consumers that actually supply captures.

## In progress

- Nothing pending.

## Blocked

Nothing. This repository depends on no model, no checkpoint and no weights: it consumes captures it is given.

## Done

- `NoesisEvidenceProvider` emitting `LATENT_STRUCTURAL` evidence.
- Runtime validation and real-model acceptance in CI.
- Identity reported as a label for the method, with no checkpoint claimed.
