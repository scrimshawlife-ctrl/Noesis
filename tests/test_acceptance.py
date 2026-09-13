import pytest

from noesis.acceptance import N01AcceptanceConfig, run_n01_acceptance
from noesis.adapters.fake import DeterministicFakeAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.domain.models import RepresentationSite


def test_n01_acceptance_accepts_deterministic_embedding_and_hidden_state(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path / "artifacts")
    config = N01AcceptanceConfig(
        experiment_id="test-n01",
        fixture_id="fixture-001",
        text="Stable fixture",
        sites=(
            RepresentationSite(kind="embedding", token_index=-1),
            RepresentationSite(kind="hidden_state", layer=1, token_index=-1),
        ),
        seed=42,
        repeats=2,
    )
    evidence = run_n01_acceptance(adapter, store, config)
    assert evidence["gate_decisions"] == {"AC-N0": "ACCEPT", "AC-N1": "ACCEPT"}
    assert all(result["decision"] == "ACCEPT" for result in evidence["site_results"])
    assert all(result["comparisons"][0]["cosine"] == pytest.approx(1.0) for result in evidence["site_results"])


def test_n01_acceptance_without_hidden_state_keeps_n1_not_computable(tmp_path):
    adapter = DeterministicFakeAdapter(dimensions=8)
    store = ContentAddressedStore(tmp_path / "artifacts")
    config = N01AcceptanceConfig(
        experiment_id="test-n01",
        fixture_id="fixture-001",
        text="Stable fixture",
        sites=(RepresentationSite(kind="embedding", token_index=-1),),
        repeats=2,
    )
    evidence = run_n01_acceptance(adapter, store, config)
    assert evidence["gate_decisions"]["AC-N0"] == "ACCEPT"
    assert evidence["gate_decisions"]["AC-N1"] == "NOT_COMPUTABLE"
