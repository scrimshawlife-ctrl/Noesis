import json

import pytest

from noesis.contracts.registry import ContractRegistry


def test_manifest_contract_accepts_canonical_fixture():
    registry = ContractRegistry("contracts")
    manifest = json.loads(open("examples/manifests/slice-001.json", encoding="utf-8").read())
    registry.validate("experiment-manifest", manifest)


def test_manifest_contract_rejects_missing_provenance_fields():
    registry = ContractRegistry("contracts")
    with pytest.raises(ValueError):
        registry.validate("experiment-manifest", {"schema_version": "1.0.0"})


def test_exp001_transform_catalog_contract_accepts_minimal_operator_catalog():
    registry = ContractRegistry("contracts")
    registry.validate(
        "exp001-transform-catalog",
        {
            "schema_version": "1.0.0",
            "catalog_id": "exp001-transforms",
            "version": "draft-1",
            "transforms": [
                {
                    "transform_class": "slang",
                    "semantic_intent": "operator-declared intent",
                    "expected_invariants": ["declared-invariant"],
                    "expected_changed_attributes": ["register"],
                    "parameters": {},
                    "role": "transform",
                }
            ],
        },
    )


def test_new_preregistration_contracts_fail_closed():
    registry = ContractRegistry("contracts")
    with pytest.raises(ValueError):
        registry.validate("exp001-source-corpus", {"schema_version": "1.0.0"})
    with pytest.raises(ValueError):
        registry.validate("n01-acceptance-evidence", {"schema_version": "1.0.0"})


def test_geometry_profile_requires_euclidean_control():
    registry = ContractRegistry("contracts")
    digest = "a" * 64
    base = {
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
            "discovery_hash": digest,
            "selection_hash": digest,
            "confirmation_hash": digest,
            "control_hash": digest,
        },
        "primary_metrics": ["geodesic_distortion"],
        "selection_rule": {"minimum_effect": 0.05},
        "nulls": ["shuffled_labels"],
        "failure_policy": "NOT_COMPUTABLE",
        "created_at": "2026-09-14T00:00:00Z",
    }
    registry.validate("geometry-profile", base)
    base["candidate_spaces"][0]["family"] = "SPHERICAL"
    with pytest.raises(ValueError):
        registry.validate("geometry-profile", base)


def test_geometric_result_binds_not_computable_provenance():
    registry = ContractRegistry("contracts")
    result = {
        "schema_version": "0.1.0",
        "result_id": "geo-result-1",
        "profile_id": "exp001-geo-001",
        "run_id": "run-1",
        "candidate_id": "h2",
        "split": "CONFIRMATION",
        "metric": "geodesic_distortion",
        "status": "NOT_COMPUTABLE",
        "input_evidence_ids": ["observation-1"],
        "diagnostics": {"reason": "insufficient_sample"},
        "null_result_ids": [],
        "provenance": "NOT_COMPUTABLE",
        "created_at": "2026-09-14T00:00:00Z",
    }
    registry.validate("geometric-metric-result", result)
    result["provenance"] = "OBSERVED"
    with pytest.raises(ValueError):
        registry.validate("geometric-metric-result", result)
