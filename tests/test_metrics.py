import numpy as np
import pytest

from noesis.metrics.core import cosine_similarity, euclidean_distance, linear_cka


def test_vector_metrics_identity_and_orthogonality():
    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)
    assert euclidean_distance([1, 0], [1, 0]) == pytest.approx(0.0)


def test_linear_cka_identity():
    x = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    assert linear_cka(x, x) == pytest.approx(1.0)


def test_metrics_fail_closed():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 0])
    with pytest.raises(ValueError):
        euclidean_distance([1], [1, 2])
    with pytest.raises(ValueError):
        linear_cka([[1, 2]], [[1, 2]])
