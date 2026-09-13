from __future__ import annotations

from collections.abc import Callable

import numpy as np


def _vector(x) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float64)
    if arr.ndim != 1 or arr.size == 0:
        raise ValueError("expected a non-empty 1D vector")
    if not np.all(np.isfinite(arr)):
        raise ValueError("vector contains non-finite values")
    return arr


def _matrix(x) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[0] == 0 or arr.shape[1] == 0:
        raise ValueError("expected a non-empty 2D matrix")
    if not np.all(np.isfinite(arr)):
        raise ValueError("matrix contains non-finite values")
    return arr


def cosine_similarity(a, b) -> float:
    x, y = _vector(a), _vector(b)
    if x.shape != y.shape:
        raise ValueError("vectors must have equal shape")
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    if denom == 0:
        raise ValueError("cosine similarity is undefined for zero vectors")
    return float(np.dot(x, y) / denom)


def euclidean_distance(a, b) -> float:
    x, y = _vector(a), _vector(b)
    if x.shape != y.shape:
        raise ValueError("vectors must have equal shape")
    return float(np.linalg.norm(x - y))


def linear_cka(x, y) -> float:
    a, b = _matrix(x), _matrix(y)
    if a.shape[0] != b.shape[0] or a.shape[0] < 2:
        raise ValueError("CKA expects equal sample count >= 2")
    a = a - a.mean(axis=0, keepdims=True)
    b = b - b.mean(axis=0, keepdims=True)
    numerator = np.linalg.norm(a.T @ b, ord="fro") ** 2
    denom = np.linalg.norm(a.T @ a, ord="fro") * np.linalg.norm(b.T @ b, ord="fro")
    if denom == 0:
        raise ValueError("CKA is undefined for degenerate matrices")
    return float(numerator / denom)


def neighborhood_overlap(x, y, k: int = 5) -> float:
    """Mean Jaccard overlap of k-nearest-neighbor sets across two spaces."""
    a, b = _matrix(x), _matrix(y)
    if a.shape[0] != b.shape[0]:
        raise ValueError("spaces must contain the same samples")
    n = a.shape[0]
    if not 1 <= k < n:
        raise ValueError("k must satisfy 1 <= k < sample count")

    def neighbors(matrix: np.ndarray) -> list[set[int]]:
        sq = np.sum((matrix[:, None, :] - matrix[None, :, :]) ** 2, axis=-1)
        order = np.argsort(sq, axis=1)
        return [set(row[1 : k + 1].tolist()) for row in order]

    left, right = neighbors(a), neighbors(b)
    return float(np.mean([len(p & q) / len(p | q) for p, q in zip(left, right, strict=True)]))


def permutation_null(
    x,
    y,
    metric: Callable[[np.ndarray, np.ndarray], float],
    repeats: int = 100,
    seed: int = 0,
) -> np.ndarray:
    a, b = _matrix(x), _matrix(y)
    if a.shape[0] != b.shape[0] or repeats < 1:
        raise ValueError("invalid permutation-null inputs")
    rng = np.random.default_rng(seed)
    return np.asarray([metric(a, b[rng.permutation(b.shape[0])]) for _ in range(repeats)], dtype=np.float64)


def bootstrap_mean_ci(values, confidence: float = 0.95, repeats: int = 1000, seed: int = 0) -> tuple[float, float, float]:
    sample = _vector(values)
    if not 0 < confidence < 1 or repeats < 1:
        raise ValueError("invalid bootstrap parameters")
    rng = np.random.default_rng(seed)
    means = np.asarray([rng.choice(sample, size=sample.size, replace=True).mean() for _ in range(repeats)])
    alpha = (1.0 - confidence) / 2.0
    return float(sample.mean()), float(np.quantile(means, alpha)), float(np.quantile(means, 1.0 - alpha))
