#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from noesis.acceptance import N01AcceptanceConfig, run_n01_acceptance
from noesis.adapters.huggingface import HuggingFaceAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.contracts.registry import ContractRegistry
from noesis.domain.models import RepresentationSite


def parse_site(value: str) -> RepresentationSite:
    if value == "embedding":
        return RepresentationSite(kind="embedding", layer=None, token_index=-1)
    if value.startswith("hidden_state:"):
        _, layer = value.split(":", 1)
        return RepresentationSite(kind="hidden_state", layer=int(layer), token_index=-1)
    raise argparse.ArgumentTypeError("site must be 'embedding' or 'hidden_state:<layer>'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Noesis AC-N0/AC-N1 acceptance against a pinned open-weight model.")
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--revision", required=True, help="Immutable model revision/commit; do not use a floating branch for settlement evidence.")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--fixture-id", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--site", action="append", type=parse_site, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--cosine-floor", type=float, default=0.999999)
    parser.add_argument("--euclidean-ceiling", type=float, default=1e-9)
    parser.add_argument("--artifacts", type=Path, default=Path("out/acceptance/artifacts"))
    parser.add_argument("--output", type=Path, default=Path("out/acceptance/n01-evidence.json"))
    args = parser.parse_args()

    adapter = HuggingFaceAdapter(args.model_id, revision=args.revision, device=args.device)
    store = ContentAddressedStore(args.artifacts)
    config = N01AcceptanceConfig(
        experiment_id="N01-ACCEPTANCE",
        fixture_id=args.fixture_id,
        text=args.text,
        sites=tuple(args.site),
        seed=args.seed,
        repeats=args.repeats,
        cosine_floor=args.cosine_floor,
        euclidean_ceiling=args.euclidean_ceiling,
    )
    evidence = run_n01_acceptance(adapter, store, config)
    ContractRegistry("contracts").validate("n01-acceptance-evidence", evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(evidence["gate_decisions"], sort_keys=True))


if __name__ == "__main__":
    main()
