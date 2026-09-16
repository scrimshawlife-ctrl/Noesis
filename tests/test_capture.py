from datetime import UTC, datetime

from noesis.adapters.fake import DeterministicFakeAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.capture.runner import CaptureRunner
from noesis.contracts.registry import ContractRegistry
from noesis.domain.models import CaptureRequest, RepresentationSite

FIXED_TIME = datetime(2026, 9, 13, 23, 0, tzinfo=UTC)


def test_capture_replays_identically(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path / "artifacts")
    runner = CaptureRunner(adapter, store, clock=lambda: FIXED_TIME)
    request = CaptureRequest(
        fixture_id="fixture-001",
        text="authority persists across surface form",
        site=RepresentationSite(kind="hidden_state", layer=2, token_index=-1),
        seed=42,
    )

    first = runner.run("EXP-SLICE-001", "run-001", request)
    second = runner.run("EXP-SLICE-001", "run-001", request)

    assert first == second
    assert first["artifact"]["sha256"] == second["artifact"]["sha256"]
    assert first["provenance"] == "OBSERVED"
    assert first["environment"]["fingerprint"]
    assert first["environment"]["fingerprint"] == second["environment"]["fingerprint"]

    registry = ContractRegistry("contracts")
    registry.validate("observation", first)


def test_seed_changes_artifact(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    runner = CaptureRunner(adapter, ContentAddressedStore(tmp_path), clock=lambda: FIXED_TIME)
    base = dict(
        fixture_id="fixture-001",
        text="same input",
        site=RepresentationSite(kind="embedding", token_index=-1),
    )
    a = runner.run("EXP", "run-a", CaptureRequest(seed=1, **base))
    b = runner.run("EXP", "run-b", CaptureRequest(seed=2, **base))
    assert a["artifact"]["sha256"] != b["artifact"]["sha256"]
