from __future__ import annotations

from noesis.geometry import label_geometric_rupture


def _profile() -> dict:
    return {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-rupture",
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
            "discovery_hash": "a" * 64,
            "selection_hash": "a" * 64,
            "confirmation_hash": "a" * 64,
            "control_hash": "a" * 64,
        },
        "primary_metrics": ["geodesic_distortion"],
        "selection_rule": {"minimum_effect": 0.05, "rupture_threshold": 0.25},
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-16T00:00:00Z",
    }


def test_distortion_above_threshold_is_ruptured():
    label = label_geometric_rupture(
        _profile(),
        {"result_id": "geo-e2-discovery", "status": "MEASURED", "value": 0.40, "metric": "geodesic_distortion"},
    )
    assert label["decision"] == "RUPTURED"
    assert label["canonical"] is False
    assert "semantic_destruction" not in label


def test_distortion_below_threshold_is_intact():
    label = label_geometric_rupture(
        _profile(),
        {"result_id": "geo-e2-discovery", "status": "MEASURED", "value": 0.01, "metric": "geodesic_distortion"},
    )
    assert label["decision"] == "INTACT"


def test_not_computable_metric_cannot_claim_rupture():
    label = label_geometric_rupture(
        _profile(),
        {"result_id": "geo-h2-discovery", "status": "NOT_COMPUTABLE", "value": None, "metric": "geodesic_distortion"},
    )
    assert label["decision"] == "NOT_COMPUTABLE"
    assert label["canonical"] is False
