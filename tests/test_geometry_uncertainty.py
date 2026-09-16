from __future__ import annotations

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.geometry import (
    bootstrap_geodesic_uncertainty,
    evaluate_geometry_candidate,
    random_pair_null,
)


DIGEST = "a" * 64


def _profile() -> dict:
    return {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-unc",
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
        "primary_metrics": ["geodesic_distortion"],
        "selection_rule": {"minimum_effect": 0.05},
        "nulls": ["shuffled_labels", "random_pairs"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }


def test_random_pairs_raise_distortion_vs_registered_relations():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    relations = ((0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0), (0, 3, float(np.sqrt(2))))
    true = evaluate_geometry_candidate(
        _profile(), candidate_id="e2", split="DISCOVERY", points=points, relations=relations
    )
    null = random_pair_null(
        _profile(), candidate_id="e2", split="CONTROL", points=points, relations=relations, seed=4
    )
    ContractRegistry("contracts").validate("geometric-metric-result", null)
    assert true["value"] < null["value"]
    assert null["diagnostics"]["null"] == "random_pairs"


def test_bootstrap_uncertainty_bounds_the_mean():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    relations = ((0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0), (0, 3, float(np.sqrt(2))))
    result = bootstrap_geodesic_uncertainty(
        _profile(),
        candidate_id="e2",
        split="DISCOVERY",
        points=points,
        relations=relations,
        seed=2,
        repeats=40,
    )
    ContractRegistry("contracts").validate("geometric-metric-result", result)
    assert result["status"] == "MEASURED"
    lo = result["uncertainty"]["lo"]
    hi = result["uncertainty"]["hi"]
    mean = result["uncertainty"]["mean"]
    assert lo <= mean <= hi
    assert result["value"] == pytest.approx(mean)


def test_bootstrap_fails_closed_with_too_few_relations():
    points = np.array([[0.0, 0.0], [1.0, 0.0]])
    result = bootstrap_geodesic_uncertainty(
        _profile(),
        candidate_id="e2",
        split="DISCOVERY",
        points=points,
        relations=((0, 1, 1.0),),
        seed=0,
        repeats=10,
    )
    assert result["status"] == "NOT_COMPUTABLE"
