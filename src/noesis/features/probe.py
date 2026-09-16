from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Sequence

import numpy as np

from noesis.contracts.registry import validate_contract

_EPS = 1e-12
_CREATED = datetime(2026, 9, 16, tzinfo=UTC).isoformat()


@dataclass(frozen=True, slots=True)
class LeakageReport:
    leaked: bool
    overlapping_ids: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class ProbeRecord:
    probe_id: str
    probe_sha256: str
    algorithm: str
    regularization: float
    train_partition_sha256: str
    held_out_partition_sha256: str
    baselines: dict[str, float]
    weights: tuple[float, ...]
    held_out_metric: dict[str, Any]
    training: dict[str, Any]


def detect_probe_leakage(
    *,
    train_ids: Sequence[str],
    test_ids: Sequence[str],
    train_activations=None,
    test_activations=None,
) -> LeakageReport:
    overlap = tuple(sorted(set(train_ids) & set(test_ids)))
    if overlap:
        return LeakageReport(
            leaked=True,
            overlapping_ids=overlap,
            reason="train and held-out partitions share observation IDs",
        )
    if train_activations is not None and test_activations is not None:
        train_rows = {_row_hash(row) for row in _matrix(train_activations)}
        test_rows = {_row_hash(row) for row in _matrix(test_activations)}
        shared = train_rows & test_rows
        if shared:
            return LeakageReport(
                leaked=True,
                overlapping_ids=(),
                reason="train and held-out partitions share identical activation rows",
            )
    return LeakageReport(leaked=False, overlapping_ids=(), reason="")


def train_linear_probe(
    x_train,
    y_train,
    *,
    x_held_out,
    y_held_out,
    regularization: float,
    seed: int,
    train_ids: Sequence[str] | None = None,
    test_ids: Sequence[str] | None = None,
) -> ProbeRecord:
    train_x = _matrix(x_train)
    test_x = _matrix(x_held_out)
    train_y = _labels(y_train)
    test_y = _labels(y_held_out)
    if train_x.shape[0] != train_y.shape[0] or test_x.shape[0] != test_y.shape[0]:
        raise ValueError("activations and labels must have equal sample counts")
    if train_x.shape[1] != test_x.shape[1]:
        raise ValueError("train and held-out activations must have equal width")
    if regularization < 0:
        raise ValueError("regularization must be >= 0")

    train_ids = tuple(train_ids) if train_ids is not None else tuple(_row_hash(row) for row in train_x)
    test_ids = tuple(test_ids) if test_ids is not None else tuple(_row_hash(row) for row in test_x)
    if len(train_ids) != train_x.shape[0] or len(test_ids) != test_x.shape[0]:
        raise ValueError("partition IDs must align with samples")

    leakage = detect_probe_leakage(
        train_ids=train_ids,
        test_ids=test_ids,
        train_activations=train_x,
        test_activations=test_x,
    )
    if leakage.leaked:
        raise ValueError(f"probe leakage: {leakage.reason}")

    weights = _ridge_weights(train_x, train_y, regularization)
    held_out_acc = _accuracy(test_x, test_y, weights)
    majority = _majority_accuracy(train_y, test_y)
    shuffled = _shuffled_baseline(train_x, train_y, test_x, test_y, regularization, seed)

    train_sha = _partition_sha256(train_x, train_y, train_ids)
    test_sha = _partition_sha256(test_x, test_y, test_ids)
    weight_sha = hashlib.sha256(np.asarray(weights, dtype=np.float64).tobytes()).hexdigest()
    probe_id = f"probe-{weight_sha[:12]}"
    metric = _metric_result(
        name="held_out_accuracy",
        value=held_out_acc,
        owner_id=probe_id,
        inputs=(f"train:{train_sha[:16]}", f"heldout:{test_sha[:16]}"),
        limitations=(
            "probe accuracy is not mechanistic or causal evidence",
            "held-out evaluation only; training accuracy is not reported as evidence",
        ),
    )
    return ProbeRecord(
        probe_id=probe_id,
        probe_sha256=weight_sha,
        algorithm="ridge-linear",
        regularization=float(regularization),
        train_partition_sha256=train_sha,
        held_out_partition_sha256=test_sha,
        baselines={"majority": majority, "shuffled_labels": shuffled},
        weights=tuple(float(v) for v in weights),
        held_out_metric=metric,
        training={
            "seed": seed,
            "n_train": int(train_x.shape[0]),
            "n_held_out": int(test_x.shape[0]),
            "n_dims": int(train_x.shape[1]),
            "leakage_controls": ("disjoint_ids", "disjoint_row_hashes"),
        },
    )


def evaluate_probe(probe: ProbeRecord, activations, labels) -> dict[str, Any]:
    matrix = _matrix(activations)
    y = _labels(labels)
    if matrix.shape[0] != y.shape[0]:
        raise ValueError("activations and labels must have equal sample counts")
    if matrix.shape[1] + 1 != len(probe.weights):
        raise ValueError("activation width does not match probe weights")
    accuracy = _accuracy(matrix, y, np.asarray(probe.weights, dtype=np.float64))
    return _metric_result(
        name="probe_accuracy",
        value=accuracy,
        owner_id=probe.probe_id,
        inputs=(f"probe:{probe.probe_sha256[:16]}",),
        limitations=("probe accuracy is not mechanistic or causal evidence",),
    )


def _matrix(values) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[1] == 0:
        raise ValueError("expected a non-empty 2D activation matrix")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("activations contain non-finite values")
    return matrix


def _labels(values) -> np.ndarray:
    labels = np.asarray(values, dtype=np.float64).reshape(-1)
    if labels.size == 0:
        raise ValueError("labels must be non-empty")
    if not np.all(np.isfinite(labels)):
        raise ValueError("labels contain non-finite values")
    unique = set(np.unique(labels).tolist())
    if not unique <= {0.0, 1.0}:
        raise ValueError("probe currently supports binary labels {0,1}")
    return labels


def _ridge_weights(x: np.ndarray, y: np.ndarray, regularization: float) -> np.ndarray:
    phi = np.column_stack([np.ones(x.shape[0]), x])
    gram = phi.T @ phi
    penalty = regularization * np.eye(gram.shape[0])
    penalty[0, 0] = 0.0
    try:
        return np.linalg.solve(gram + penalty, phi.T @ y)
    except np.linalg.LinAlgError as exc:
        raise ValueError("probe fit is not computable for these activations") from exc


def _accuracy(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> float:
    phi = np.column_stack([np.ones(x.shape[0]), x])
    predicted = (phi @ weights) >= 0.5
    return float(np.mean(predicted == (y >= 0.5)))


def _majority_accuracy(train_y: np.ndarray, test_y: np.ndarray) -> float:
    majority = 1.0 if np.mean(train_y) >= 0.5 else 0.0
    return float(np.mean((test_y >= 0.5) == (majority >= 0.5)))


def _shuffled_baseline(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    test_y: np.ndarray,
    regularization: float,
    seed: int,
) -> float:
    shuffled = train_y.copy()
    np.random.default_rng(seed).shuffle(shuffled)
    weights = _ridge_weights(train_x, shuffled, regularization)
    return _accuracy(test_x, test_y, weights)


def _row_hash(row: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(row, dtype=np.float64).tobytes()).hexdigest()


def _partition_sha256(x: np.ndarray, y: np.ndarray, ids: Sequence[str]) -> str:
    payload = b"|".join(item.encode("utf-8") for item in ids)
    payload += np.ascontiguousarray(x).tobytes()
    payload += np.ascontiguousarray(y).tobytes()
    return hashlib.sha256(payload).hexdigest()


def _metric_result(
    *,
    name: str,
    value: float,
    owner_id: str,
    inputs: Sequence[str],
    limitations: Sequence[str],
) -> dict[str, Any]:
    result = {
        "schema_version": "1.0.0",
        "metric_result_id": f"{name}-{owner_id[:12]}",
        "metric_name": name,
        "metric_version": "0.1.0",
        "input_observation_ids": list(inputs),
        "preprocessing_id": "ridge-linear-probe",
        "status": "MEASURED",
        "value": value,
        "uncertainty": None,
        "tolerance": None,
        "null_control_ids": [],
        "limitations": list(limitations),
        "created_at_utc": _CREATED,
    }
    validate_contract("metric-result", result)
    return result
