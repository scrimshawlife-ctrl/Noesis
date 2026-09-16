from __future__ import annotations

import pytest

from noesis.artifacts.store import ContentAddressedStore
from noesis.security import (
    authorize_scope,
    classify_fixture,
    record_incident,
    scan_secrets,
    verify_artifact_integrity,
)
from noesis.settlement import supersede_settlement


def test_secret_scan_catches_synthetic_credential_patterns():
    hits = scan_secrets("token=ghp_exampleExampleExampleExample0001\naws_key=AKIAIOSFODNN7EXAMPLE")
    assert any("ghp_" in hit or "github" in hit.lower() for hit in hits)
    assert any("AKIA" in hit or "aws" in hit.lower() for hit in hits)
    assert scan_secrets("public fixture about agency") == ()


def test_prohibited_classification_is_rejected():
    with pytest.raises(ValueError, match="PROHIBITED"):
        classify_fixture({"text": "ok", "data_classification": "PROHIBITED"})


def test_sensitive_requires_retention_and_access_scope():
    with pytest.raises(ValueError, match="retention"):
        classify_fixture({"text": "vet notes", "data_classification": "SENSITIVE"})
    record = classify_fixture(
        {
            "text": "vet notes",
            "data_classification": "SENSITIVE",
            "retention": "30d",
            "access_scope": "LAB",
        }
    )
    assert record["data_classification"] == "SENSITIVE"


def test_unauthorized_field_and_n5_are_rejected():
    with pytest.raises(ValueError, match="FIELD"):
        authorize_scope("FIELD", authorization=None)
    with pytest.raises(ValueError, match="N5"):
        authorize_scope("N5", authorization={"scope": "LAB"})
    assert authorize_scope("LAB", authorization=None) == "LAB"
    assert authorize_scope("N5", authorization={"scope": "N5", "operator": "owner"}) == "N5"


def test_artifact_substitution_is_detected(tmp_path):
    store = ContentAddressedStore(tmp_path / "artifacts")
    sha, path = store.put_bytes(b"tensor-bytes", "bin")
    verify_artifact_integrity(store, path, sha)
    path.write_bytes(b"substituted")
    with pytest.raises(RuntimeError, match="hash mismatch"):
        verify_artifact_integrity(store, path, sha)


def test_synthetic_incident_uses_supersession_without_deleting_original():
    original = {
        "settlement_id": "set-incident-1",
        "proposition": "synthetic",
    }
    snapshot = dict(original)
    incident = record_incident(
        original,
        reason="synthetic credential detected in fixture",
        actor="operator:security",
        successor_ref="set-incident-2",
    )
    assert original == snapshot
    assert incident["reason"]
    supersede_settlement(
        {"settlement_id": original["settlement_id"]},
        successor_ref=incident["incident_id"],
        reason=incident["reason"],
        actor="operator:security",
        created_at="2026-09-16T00:00:00Z",
        supersession_id="sup-sec-1",
    )
    assert original["settlement_id"] == "set-incident-1"
