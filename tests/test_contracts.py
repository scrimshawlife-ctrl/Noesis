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
