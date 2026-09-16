import json
from datetime import UTC, datetime

import pytest

from noesis.adapters.fake import DeterministicFakeAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.capture.executor import ManifestExecutor
from noesis.capture.runner import CaptureRunner
from noesis.contracts.registry import ContractRegistry
from noesis.domain.models import InputFixture

FIXED_TIME = datetime(2026, 9, 13, 23, 0, tzinfo=UTC)


def manifest():
    return json.loads(open("examples/manifests/slice-001.json", encoding="utf-8").read())


def test_manifest_executor_rejects_unauthorized_field_scope(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"))
    field_manifest = manifest()
    field_manifest["environment_requirements"] = {"execution_scope": "FIELD"}
    with pytest.raises(ValueError, match="FIELD"):
        executor.execute(field_manifest, [InputFixture("fixture-001", "stable fixture")], "run-field")


def test_manifest_executor_allows_authorized_n5(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    runner = CaptureRunner(adapter, store, clock=lambda: FIXED_TIME)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"), runner)
    n5_manifest = manifest()
    n5_manifest["environment_requirements"] = {"execution_scope": "N5"}
    report = executor.execute(
        n5_manifest,
        [InputFixture("fixture-001", "stable fixture")],
        "run-n5",
        authorization={"scope": "N5", "operator": "owner"},
    )
    assert len(report.observations) == 1
    assert report.failures == ()


def test_manifest_executor_emits_observation(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    runner = CaptureRunner(adapter, store, clock=lambda: FIXED_TIME)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"), runner)
    report = executor.execute(manifest(), [InputFixture("fixture-001", "stable fixture")], "run-001")
    assert len(report.observations) == 1
    assert report.failures == ()


def test_manifest_executor_rejects_secret_like_fixture_text(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"))
    report = executor.execute(
        manifest(),
        [InputFixture("fixture-001", "token=ghp_exampleExampleExampleExample0001")],
        "run-secret",
    )
    assert report.observations == ()
    assert len(report.failures) == 1
    assert "secret" in report.failures[0]["message"].lower() or "ghp_" in report.failures[0]["message"]


def test_manifest_executor_rejects_prohibited_classification(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"))
    report = executor.execute(
        manifest(),
        [InputFixture("fixture-001", "stable fixture", data_classification="PROHIBITED")],
        "run-prohibited",
    )
    assert report.observations == ()
    assert any("PROHIBITED" in item["message"] for item in report.failures)


def test_manifest_executor_persists_missing_fixture_as_failure(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"))
    report = executor.execute(manifest(), [], "run-missing")
    assert report.observations == ()
    assert len(report.failures) == 1
    assert report.failures[0]["error_type"] == "KeyError"
    assert report.failures[0]["provenance"] == "OBSERVED"
