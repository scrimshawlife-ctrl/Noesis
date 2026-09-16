from __future__ import annotations

import numpy as np
import pytest

from noesis.alignment import fit_linear_alignment
from noesis.contracts.registry import ContractRegistry
from noesis.metrics.core import linear_cka


def _paired_spaces(n: int = 80, d: int = 4, seed: int = 0, shift: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    source = rng.normal(size=(n, d))
    rotate = np.linalg.qr(rng.normal(size=(d, d)))[0]
    target = source @ rotate + shift
    return source, target


def test_known_linear_map_is_supported_and_schema_valid():
    source, target = _paired_spaces()
    result = fit_linear_alignment(
        source_train=source[:40],
        target_train=target[:40],
        source_validation=source[40:56],
        target_validation=target[40:56],
        source_test=source[56:72],
        target_test=target[56:72],
        source_shift=source[72:] + 1.5,
        target_shift=target[72:] + 1.5,
        seed=1,
    )
    ContractRegistry("contracts").validate("alignment-map", result.map)
    assert result.map["status"] == "SUPPORTED"
    assert result.map["algorithm"] == "least-squares"
    assert result.test_metric["status"] == "MEASURED"
    assert result.null_metric["status"] == "MEASURED"
    assert result.shift_metric["status"] == "MEASURED"
    assert result.test_metric["value"] > result.null_metric["value"]
    mapped = source[56:72] @ result.weights
    assert linear_cka(mapped, target[56:72]) == pytest.approx(result.test_metric["value"], abs=1e-9)


def test_shuffled_pairing_does_not_beat_null_threshold():
    source, target = _paired_spaces(seed=4)
    rng = np.random.default_rng(9)
    shuffled = target[rng.permutation(target.shape[0])]
    result = fit_linear_alignment(
        source_train=source[:40],
        target_train=shuffled[:40],
        source_validation=source[40:56],
        target_validation=shuffled[40:56],
        source_test=source[56:72],
        target_test=shuffled[56:72],
        source_shift=source[72:],
        target_shift=shuffled[72:],
        seed=2,
    )
    assert result.map["status"] in {"WEAK", "REJECTED"}
    assert result.test_metric["value"] <= result.null_metric["value"] + 0.15


def test_train_validation_test_hashes_are_disjoint():
    source, target = _paired_spaces()
    result = fit_linear_alignment(
        source_train=source[:40],
        target_train=target[:40],
        source_validation=source[40:56],
        target_validation=target[40:56],
        source_test=source[56:72],
        target_test=target[56:72],
        source_shift=source[72:],
        target_shift=target[72:],
        seed=0,
    )
    hashes = {
        result.map["train_partition_hash"],
        result.map["validation_partition_hash"],
        result.map["test_partition_hash"],
    }
    assert len(hashes) == 3


def test_semantic_equivalence_is_not_populated_from_geometry():
    source, target = _paired_spaces()
    result = fit_linear_alignment(
        source_train=source[:40],
        target_train=target[:40],
        source_validation=source[40:56],
        target_validation=target[40:56],
        source_test=source[56:72],
        target_test=target[56:72],
        source_shift=source[72:],
        target_shift=target[72:],
        seed=0,
    )
    assert "semantic_equivalence" not in result.map
    assert all("semantic" not in key for key in result.map)


def test_overlapping_test_rows_are_invalidated():
    source, target = _paired_spaces(n=30)
    with pytest.raises(ValueError, match="leakage"):
        fit_linear_alignment(
            source_train=source[:20],
            target_train=target[:20],
            source_validation=source[10:20],
            target_validation=target[10:20],
            source_test=source[:10],
            target_test=target[:10],
            source_shift=source[20:],
            target_shift=target[20:],
            seed=0,
        )


def test_nonfinite_inputs_are_not_computable():
    source, target = _paired_spaces(n=24)
    source[0, 0] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        fit_linear_alignment(
            source_train=source[:12],
            target_train=target[:12],
            source_validation=source[12:16],
            target_validation=target[12:16],
            source_test=source[16:20],
            target_test=target[16:20],
            source_shift=source[20:],
            target_shift=target[20:],
            seed=0,
        )
