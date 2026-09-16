from __future__ import annotations

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.geometry import evaluate_geometry_candidate, evaluate_projection_loss


DIGEST = "a" * 64


def _profile() -> dict:
    return {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-proj",
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
        "primary_metrics": ["geodesic_distortion", "projection_loss"],
        "selection_rule": {"minimum_effect": 0.05},
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }


def test_projection_to_one_dimension_increases_relational_loss():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    relations = ((0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0), (0, 3, float(np.sqrt(2))))
    baseline = evaluate_geometry_candidate(
        _profile(), candidate_id="e2", split="DISCOVERY", points=points, relations=relations
    )
    lost = evaluate_projection_loss(
        _profile(),
        candidate_id="e2",
        split="CONTROL",
        points=points,
        relations=relations,
        target_dimension=1,
    )
    ContractRegistry("contracts").validate("geometric-metric-result", lost)
    assert lost["metric"] == "projection_loss"
    assert lost["status"] == "MEASURED"
    assert lost["value"] > baseline["value"]
    assert "intent" not in lost
    assert "legitimacy" not in lost
    assert "social_cause" not in lost


def test_projection_loss_fails_closed_when_target_dimension_invalid():
    points = np.array([[0.0, 0.0], [1.0, 0.0]])
    result = evaluate_projection_loss(
        _profile(),
        candidate_id="e2",
        split="CONTROL",
        points=points,
        relations=((0, 1, 1.0),),
        target_dimension=2,
    )
    assert result["status"] == "NOT_COMPUTABLE"
