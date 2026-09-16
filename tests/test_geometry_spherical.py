from __future__ import annotations

import numpy as np
import pytest

from noesis.geometry import (
    evaluate_geometry_candidate,
    select_geometry_candidate,
    validate_geometry_profile,
)


DIGEST = "a" * 64


def _profile(**overrides) -> dict:
    profile = {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-sph",
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
                "candidate_id": "s2",
                "family": "SPHERICAL",
                "dimension": 2,
                "metric": "great_circle",
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
        "selection_rule": {"minimum_effect": 0.05, "complexity_penalty": 0.0, "compute_penalty": 1.0},
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }
    profile.update(overrides)
    return profile


def test_spherical_reports_antipodal_pairs():
    profile = _profile()
    validate_geometry_profile(profile)
    points = np.array([[1.0, 0.0], [-1.0, 0.0]])
    result = evaluate_geometry_candidate(
        profile,
        candidate_id="s2",
        split="DISCOVERY",
        points=points,
        relations=((0, 1, float(np.pi)),),
    )
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(0.0, abs=1e-9)
    assert result["diagnostics"]["antipodal_pairs"] >= 1


def test_spherical_renormalizes_and_reports_it():
    profile = _profile()
    points = np.array([[2.0, 0.0], [0.0, 2.0]])
    result = evaluate_geometry_candidate(
        profile,
        candidate_id="s2",
        split="DISCOVERY",
        points=points,
        relations=((0, 1, float(np.pi / 2)),),
    )
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(0.0, abs=1e-9)
    assert result["diagnostics"]["renormalized"] is True


def test_selection_applies_compute_penalty():
    profile = _profile()
    cheap = {
        "candidate_id": "e2",
        "split": "SELECTION",
        "metric": "geodesic_distortion",
        "value": 0.10,
        "status": "MEASURED",
        "diagnostics": {"compute_cost": 1.0},
    }
    expensive = {
        "candidate_id": "s2",
        "split": "SELECTION",
        "metric": "geodesic_distortion",
        "value": 0.10,
        "status": "MEASURED",
        "diagnostics": {"compute_cost": 5.0},
    }
    decision = select_geometry_candidate(profile, (cheap, expensive))
    assert decision["selected_id"] == "e2"
