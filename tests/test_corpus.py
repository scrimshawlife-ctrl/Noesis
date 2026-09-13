from datetime import UTC, datetime

import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.experiments.corpus import CorpusFixture, freeze_source_corpus


def test_freeze_source_corpus_is_hash_stable_and_schema_valid():
    corpus = freeze_source_corpus(
        corpus_id="exp001-sources",
        version="draft-1",
        fixtures=(
            CorpusFixture(
                fixture_id="fx-001",
                text="Operator supplied fixture.",
                hypothesis_tags=("example",),
                partition="discovery",
            ),
        ),
        created_at=datetime(2026, 9, 13, tzinfo=UTC),
    )
    assert len(corpus["fixtures"][0]["sha256"]) == 64
    registry = ContractRegistry("contracts")
    registry.validate("exp001-source-corpus", corpus)


def test_freeze_source_corpus_rejects_duplicate_ids():
    fixture = CorpusFixture(
        fixture_id="fx-001",
        text="One",
        hypothesis_tags=(),
        partition="control",
    )
    with pytest.raises(ValueError, match="duplicate fixture_id"):
        freeze_source_corpus(corpus_id="c", version="1", fixtures=(fixture, fixture))
