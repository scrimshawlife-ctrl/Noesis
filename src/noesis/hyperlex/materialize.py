from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from noesis.contracts.registry import validate_contract


@dataclass(frozen=True, slots=True)
class MaterializedFixture:
    fixture_id: str
    source_fixture_id: str
    transform_id: str
    text: str
    sha256: str
    transform_class: str
    semantic_intent: str
    expected_invariants: tuple[str, ...]
    expected_changed_attributes: tuple[str, ...]


def materialize_transform_result(result: dict[str, Any]) -> MaterializedFixture:
    validate_contract("hyperlex-transform-result", result)
    observed_sha = hashlib.sha256(result["output_text"].encode("utf-8")).hexdigest()
    if observed_sha != result["transform_sha256"]:
        raise ValueError("Hyperlex transform output hash mismatch")
    return MaterializedFixture(
        fixture_id=f"fixture-{result['transform_id']}",
        source_fixture_id=result["source_fixture_id"],
        transform_id=result["transform_id"],
        text=result["output_text"],
        sha256=observed_sha,
        transform_class=result["transform_class"],
        semantic_intent=result["semantic_intent"],
        expected_invariants=tuple(result["expected_invariants"]),
        expected_changed_attributes=tuple(result["expected_changed_attributes"]),
    )
