#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from noesis.contracts.registry import ContractRegistry
from noesis.experiments.exp001 import SourceFixtureSpec, TransformSpec, compile_exp001_requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile frozen EXP-001 source corpus and transform catalog into deterministic Hyperlex requests.")
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    registry = ContractRegistry("contracts")
    registry.validate("exp001-source-corpus", corpus)
    registry.validate("exp001-transform-catalog", catalog)

    sources = tuple(
        SourceFixtureSpec(fixture_id=item["fixture_id"], text=item["text"])
        for item in corpus["fixtures"]
    )
    transforms = tuple(
        TransformSpec(
            transform_class=item["transform_class"],
            semantic_intent=item["semantic_intent"],
            expected_invariants=tuple(item["expected_invariants"]),
            expected_changed_attributes=tuple(item["expected_changed_attributes"]),
            parameters=item.get("parameters") or {},
        )
        for item in catalog["transforms"]
    )
    requests = compile_exp001_requests(sources, transforms, seed=args.seed)
    output = {
        "schema_version": "1.0.0",
        "corpus_id": corpus["corpus_id"],
        "corpus_version": corpus["version"],
        "catalog_id": catalog["catalog_id"],
        "catalog_version": catalog["version"],
        "seed": args.seed,
        "request_count": len(requests),
        "requests": list(requests),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"request_count": len(requests)}, sort_keys=True))


if __name__ == "__main__":
    main()
