from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any, Iterable

from noesis.hyperlex.base import HyperlexAdapter
from noesis.hyperlex.materialize import MaterializedFixture, materialize_transform_result


CANONICAL_TRANSFORM_CLASSES = (
    "literal_paraphrase",
    "slang",
    "metaphor",
    "mythic",
    "symbolic",
    "technical",
    "multilingual",
    "negation",
    "role_reversal",
    "adversarial_paraphrase",
)

CONTROL_TRANSFORM_CLASSES = (
    "lexical_trigger_control",
    "surface_shuffle_control",
    "semantic_mismatch_control",
)


def stable_request_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "hxreq-" + hashlib.sha256(canonical).hexdigest()[:20]


def build_transform_request(
    *,
    source_fixture_id: str,
    source_text: str,
    transform_class: str,
    semantic_intent: str,
    expected_invariants: Iterable[str],
    expected_changed_attributes: Iterable[str],
    seed: int,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = {
        "schema_version": "1.0.0",
        "source_fixture_id": source_fixture_id,
        "source_text": source_text,
        "transform_class": transform_class,
        "semantic_intent": semantic_intent,
        "expected_invariants": list(expected_invariants),
        "expected_changed_attributes": list(expected_changed_attributes),
        "seed": seed,
        "parameters": parameters or {},
    }
    body["request_id"] = stable_request_id(body)
    return body


def generate_transform_bundle(
    adapter: HyperlexAdapter,
    requests: Iterable[dict[str, Any]],
) -> tuple[MaterializedFixture, ...]:
    fixtures: list[MaterializedFixture] = []
    seen_ids: set[str] = set()
    for req in requests:
        result = adapter.transform(dict(req))
        fixture = materialize_transform_result(result)
        if fixture.fixture_id in seen_ids:
            raise ValueError(f"duplicate materialized fixture id: {fixture.fixture_id}")
        seen_ids.add(fixture.fixture_id)
        fixtures.append(fixture)
    return tuple(fixtures)


def bundle_manifest(fixtures: Iterable[MaterializedFixture]) -> dict[str, Any]:
    rows = [asdict(fixture) for fixture in fixtures]
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return {
        "schema_version": "1.0.0",
        "fixture_count": len(rows),
        "bundle_sha256": hashlib.sha256(payload).hexdigest(),
        "fixtures": rows,
    }
