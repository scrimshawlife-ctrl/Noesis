from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from typing import Iterable


@dataclass(frozen=True, slots=True)
class CorpusFixture:
    fixture_id: str
    text: str
    hypothesis_tags: tuple[str, ...]
    partition: str
    notes: str | None = None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()


def freeze_source_corpus(
    *,
    corpus_id: str,
    version: str,
    fixtures: Iterable[CorpusFixture],
    data_classification: str = "PUBLIC_REPRODUCIBLE",
    operator_ref: str | None = None,
    created_at: datetime | None = None,
) -> dict:
    items = tuple(fixtures)
    if not corpus_id or not version:
        raise ValueError("corpus_id and version must be non-empty")
    if not items:
        raise ValueError("source corpus must contain at least one fixture")
    valid_partitions = {"discovery", "confirmation", "control"}
    seen_ids: set[str] = set()
    serialized = []
    for fixture in items:
        if not fixture.fixture_id or not fixture.text:
            raise ValueError("fixture_id and text must be non-empty")
        if fixture.fixture_id in seen_ids:
            raise ValueError(f"duplicate fixture_id: {fixture.fixture_id}")
        if fixture.partition not in valid_partitions:
            raise ValueError(f"invalid partition: {fixture.partition}")
        seen_ids.add(fixture.fixture_id)
        serialized.append(
            {
                "fixture_id": fixture.fixture_id,
                "text": fixture.text,
                "sha256": fixture.sha256,
                "hypothesis_tags": list(fixture.hypothesis_tags),
                "partition": fixture.partition,
                "notes": fixture.notes,
            }
        )
    timestamp = created_at or datetime.now(timezone.utc)
    return {
        "schema_version": "1.0.0",
        "corpus_id": corpus_id,
        "version": version,
        "data_classification": data_classification,
        "fixtures": serialized,
        "created_at_utc": timestamp.isoformat(),
        "operator_ref": operator_ref,
    }
