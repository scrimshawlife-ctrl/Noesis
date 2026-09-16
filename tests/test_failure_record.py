from __future__ import annotations

import numpy as np
import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.domain.models import FailureRecord
from noesis.geometry import evaluate_geometry_candidate, validate_geometry_profile


DIGEST = "a" * 64


def _geo_profile() -> dict:
    return {
        "schema_version": "0.1.0",
        "profile_id": "exp001-geo-002",
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


def test_failure_record_schema_accepts_runtime_record():
    record = FailureRecord(
        experiment_id="exp-fail",
        run_id="run-1",
        fixture_id="fx-1",
        site="embedding:token=-1",
        seed=0,
        error_type="KeyError",
        message="fx-1",
    ).as_dict()
    ContractRegistry("contracts").validate("failure-record", record)
    assert record["failure_id"]
    assert record["provenance"] == "OBSERVED"


def test_failure_record_schema_rejects_missing_provenance():
    record = FailureRecord(
        experiment_id="exp-fail",
        run_id="run-1",
        fixture_id="fx-1",
        site="embedding:token=-1",
        seed=0,
        error_type="KeyError",
        message="fx-1",
    ).as_dict()
    del record["provenance"]
    with pytest.raises(ValueError):
        ContractRegistry("contracts").validate("failure-record", record)


def test_spherical_unit_vectors_measure_right_angle():
    profile = _geo_profile()
    validate_geometry_profile(profile)
    points = np.array([[1.0, 0.0], [0.0, 1.0]])
    result = evaluate_geometry_candidate(
        profile,
        candidate_id="s2",
        split="DISCOVERY",
        points=points,
        relations=((0, 1, float(np.pi / 2)),),
    )
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(0.0, abs=1e-9)


def test_product_manifold_is_hypot_of_component_distances():
    profile = _geo_profile()
    points = np.array([[0.0, 0.0], [3.0, 4.0]])
    result = evaluate_geometry_candidate(
        profile,
        candidate_id="p2",
        split="DISCOVERY",
        points=points,
        relations=((0, 1, 5.0),),
    )
    assert result["status"] == "MEASURED"
    assert result["value"] == pytest.approx(0.0, abs=1e-9)
