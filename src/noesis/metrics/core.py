from __future__ import annotations

import numpy as np


def _vector(x: tuple[float, ...] | list[float] | np.ndarray) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float64)
    if arr.ndim != 1 or arr.size == 0:
        raise ValueError("expected a non-empty 1D vector")
    if not np.all(np.isfinite(arr)):
        raise ValueError("vector contains non-finite values")
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
    """Linear centered-kernel alignment for sample-by-feature matrices."""
    a = np.asarray(x, dtype=np.float64)
    b = np.asarray(y, dtype=np.float64)
    if a.ndim != 2 or b.ndim != 2 or a.shape[0] != b.shape[0] or a.shape[0] < 2:
        raise ValueError("CKA expects 2D matrices with equal sample count >= 2")
    a = a - a.mean(axis=0, keepdims=True)
    b = b - b.mean(axis=0, keepdims=True)
    cross = a.T @ b
    numerator = np.linalg.norm(cross, ord="fro") ** 2
    denom = np.linalg.norm(a.T @ a, ord="fro") * np.linalg.norm(b.T @ b, ord="fro")
    if denom == 0:
        raise ValueError("CKA is undefined for degenerate matrices")
    return float(numerator / denom)
