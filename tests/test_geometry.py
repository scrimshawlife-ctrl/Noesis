from __future__ import annotations

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.geometry import (
    evaluate_geometry_candidate,
    freeze_geometry_selection,
    select_geometry_candidate,
    validate_geometry_profile,
)


DIGEST = "a" * 64


def _profile(**overrides) -> dict:
    profile = {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-001",
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
        "selection_rule": {"minimum_effect": 0.05, "complexity_penalty": 0.2},
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }
    profile.update(overrides)
    return profile


def test_profile_requires_euclidean_and_validates_contract():
    profile = _profile()
    validate_geometry_profile(profile)
    ContractRegistry("contracts").validate("geometry-profile", profile)
    broken = _profile()
    broken["candidate_spaces"] = [c for c in broken["candidate_spaces"] if c["family"] != "EUCLIDEAN"]
    broken["candidate_spaces"].append(
        {
            "candidate_id": "s2",
            "family": "SPHERICAL",
            "dimension": 2,
            "metric": "great_circle",
            "fit_config": {},
            "complexity_cost": 1,
        }
    )
    with pytest.raises(ValueError):
        validate_geometry_profile(broken)


def test_euclidean_identity_relations_have_low_geodesic_distortion():
    points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    relations = ((0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0), (2, 3, 1.0))
    result = evaluate_geometry_candidate(
        _profile(),
        candidate_id="e2",
        split="DISCOVERY",
        points=points,
        relations=relations,
    )
    ContractRegistry("contracts").validate("geometric-metric-result", result)
    assert result["status"] == "MEASURED"
    assert result["provenance"] == "OBSERVED"
    assert result["value"] == pytest.approx(0.0, abs=1e-9)
    assert "semantic_equivalence" not in result
    assert "universal_geometry" not in result


def test_confirmation_is_blocked_until_selection_is_frozen():
    points = np.array([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1]])
    relations = ((0, 1, 0.1), (0, 2, 0.1))
    with pytest.raises(ValueError, match="confirmation"):
        evaluate_geometry_candidate(
            _profile(),
            candidate_id="e2",
            split="CONFIRMATION",
            points=points,
            relations=relations,
        )


def test_hyperbolic_points_outside_ball_are_not_computable():
    points = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0]])
    relations = ((0, 1, 1.0), (0, 2, 1.0))
    result = evaluate_geometry_candidate(
        _profile(),
        candidate_id="h2",
        split="DISCOVERY",
        points=points,
        relations=relations,
    )
    assert result["status"] == "NOT_COMPUTABLE"
    assert result["provenance"] == "NOT_COMPUTABLE"
    assert result["value"] is None


def test_selection_uses_selection_split_and_complexity_penalty():
    euclid = {
        "candidate_id": "e2",
        "split": "SELECTION",
        "metric": "geodesic_distortion",
        "value": 0.20,
        "status": "MEASURED",
    }
    hyper = {
        "candidate_id": "h2",
        "split": "SELECTION",
        "metric": "geodesic_distortion",
        "value": 0.10,
        "status": "MEASURED",
    }
    decision = select_geometry_candidate(_profile(), (euclid, hyper))
    assert decision["selected_id"] == "e2"
    assert decision["frozen"] is False
    confirmation = {
        "candidate_id": "h2",
        "split": "CONFIRMATION",
        "metric": "geodesic_distortion",
        "value": 0.0,
        "status": "MEASURED",
    }
    with_confirmation = select_geometry_candidate(_profile(), (euclid, hyper, confirmation))
    assert with_confirmation["selected_id"] == "e2"


def test_frozen_selection_allows_confirmation_eval():
    profile = _profile()
    freeze = freeze_geometry_selection(profile, selected_id="e2")
    points = np.array([[0.0, 0.0], [1.0, 0.0]])
    relations = ((0, 1, 1.0),)
    result = evaluate_geometry_candidate(
        profile,
        candidate_id="e2",
        split="CONFIRMATION",
        points=points,
        relations=relations,
        frozen_selection=freeze,
    )
    assert result["status"] == "MEASURED"
    assert result["split"] == "CONFIRMATION"
