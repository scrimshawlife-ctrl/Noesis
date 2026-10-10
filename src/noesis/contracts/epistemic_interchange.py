from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from .registry import ContractRegistry, repository_contracts_dir

_STATUS_RANK = {
    "OBSERVED": 0,
    "INTERPRETED": 1,
    "CALIBRATED": 2,
    "SETTLED": 3,
    "NOT_COMPUTABLE": -1,
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def validate_interchange_object(instance: dict[str, Any], contracts_dir=None) -> None:
    ContractRegistry(contracts_dir or repository_contracts_dir()).validate(
        "epistemic-interchange-object", instance
    )


def assert_no_silent_promotion(before: dict[str, Any], after: dict[str, Any]) -> None:
    """Reject epistemic strengthening without an explicit assertion for the target state."""
    source = before["epistemic_status"]
    target = after["epistemic_status"]
    if target == "NOT_COMPUTABLE" or source == target:
        return
    if _STATUS_RANK[target] <= _STATUS_RANK[source]:
        return

    required_class = {
        "INTERPRETED": "INTERPRETATION",
        "CALIBRATED": "CALIBRATION",
        "SETTLED": "SETTLEMENT",
    }[target]
    new_assertions = {
        item["assertion_id"]: item
        for item in after.get("assertions", [])
        if item["assertion_id"] not in {x["assertion_id"] for x in before.get("assertions", [])}
    }
    if not any(item["class"] == required_class and item.get("evidence_refs") for item in new_assertions.values()):
        raise ValueError(
            f"silent epistemic promotion {source}->{target}: missing new {required_class} assertion"
        )


def append_provenance(
    instance: dict[str, Any],
    event: dict[str, Any],
    *,
    expected_previous_hash: str | None = None,
) -> dict[str, Any]:
    validate_interchange_object(instance)
    current_hash = canonical_sha256(instance)
    if expected_previous_hash is not None and current_hash != expected_previous_hash:
        raise ValueError("interchange object hash mismatch before provenance append")

    updated = deepcopy(instance)
    updated["provenance"] = [*instance["provenance"], deepcopy(event)]
    validate_interchange_object(updated)

    if updated["provenance"][:-1] != instance["provenance"]:
        raise ValueError("provenance history mutation detected")
    return updated
