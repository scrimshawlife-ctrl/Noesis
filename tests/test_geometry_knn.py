from __future__ import annotations

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.geometry import evaluate_knn_retention, evaluate_rank_preservation


DIGEST = "a" * 64


def _profile() -> dict:
    return {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-knn",
        "experiment_id": "exp001",
        "candidate_spaces": [
            {
                "candidate_id": "e2",
                "family": "EUCLIDEAN",
                "dimension": 2,
                "metric": "l2",
                "fit_config": {},
                "complexity_cost": 0,
            },
            {
                "candidate_id": "h2",
                "family": "HYPERBOLIC",
                "curvature": -1,
                "dimension": 2,
                "metric": "poincare",
                "fit_config": {},
                "complexity_cost": 1,
            },
        ],
        "partitions": {
            "discovery_hash": DIGEST,
            "selection_hash": DIGEST,
            "confirmation_hash": DIGEST,
            "control_hash": DIGEST,
        },
        "primary_metrics": ["geodesic_distortion", "knn_retention"],
        "selection_rule": {"minimum_effect": 0.05},
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }


def test_knn_retention_is_one_on_identity_grid():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    relations = (
        (0, 1, 1.0),
        (0, 2, 1.0),
        (1, 3, 1.0),
        (2, 3, 1.0),
        (0, 3, float(np.sqrt(2))),
        (1, 2, float(np.sqrt(2))),
    )
    result = evaluate_knn_retention(
        _profile(), candidate_id="e2", split="DISCOVERY", points=points, relations=relations, k=1
    )
    ContractRegistry("contracts").validate("geometric-metric-result", result)
    assert result["metric"] == "knn_retention"
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(1.0)


def test_knn_retention_fails_closed_when_k_too_large():
    points = np.array([[0.0, 0.0], [1.0, 0.0]])
    result = evaluate_knn_retention(
        _profile(),
        candidate_id="e2",
        split="DISCOVERY",
        points=points,
        relations=((0, 1, 1.0),),
        k=2,
    )
    assert result["status"] == "NOT_COMPUTABLE"


def test_rank_preservation_is_one_when_order_matches():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [3.0, 0.0]])
    relations = ((0, 1, 1.0), (0, 2, 3.0), (1, 2, 2.0))
    result = evaluate_rank_preservation(
        _profile(), candidate_id="e2", split="DISCOVERY", points=points, relations=relations
    )
    ContractRegistry("contracts").validate("geometric-metric-result", result)
    assert result["metric"] == "rank_order_preservation"
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(1.0)
