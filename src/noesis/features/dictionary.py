from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import numpy as np

from noesis.contracts.registry import validate_contract

_EPS = 1e-12


@dataclass(frozen=True, slots=True)
class DictionaryRecord:
    dictionary_id: str
    dictionary_sha256: str
    n_features: int
    reconstruction_r2: float
    mean_l0_fraction: float
    dead_feature_rate: float
    source_activation_sha256: str
    training: dict[str, Any]
    metric_results: tuple[dict[str, Any], ...]
    decoder: tuple[tuple[float, ...], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "dictionary_id": self.dictionary_id,
            "dictionary_sha256": self.dictionary_sha256,
            "n_features": self.n_features,
            "reconstruction_r2": self.reconstruction_r2,
            "mean_l0_fraction": self.mean_l0_fraction,
            "dead_feature_rate": self.dead_feature_rate,
            "source_activation_sha256": self.source_activation_sha256,
            "training": dict(self.training),
            "features": [{"index": index} for index in range(self.n_features)],
        }


def fit_sparse_dictionary(
    activations,
    *,
    n_features: int,
    seed: int,
    dead_threshold: float = 1e-8,
) -> DictionaryRecord:
    matrix = _activation_matrix(activations)
    if n_features < 1:
        raise ValueError("n_features must be >= 1")
    decoder = _tied_dictionary(matrix, n_features=n_features, seed=seed)
    codes = _relu(matrix @ decoder)
    reconstruction = codes @ decoder.T
    stats = _dictionary_stats(matrix, codes, reconstruction, dead_threshold)
    source_sha = hashlib.sha256(np.ascontiguousarray(matrix).tobytes()).hexdigest()
    decoder_sha = hashlib.sha256(np.ascontiguousarray(decoder).tobytes()).hexdigest()
    dictionary_id = f"dict-{decoder_sha[:12]}"
    training = {
        "algorithm": "tied-svd-relu",
        "seed": seed,
        "n_features": n_features,
        "n_samples": int(matrix.shape[0]),
        "n_dims": int(matrix.shape[1]),
        "dead_threshold": dead_threshold,
    }
    created_at = datetime(2026, 9, 16, tzinfo=UTC).isoformat()
    metrics = (
        _metric_result(
            "reconstruction_r2",
            stats["reconstruction_r2"],
            source_sha,
            created_at,
            dictionary_id,
        ),
        _metric_result(
            "mean_l0_fraction",
            stats["mean_l0_fraction"],
            source_sha,
            created_at,
            dictionary_id,
        ),
        _metric_result(
            "dead_feature_rate",
            stats["dead_feature_rate"],
            source_sha,
            created_at,
            dictionary_id,
        ),
    )
    return DictionaryRecord(
        dictionary_id=dictionary_id,
        dictionary_sha256=decoder_sha,
        n_features=n_features,
        reconstruction_r2=stats["reconstruction_r2"],
        mean_l0_fraction=stats["mean_l0_fraction"],
        dead_feature_rate=stats["dead_feature_rate"],
        source_activation_sha256=source_sha,
        training=training,
        metric_results=metrics,
        decoder=tuple(tuple(float(v) for v in row) for row in decoder),
    )


def run_dictionary_consistency(
    activations,
    *,
    n_features: int,
    seeds: tuple[int, int],
    bootstrap: bool = False,
) -> dict[str, Any]:
    matrix = _activation_matrix(activations)
    left = _fit_decoder(matrix, n_features=n_features, seed=seeds[0], bootstrap=bootstrap)
    right = _fit_decoder(matrix, n_features=n_features, seed=seeds[1], bootstrap=bootstrap)
    value = _matched_column_cosine(left, right)
    source_sha = hashlib.sha256(np.ascontiguousarray(matrix).tobytes()).hexdigest()
    result = _metric_result(
        "dictionary_run_consistency",
        value,
        source_sha,
        datetime(2026, 9, 16, tzinfo=UTC).isoformat(),
        f"consistency-{seeds[0]}-{seeds[1]}",
    )
    result["limitations"] = [
        "consistency is decoder-column cosine after sign-invariant matching",
        "bootstrap=true resamples rows before each fit",
    ]
    validate_contract("metric-result", result)
    return result


def _activation_matrix(activations) -> np.ndarray:
    matrix = np.asarray(activations, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[1] == 0:
        raise ValueError("expected a non-empty 2D activation matrix")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("activations contain non-finite values")
    return matrix


def _tied_dictionary(matrix: np.ndarray, *, n_features: int, seed: int) -> np.ndarray:
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    _u, _s, vt = np.linalg.svd(centered, full_matrices=False)
    rank = int(vt.shape[0])
    take = min(n_features, rank)
    decoder = vt[:take].T.copy()
    if n_features > take:
        rng = np.random.default_rng(seed)
        extra = rng.normal(size=(matrix.shape[1], n_features - take))
        norms = np.linalg.norm(extra, axis=0, keepdims=True)
        extra = extra / np.maximum(norms, _EPS)
        decoder = np.concatenate([decoder, extra], axis=1)
    return decoder


def _fit_decoder(matrix: np.ndarray, *, n_features: int, seed: int, bootstrap: bool) -> np.ndarray:
    data = matrix
    if bootstrap:
        rng = np.random.default_rng(seed)
        data = matrix[rng.integers(0, matrix.shape[0], size=matrix.shape[0])]
    return _tied_dictionary(data, n_features=n_features, seed=seed)


def _relu(values: np.ndarray) -> np.ndarray:
    return np.maximum(values, 0.0)


def _dictionary_stats(
    matrix: np.ndarray,
    codes: np.ndarray,
    reconstruction: np.ndarray,
    dead_threshold: float,
) -> dict[str, float]:
    residual = matrix - reconstruction
    ss_res = float(np.sum(residual ** 2))
    ss_tot = float(np.sum((matrix - matrix.mean(axis=0, keepdims=True)) ** 2))
    r2 = 0.0 if ss_tot <= _EPS else float(np.clip(1.0 - ss_res / ss_tot, 0.0, 1.0))
    active = codes > dead_threshold
    mean_l0 = float(active.mean(axis=1).mean()) if codes.size else 0.0
    dead = float(np.mean(np.max(codes, axis=0) <= dead_threshold)) if codes.size else 1.0
    return {
        "reconstruction_r2": r2,
        "mean_l0_fraction": mean_l0,
        "dead_feature_rate": dead,
    }


def _matched_column_cosine(left: np.ndarray, right: np.ndarray) -> float:
    def _normalize(matrix: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(matrix, axis=0, keepdims=True)
        return matrix / np.maximum(norms, _EPS)

    a, b = _normalize(left), _normalize(right)
    similarity = np.abs(a.T @ b)
    remaining_rows = set(range(similarity.shape[0]))
    remaining_cols = set(range(similarity.shape[1]))
    scores: list[float] = []
    while remaining_rows and remaining_cols:
        best = -1.0
        pair = (0, 0)
        for i in remaining_rows:
            for j in remaining_cols:
                if similarity[i, j] > best:
                    best = float(similarity[i, j])
                    pair = (i, j)
        scores.append(best)
        remaining_rows.remove(pair[0])
        remaining_cols.remove(pair[1])
    return float(np.mean(scores)) if scores else 0.0


def _metric_result(
    name: str,
    value: float,
    source_sha: str,
    created_at: str,
    owner_id: str,
) -> dict[str, Any]:
    result = {
        "schema_version": "1.0.0",
        "metric_result_id": f"{name}-{owner_id[:12]}",
        "metric_name": name,
        "metric_version": "0.1.0",
        "input_observation_ids": [f"activations:{source_sha[:16]}"],
        "preprocessing_id": "center+tied-svd-relu",
        "status": "MEASURED",
        "value": value,
        "uncertainty": None,
        "tolerance": None,
        "null_control_ids": [],
        "limitations": [],
        "created_at_utc": created_at,
    }
    validate_contract("metric-result", result)
    return result
