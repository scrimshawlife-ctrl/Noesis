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
