from __future__ import annotations

import numpy as np
import pytest

from noesis.geometry import (
    evaluate_geometry_candidate,
    evaluate_product_ablation,
    shuffled_relation_null,
    validate_geometry_profile,
)


DIGEST = "a" * 64


def _profile() -> dict:
    return {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-topo",
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
                "candidate_id": "t2",
                "family": "TOPOLOGICAL",
                "dimension": 2,
                "metric": "graph_path",
                "fit_config": {"max_scale": 1.5},
                "complexity_cost": 1,
            },
            {
                "candidate_id": "p2",
                "family": "PRODUCT_MANIFOLD",
                "dimension": 2,
                "metric": "product_l2",
                "fit_config": {"component_dims": [1, 1]},
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
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }


def test_topological_path_metric_on_a_line():
    profile = _profile()
    validate_geometry_profile(profile)
    points = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]])
    relations = ((0, 1, 1.0), (1, 2, 1.0), (0, 2, 2.0))
    result = evaluate_geometry_candidate(
        profile,
        candidate_id="t2",
        split="DISCOVERY",
        points=points,
        relations=relations,
    )
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(0.0, abs=1e-9)


def test_topological_without_filtration_is_not_computable():
    profile = _profile()
    profile["candidate_spaces"][1]["fit_config"] = {}
    result = evaluate_geometry_candidate(
        profile,
        candidate_id="t2",
        split="DISCOVERY",
        points=np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]),
        relations=((0, 1, 1.0), (1, 2, 1.0), (0, 2, 2.0)),
    )
    assert result["status"] == "NOT_COMPUTABLE"


def test_shuffled_relations_raise_distortion():
    profile = _profile()
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    relations = ((0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0), (0, 3, float(np.sqrt(2))))
    true = evaluate_geometry_candidate(
        profile, candidate_id="e2", split="DISCOVERY", points=points, relations=relations
    )
    null = shuffled_relation_null(
        profile, candidate_id="e2", split="CONTROL", points=points, relations=relations, seed=3
    )
    assert true["value"] < null["value"]
    assert null["diagnostics"]["null"] == "shuffled_labels"


def test_product_component_ablation_increases_distortion():
    profile = _profile()
    points = np.array([[0.0, 0.0], [3.0, 4.0]])
    relations = ((0, 1, 5.0),)
    full = evaluate_geometry_candidate(
        profile, candidate_id="p2", split="DISCOVERY", points=points, relations=relations
    )
    ablations = evaluate_product_ablation(
        profile, candidate_id="p2", split="DISCOVERY", points=points, relations=relations
    )
    assert full["value"] == pytest.approx(0.0, abs=1e-9)
    assert len(ablations) == 2
    assert all(item["value"] > full["value"] for item in ablations)
