from __future__ import annotations

import hashlib

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.features import detect_probe_leakage, evaluate_probe, train_linear_probe
from noesis.settlement import EvidenceRef, SettlementRequest, settle_evidence


def _separable(n: int = 40, d: int = 4, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, size=n)
    x = rng.normal(size=(n, d))
    x[:, 0] += 3.0 * y
    return x, y.astype(np.float64)


def test_probe_declares_partitions_regularization_and_baselines():
    x, y = _separable()
    train_ids = tuple(f"tr-{i}" for i in range(30))
    test_ids = tuple(f"te-{i}" for i in range(10))
    probe = train_linear_probe(
        x[:30],
        y[:30],
        x_held_out=x[30:],
        y_held_out=y[30:],
        train_ids=train_ids,
        test_ids=test_ids,
        regularization=0.1,
        seed=4,
    )
    assert probe.algorithm == "ridge-linear"
    assert probe.regularization == 0.1
    assert probe.train_partition_sha256
    assert probe.held_out_partition_sha256
    assert probe.train_partition_sha256 != probe.held_out_partition_sha256
    assert "majority" in probe.baselines
    assert "shuffled_labels" in probe.baselines
    ContractRegistry("contracts").validate("metric-result", probe.held_out_metric)
    assert probe.held_out_metric["status"] == "MEASURED"
    assert 0.0 <= probe.held_out_metric["value"] <= 1.0


def test_held_out_accuracy_beats_shuffled_baseline_on_separable_data():
    x, y = _separable(n=60, seed=3)
    probe = train_linear_probe(
        x[:40],
        y[:40],
        x_held_out=x[40:],
        y_held_out=y[40:],
        regularization=0.01,
        seed=1,
    )
    assert probe.held_out_metric["value"] > probe.baselines["shuffled_labels"]


def test_overlapping_ids_are_detected_as_leakage():
    report = detect_probe_leakage(
        train_ids=("a", "b", "c"),
        test_ids=("c", "d"),
    )
    assert report.leaked is True
    assert "c" in report.overlapping_ids


def test_identical_row_content_is_leakage_even_without_shared_ids():
    row = np.array([1.0, 2.0, 3.0])
    report = detect_probe_leakage(
        train_ids=("tr-0",),
        test_ids=("te-0",),
        train_activations=np.stack([row]),
        test_activations=np.stack([row]),
    )
    assert report.leaked is True
    assert report.reason


def test_leaked_probe_is_invalid_not_measured():
    x, y = _separable(n=20)
    with pytest.raises(ValueError, match="leakage"):
        train_linear_probe(
            x[:10],
            y[:10],
            x_held_out=x[:10],
            y_held_out=y[:10],
            train_ids=tuple(f"id-{i}" for i in range(10)),
            test_ids=tuple(f"id-{i}" for i in range(10)),
            regularization=0.1,
            seed=0,
        )


def test_probe_accuracy_alone_does_not_settle_observed_mechanism():
    x, y = _separable()
    probe = train_linear_probe(
        x[:30],
        y[:30],
        x_held_out=x[30:],
        y_held_out=y[30:],
        regularization=0.1,
        seed=2,
    )
    payload = str(probe.held_out_metric["value"]).encode("utf-8")
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-probe-001",
            proposition="The linear probe proves a causal agency mechanism.",
            evidence=(
                EvidenceRef(
                    id="probe-acc",
                    sha256=hashlib.sha256(payload).hexdigest(),
                    role="supporting",
                    kind="metric",
                    payload=payload,
                ),
            ),
            requested_label="OBSERVED",
            causal_claim=True,
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-probe-causal",
        )
    )
    assert settlement["label"] != "OBSERVED"
    assert settlement["promotion"] == "HOLD_SHADOW"


def test_evaluate_probe_rejects_nonfinite_inputs():
    x, y = _separable(n=12)
    probe = train_linear_probe(
        x[:8],
        y[:8],
        x_held_out=x[8:],
        y_held_out=y[8:],
        regularization=0.1,
        seed=0,
    )
    x[0, 0] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        evaluate_probe(probe, x, y)
