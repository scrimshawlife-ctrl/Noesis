from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from noesis.hyperlex.bundle import build_transform_request


@dataclass(frozen=True, slots=True)
class TransformSpec:
    transform_class: str
    semantic_intent: str
    expected_invariants: tuple[str, ...]
    expected_changed_attributes: tuple[str, ...]
    parameters: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class SourceFixtureSpec:
    fixture_id: str
    text: str


def compile_exp001_requests(
    sources: Iterable[SourceFixtureSpec],
    transforms: Iterable[TransformSpec],
    *,
    seed: int,
) -> tuple[dict[str, Any], ...]:
    """Compile operator-declared EXP-001 hypotheses into deterministic Hyperlex requests.

    This function does not infer semantic truth. It only preserves the hypotheses and
    controls explicitly supplied by the caller.
    """
    requests: list[dict[str, Any]] = []
    for source in sources:
        if not source.fixture_id:
            raise ValueError("source fixture_id must be non-empty")
        for spec in transforms:
            requests.append(
                build_transform_request(
                    source_fixture_id=source.fixture_id,
                    source_text=source.text,
                    transform_class=spec.transform_class,
                    semantic_intent=spec.semantic_intent,
                    expected_invariants=spec.expected_invariants,
                    expected_changed_attributes=spec.expected_changed_attributes,
                    seed=seed,
                    parameters=spec.parameters,
                )
            )
    ids = [request["request_id"] for request in requests]
    if len(ids) != len(set(ids)):
        raise ValueError("EXP-001 plan produced duplicate request identifiers")
    return tuple(requests)
