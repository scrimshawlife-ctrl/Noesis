from __future__ import annotations

import hashlib

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.features import (
    FeatureHypothesis,
    evaluate_feature_controls,
    fit_sparse_dictionary,
    hypothesis_from_description,
    run_dictionary_consistency,
)
from noesis.settlement import EvidenceRef, SettlementRequest, settle_evidence


def _activations(n: int = 32, d: int = 8, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n, d))


def test_dictionary_reports_reconstruction_sparsity_and_dead_features():
    record = fit_sparse_dictionary(_activations(), n_features=6, seed=3)
    assert record.n_features == 6
    assert 0.0 <= record.reconstruction_r2 <= 1.0
    assert 0.0 <= record.mean_l0_fraction <= 1.0
    assert 0.0 <= record.dead_feature_rate <= 1.0
    assert record.training["seed"] == 3
    assert len(record.source_activation_sha256) == 64
    for result in record.metric_results:
        ContractRegistry("contracts").validate("metric-result", result)
        assert result["status"] == "MEASURED"


def test_dictionary_fit_is_seed_reproducible():
    x = _activations(seed=11)
    first = fit_sparse_dictionary(x, n_features=4, seed=7)
    second = fit_sparse_dictionary(x, n_features=4, seed=7)
    assert first.dictionary_sha256 == second.dictionary_sha256
    assert first.reconstruction_r2 == second.reconstruction_r2


def test_run_consistency_is_lower_when_training_is_resampled():
    x = _activations(n=40, d=6, seed=2)
    stable = run_dictionary_consistency(x, n_features=3, seeds=(1, 1), bootstrap=False)
    unstable = run_dictionary_consistency(x, n_features=3, seeds=(1, 2), bootstrap=True)
    assert stable["status"] == "MEASURED"
    assert unstable["value"] < stable["value"]
    ContractRegistry("contracts").validate("metric-result", stable)
    ContractRegistry("contracts").validate("metric-result", unstable)


def test_feature_description_is_hypothesis_not_dictionary_label():
    record = fit_sparse_dictionary(_activations(), n_features=3, seed=1)
    hypo = hypothesis_from_description(
        dictionary_id=record.dictionary_id,
        feature_index=0,
        description="tracks agency",
        proposer="operator:test",
    )
    assert isinstance(hypo, FeatureHypothesis)
    assert "tracks agency" not in record.as_dict().get("features", [{}])[0].values()
    assert hypo.description == "tracks agency"
    assert hypo.canonical is False


def test_nonfinite_activations_fail_closed():
    x = _activations()
    x[0, 0] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        fit_sparse_dictionary(x, n_features=2, seed=0)


def test_lexical_trigger_without_semantic_positive_weakens_candidate():
    trigger = np.ones((10, 4))
    semantic = np.zeros((10, 4))
    negative = np.zeros((10, 4))
    report = evaluate_feature_controls(
        feature_index=0,
        trigger_activations=trigger,
        semantic_positive_activations=semantic,
        negative_activations=negative,
    )
    assert report.decision in {"WEAKENED", "REJECTED"}
    assert report.reason
    assert report.mean_trigger > report.mean_semantic


def test_weakened_feature_settlement_is_not_observed():
    trigger = np.ones((8, 3))
    semantic = np.zeros((8, 3))
    negative = np.zeros((8, 3))
    report = evaluate_feature_controls(
        feature_index=0,
        trigger_activations=trigger,
        semantic_positive_activations=semantic,
        negative_activations=negative,
    )
    payload = report.reason.encode("utf-8")
    sha = hashlib.sha256(payload).hexdigest()
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-n2-001",
            proposition="Feature 0 tracks the hypothesized property.",
            evidence=(
                EvidenceRef(
                    id="ctrl-0",
                    sha256=sha,
                    role="contradicting",
                    kind="metric",
                    payload=payload,
                ),
            ),
            requested_label="OBSERVED",
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-n2-weak",
        )
    )
    assert settlement["label"] != "OBSERVED"
    assert settlement["promotion"] in {"HOLD_SHADOW", "REJECT"}
