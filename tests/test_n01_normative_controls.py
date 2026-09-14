from __future__ import annotations

import numpy as np
import pytest

from noesis.acceptance import N01AcceptanceConfig, run_n01_acceptance
from noesis.adapters.base import UnsupportedRepresentationSite
from noesis.adapters.fake import DeterministicFakeAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.domain.models import AdapterCapabilities, CaptureRequest, ModelIdentity, RepresentationSite
from noesis.metrics.core import linear_cka, permutation_null


class FailingAdapter:
    def __init__(self, error: Exception):
        self._error = error
        self._identity = ModelIdentity("failing", "immutable-revision", "immutable-revision")
        self._capabilities = AdapterCapabilities(frozenset({"embedding", "hidden_state"}))

    @property
    def identity(self):
        return self._identity

    @property
    def capabilities(self):
        return self._capabilities

    def capture(self, request: CaptureRequest):
        raise self._error


def config(*sites: RepresentationSite) -> N01AcceptanceConfig:
    return N01AcceptanceConfig(
        experiment_id="N01-NORMATIVE-CONTROLS",
        fixture_id="fixture-normative",
        text="Stable public fixture",
        sites=sites,
        seed=7,
        repeats=2,
    )


def test_acceptance_persists_only_declared_sites_and_verifies_artifacts(tmp_path):
    sites = (
        RepresentationSite(kind="embedding", token_index=-1),
        RepresentationSite(kind="hidden_state", layer=1, token_index=-1),
    )
    evidence = run_n01_acceptance(
        DeterministicFakeAdapter(dimensions=8),
        ContentAddressedStore(tmp_path / "artifacts"),
        config(*sites),
    )
    assert [row["site"] for row in evidence["site_results"]] == [site.key() for site in sites]
    assert evidence["gate_decisions"] == {"AC-N0": "ACCEPT", "AC-N1": "ACCEPT"}
    assert all(not row["failures"] for row in evidence["site_results"])


def test_content_addressed_store_detects_post_write_corruption(tmp_path):
    store = ContentAddressedStore(tmp_path)
    sha, path = store.put_bytes(b"trusted", "bin")
    assert store.verify_path(path, sha) is True
    path.write_bytes(b"tampered")
    with pytest.raises(RuntimeError, match="artifact hash mismatch"):
        store.verify_path(path, sha)


def test_nonfinite_vectors_fail_before_artifact_acceptance(tmp_path):
    store = ContentAddressedStore(tmp_path)
    with pytest.raises(ValueError, match="non-finite"):
        store.put_vector((1.0, float("nan")))
    with pytest.raises(ValueError, match="non-finite"):
        store.put_vector((1.0, float("inf")))


@pytest.mark.parametrize(
    "error,error_class",
    [
        (UnsupportedRepresentationSite("hidden_state:999"), "UnsupportedRepresentationSite"),
        (MemoryError("synthetic OOM"), "MemoryError"),
    ],
)
def test_adapter_failures_are_explicit_in_acceptance_evidence(tmp_path, error, error_class):
    site = RepresentationSite(kind="hidden_state", layer=1, token_index=-1)
    evidence = run_n01_acceptance(
        FailingAdapter(error),
        ContentAddressedStore(tmp_path),
        config(site),
    )
    row = evidence["site_results"][0]
    assert row["decision"] == "REJECT"
    assert len(row["failures"]) == 2
    assert all(item["error_class"] == error_class for item in row["failures"])
    assert evidence["gate_decisions"] == {"AC-N0": "REJECT", "AC-N1": "REJECT"}


def test_permutation_null_control_is_implemented_and_seed_reproducible():
    x = np.asarray([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 1.0]])
    first = permutation_null(x, x, linear_cka, repeats=16, seed=11)
    second = permutation_null(x, x, linear_cka, repeats=16, seed=11)
    assert np.array_equal(first, second)
    assert first.shape == (16,)
