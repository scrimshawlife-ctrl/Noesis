from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


def environment_fingerprint(environment: Mapping[str, Any]) -> str:
    material = {key: environment[key] for key in environment if key != "fingerprint"}
    payload = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def compare_environment_fingerprints(
    original: Mapping[str, Any],
    current: Mapping[str, Any],
) -> dict[str, Any]:
    original_fp = original.get("fingerprint") or environment_fingerprint(original)
    current_fp = current.get("fingerprint") or environment_fingerprint(current)
    if original_fp == current_fp:
        return {"status": "EQUIVALENT", "fingerprint": original_fp, "delta": []}
    original_keys = {key: original[key] for key in original if key != "fingerprint"}
    current_keys = {key: current[key] for key in current if key != "fingerprint"}
    delta = sorted(
        key for key in set(original_keys) | set(current_keys) if original_keys.get(key) != current_keys.get(key)
    )
    return {
        "status": "NEW_RUN_REQUIRED",
        "original_fingerprint": original_fp,
        "current_fingerprint": current_fp,
        "delta": delta,
    }
