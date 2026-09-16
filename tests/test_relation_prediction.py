from __future__ import annotations

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.geometry import evaluate_relation_prediction


DIGEST = "a" * 64


def _profile() -> dict:
    return {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-link",
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
        "primary_metrics": ["relation_prediction_auc"],
        "selection_rule": {"minimum_effect": 0.05},
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }


def test_held_out_close_pairs_outrank_non_edges():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    result = evaluate_relation_prediction(
        _profile(),
        candidate_id="e2",
        split="CONTROL",
        points=points,
        train_relations=((0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0)),
        held_out_relations=((2, 3, 1.0),),
    )
    ContractRegistry("contracts").validate("geometric-metric-result", result)
    assert result["metric"] == "relation_prediction_auc"
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(1.0)


def test_relation_prediction_fails_closed_without_negatives():
    points = np.array([[0.0, 0.0], [1.0, 0.0]])
    result = evaluate_relation_prediction(
        _profile(),
        candidate_id="e2",
        split="CONTROL",
        points=points,
        train_relations=((0, 1, 1.0),),
        held_out_relations=(),
    )
    assert result["status"] == "NOT_COMPUTABLE"
