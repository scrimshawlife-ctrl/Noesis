import json
from datetime import UTC, datetime

from noesis.adapters.fake import DeterministicFakeAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.capture.executor import ManifestExecutor
from noesis.capture.runner import CaptureRunner
from noesis.contracts.registry import ContractRegistry
from noesis.domain.models import InputFixture

FIXED_TIME = datetime(2026, 9, 13, 23, 0, tzinfo=UTC)


def manifest():
    return json.loads(open("examples/manifests/slice-001.json", encoding="utf-8").read())


def test_manifest_executor_emits_observation(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    runner = CaptureRunner(adapter, store, clock=lambda: FIXED_TIME)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"), runner)
    report = executor.execute(manifest(), [InputFixture("fixture-001", "stable fixture")], "run-001")
    assert len(report.observations) == 1
    assert report.failures == ()


def test_manifest_executor_persists_missing_fixture_as_failure(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path)
    executor = ManifestExecutor(adapter, store, ContractRegistry("contracts"))
    report = executor.execute(manifest(), [], "run-missing")
    assert report.observations == ()
    assert len(report.failures) == 1
    assert report.failures[0]["error_type"] == "KeyError"
    assert report.failures[0]["provenance"] == "OBSERVED"
