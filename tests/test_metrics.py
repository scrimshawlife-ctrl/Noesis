import numpy as np
import pytest

from noesis.metrics.core import (
    bootstrap_mean_ci,
    cosine_similarity,
    euclidean_distance,
    linear_cka,
    neighborhood_overlap,
    permutation_null,
)


def test_vector_metrics_identity_and_orthogonality():
    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)
    assert euclidean_distance([1, 0], [1, 0]) == pytest.approx(0.0)


def test_matrix_metrics_identity():
    x = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 1.0]])
    assert linear_cka(x, x) == pytest.approx(1.0)
    assert neighborhood_overlap(x, x, k=2) == pytest.approx(1.0)


def test_null_and_bootstrap_are_seed_reproducible():
    x = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 1.0]])
    first = permutation_null(x, x, linear_cka, repeats=8, seed=7)
    second = permutation_null(x, x, linear_cka, repeats=8, seed=7)
    assert np.array_equal(first, second)
    assert bootstrap_mean_ci([1, 2, 3, 4], repeats=50, seed=9) == bootstrap_mean_ci([1, 2, 3, 4], repeats=50, seed=9)


def test_metrics_fail_closed():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 0])
    with pytest.raises(ValueError):
        euclidean_distance([1], [1, 2])
    with pytest.raises(ValueError):
        linear_cka([[1, 2]], [[1, 2]])
    with pytest.raises(ValueError):
        neighborhood_overlap([[1], [2]], [[1], [2]], k=2)
