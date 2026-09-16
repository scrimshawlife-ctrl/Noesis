from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from noesis.artifacts.store import ContentAddressedStore

_CLASSIFICATIONS = frozenset(
    {"PUBLIC_REPRODUCIBLE", "RESEARCH_INTERNAL", "SENSITIVE", "PROHIBITED"}
)
_GATED_SCOPES = frozenset({"FIELD", "N5"})
_SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|password|secret)\s*[:=]\s*\S+"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
)


def scan_secrets(text: str) -> tuple[str, ...]:
    hits: list[str] = []
    for pattern in _SECRET_PATTERNS:
        for match in pattern.finditer(text):
            hits.append(match.group(0)[:48])
    return tuple(hits)


def classify_fixture(record: Mapping[str, Any]) -> dict[str, Any]:
    classification = str(record.get("data_classification") or "")
    if classification not in _CLASSIFICATIONS:
        raise ValueError("fixture must declare a known data_classification")
    if classification == "PROHIBITED":
        raise ValueError("PROHIBITED data may not enter Noesis evidence storage")
    if classification == "SENSITIVE":
        if not record.get("retention"):
            raise ValueError("SENSITIVE fixtures require a retention policy")
        if not record.get("access_scope"):
            raise ValueError("SENSITIVE fixtures require an access_scope")
    secrets = scan_secrets(str(record.get("text") or ""))
    if secrets:
        raise ValueError("fixture contains secret-like patterns")
    return {
        "data_classification": classification,
        "retention": record.get("retention"),
        "access_scope": record.get("access_scope"),
    }


def authorize_scope(scope: str, *, authorization: Mapping[str, Any] | None) -> str:
    if scope in _GATED_SCOPES:
        if not authorization or authorization.get("scope") != scope:
            raise ValueError(f"{scope} execution requires explicit operator authorization")
        if not authorization.get("operator"):
            raise ValueError(f"{scope} authorization must identify an operator")
    return scope


def verify_artifact_integrity(
    store: ContentAddressedStore,
    path: str | Path,
    expected_sha256: str,
) -> bool:
    return store.verify_path(path, expected_sha256)


def record_incident(
    original: Mapping[str, Any],
    *,
    reason: str,
    actor: str,
    successor_ref: str,
) -> dict[str, Any]:
    if not reason.strip():
        raise ValueError("incident reason is required")
    material = f"{original.get('settlement_id')}|{reason}|{successor_ref}".encode("utf-8")
    return {
        "incident_id": "inc-" + hashlib.sha256(material).hexdigest()[:12],
        "target_id": original.get("settlement_id"),
        "reason": reason,
        "actor": actor,
        "successor_ref": successor_ref,
        "created_at": datetime(2026, 9, 16, tzinfo=UTC).isoformat(),
        "governance_effect": "ADVISORY_ONLY",
    }
