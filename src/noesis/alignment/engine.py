from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import numpy as np

from noesis.contracts.registry import validate_contract
from noesis.metrics.core import linear_cka

_CREATED = datetime(2026, 9, 16, tzinfo=UTC).isoformat()
_SUPPORT_MARGIN = 0.2


@dataclass(frozen=True, slots=True)
class AlignmentFit:
    map: dict[str, Any]
    weights: np.ndarray
    validation_metric: dict[str, Any]
    test_metric: dict[str, Any]
    null_metric: dict[str, Any]
    shift_metric: dict[str, Any]


def fit_linear_alignment(
    *,
    source_train,
    target_train,
    source_validation,
    target_validation,
    source_test,
    target_test,
    source_shift,
    target_shift,
    seed: int,
    source_space: str = "source",
    target_space: str = "target",
) -> AlignmentFit:
    train_src, train_tgt = _pair(source_train, target_train, "train")
    val_src, val_tgt = _pair(source_validation, target_validation, "validation")
    test_src, test_tgt = _pair(source_test, target_test, "test")
    shift_src, shift_tgt = _pair(source_shift, target_shift, "shift")
    _assert_disjoint(train_src, val_src, test_src)

    weights = _least_squares(train_src, train_tgt)
    null_target = train_tgt.copy()
    np.random.default_rng(seed).shuffle(null_target)
    null_weights = _least_squares(train_src, null_target)

    validation = _cka_metric("validation_cka", val_src @ weights, val_tgt, "val")
    test = _cka_metric("held_out_cka", test_src @ weights, test_tgt, "test")
    null = _cka_metric("null_shuffled_cka", test_src @ null_weights, test_tgt, "null")
    shift = _cka_metric("shift_cka", shift_src @ weights, shift_tgt, "shift")

    if test["value"] >= null["value"] + _SUPPORT_MARGIN:
        status = "SUPPORTED"
    elif test["value"] > null["value"]:
        status = "WEAK"
    else:
        status = "REJECTED"

    artifact_hash = hashlib.sha256(np.ascontiguousarray(weights).tobytes()).hexdigest()
    alignment_id = f"align-{artifact_hash[:12]}"
    record = {
        "schema_version": "1.0.0",
        "alignment_id": alignment_id,
        "source_space": source_space,
        "target_space": target_space,
        "algorithm": "least-squares",
        "hyperparameters": {"bias": False, "seed": seed},
        "train_partition_hash": _partition_hash(train_src, train_tgt),
        "validation_partition_hash": _partition_hash(val_src, val_tgt),
        "test_partition_hash": _partition_hash(test_src, test_tgt),
        "artifact_ref": f"sha256:{artifact_hash}",
        "artifact_hash": artifact_hash,
        "validation_metric_ids": [validation["metric_result_id"]],
        "test_metric_ids": [test["metric_result_id"]],
        "null_metric_ids": [null["metric_result_id"]],
        "shift_metric_ids": [shift["metric_result_id"]],
        "status": status,
        "limitations": [
            "geometric alignment is not semantic equivalence",
            "test and shift partitions were not used to fit the map",
        ],
        "created_at_utc": _CREATED,
    }
    validate_contract("alignment-map", record)
    return AlignmentFit(
        map=record,
        weights=weights,
        validation_metric=validation,
        test_metric=test,
        null_metric=null,
        shift_metric=shift,
    )


def _pair(source, target, name: str) -> tuple[np.ndarray, np.ndarray]:
    src, tgt = _matrix(source), _matrix(target)
    if src.shape[0] != tgt.shape[0]:
        raise ValueError(f"{name} source/target sample counts must match")
    if src.shape[1] != tgt.shape[1]:
        raise ValueError(f"{name} source/target widths must match for least-squares alignment")
    return src, tgt


def _matrix(values) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[1] == 0:
        raise ValueError("expected a non-empty 2D representation matrix")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("activations contain non-finite values")
    return matrix


def _row_hashes(matrix: np.ndarray) -> set[str]:
    return {
        hashlib.sha256(np.ascontiguousarray(row).tobytes()).hexdigest()
        for row in matrix
    }


def _assert_disjoint(train: np.ndarray, validation: np.ndarray, test: np.ndarray) -> None:
    train_rows, val_rows, test_rows = _row_hashes(train), _row_hashes(validation), _row_hashes(test)
    if train_rows & test_rows or train_rows & val_rows or val_rows & test_rows:
        raise ValueError("alignment leakage: train/validation/test partitions are not disjoint")


def _least_squares(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    weights, *_ = np.linalg.lstsq(source, target, rcond=None)
    return np.asarray(weights, dtype=np.float64)


def _partition_hash(source: np.ndarray, target: np.ndarray) -> str:
    payload = np.ascontiguousarray(source).tobytes() + np.ascontiguousarray(target).tobytes()
    return hashlib.sha256(payload).hexdigest()


def _cka_metric(name: str, left: np.ndarray, right: np.ndarray, owner: str) -> dict[str, Any]:
    value = linear_cka(left, right)
    result = {
        "schema_version": "1.0.0",
        "metric_result_id": f"{name}-{owner}",
        "metric_name": name,
        "metric_version": "0.1.0",
        "input_observation_ids": [f"alignment-{owner}"],
        "preprocessing_id": "least-squares-alignment",
        "status": "MEASURED",
        "value": value,
        "uncertainty": None,
        "tolerance": None,
        "null_control_ids": [],
        "limitations": ["CKA does not measure semantic equivalence"],
        "created_at_utc": _CREATED,
    }
    validate_contract("metric-result", result)
    return result
