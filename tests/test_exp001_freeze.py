from datetime import UTC, datetime

import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.experiments.freeze import canonical_sha256, verify_freeze_receipt


CORPUS = {
    "schema_version": "1.0.0",
    "corpus_id": "exp001-sources",
    "version": "candidate-1",
    "data_classification": "PUBLIC_REPRODUCIBLE",
    "fixtures": [{
        "fixture_id": "fx-001",
        "text": "A crossed a boundary.",
        "sha256": "aa18ecc7d14927e4c1c5e2ab1fe0bf48bf9c42a9aafff738f5cd436a9723a0ad",
        "hypothesis_tags": ["boundary"],
        "partition": "discovery",
        "notes": None,
    }],
    "created_at_utc": datetime(2026, 9, 14, tzinfo=UTC).isoformat(),
    "operator_ref": None,
}

CATALOG = {
    "schema_version": "1.0.0",
    "catalog_id": "exp001-transforms",
    "version": "candidate-1",
    "transforms": [{
        "transform_class": "literal_paraphrase",
        "semantic_intent": "preserve the declared event",
        "expected_invariants": ["event"],
        "expected_changed_attributes": ["lexical surface"],
        "role": "transform",
    }],
}


def receipt() -> dict:
    return {
        "schema_version": "1.0.0",
        "receipt_id": "exp001-freeze-2026-09-14",
        "decision": "APPROVED",
        "operator_ref": "operator:test",
        "decided_at_utc": "2026-09-14T00:00:00+00:00",
        "scope": "LAB only",
        "constraints": ["No FIELD execution"],
        "corpus_id": CORPUS["corpus_id"],
        "corpus_version": CORPUS["version"],
        "corpus_sha256": canonical_sha256(CORPUS),
        "catalog_id": CATALOG["catalog_id"],
        "catalog_version": CATALOG["version"],
        "catalog_sha256": canonical_sha256(CATALOG),
    }


def test_freeze_receipt_is_schema_valid_and_binds_exact_inputs():
    approval = receipt()
    ContractRegistry("contracts").validate("exp001-freeze-receipt", approval)
    verify_freeze_receipt(CORPUS, CATALOG, approval)


def test_freeze_receipt_rejects_modified_corpus():
    changed = {**CORPUS, "version": "candidate-2"}
    with pytest.raises(ValueError, match="corpus_version, corpus_sha256"):
        verify_freeze_receipt(changed, CATALOG, receipt())


def test_freeze_receipt_rejects_modified_catalog():
    changed = {**CATALOG, "version": "candidate-2"}
    with pytest.raises(ValueError, match="catalog_version, catalog_sha256"):
        verify_freeze_receipt(CORPUS, changed, receipt())
