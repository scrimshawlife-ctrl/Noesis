from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from noesis.contracts.registry import validate_contract

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ROLES = frozenset({"supporting", "contradicting", "control", "negative_result"})
_LABELS = ("OBSERVED", "INFERRED", "SPECULATIVE", "NOT_COMPUTABLE")
_LABEL_RANK = {label: index for index, label in enumerate(_LABELS)}


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    id: str
    sha256: str
    role: str
    kind: str = "observation"
    payload: bytes | None = None
    status: str | None = None


@dataclass(frozen=True, slots=True)
class SettlementRequest:
    experiment_id: str
    proposition: str
    evidence: Sequence[EvidenceRef]
    requested_label: str | None = None
    required_ids: Sequence[str] = ()
    causal_claim: bool = False
    limitations: Sequence[str] = ()
    confidence_basis: Sequence[str] = ()
    created_at: str = "2026-09-16T00:00:00Z"
    settlement_id: str = ""
    independent_replication: bool = False


def settle_evidence(request: SettlementRequest) -> dict[str, Any]:
    if not request.evidence:
        raise ValueError("settlement requires at least one evidence object")
    if not request.experiment_id or not request.proposition:
        raise ValueError("settlement requires experiment_id and proposition")

    cited = [_validated_item(item) for item in request.evidence]
    missing = [evidence_id for evidence_id in request.required_ids if evidence_id not in {item.id for item in request.evidence}]
    label = _assign_label(request, cited, missing)
    promotion = _assign_promotion(label, cited, request.independent_replication)
    limitations = list(request.limitations)
    if request.causal_claim and not _has_kind(cited, "intervention"):
        limitations.append(
            "Causal claim has no intervention evidence; interpretation is bounded."
        )
    unresolved = list(missing)
    if label == "NOT_COMPUTABLE" and missing:
        unresolved = list(dict.fromkeys(unresolved))

    settlement_id = request.settlement_id or _default_id(request.experiment_id, request.proposition)
    settlement = {
        "schema_version": "0.1.0",
        "settlement_id": settlement_id,
        "experiment_id": request.experiment_id,
        "created_at": request.created_at,
        "proposition": request.proposition,
        "label": label,
        "evidence": [
            {"id": item.id, "sha256": item.sha256, "role": item.role}
            for item in cited
        ],
        "confidence_basis": list(request.confidence_basis),
        "limitations": limitations,
        "unresolved": unresolved,
        "promotion": promotion,
        "governance_effect": "ADVISORY_ONLY",
    }
    validate_contract("settlement", settlement)
    return settlement


def supersede_settlement(
    original: Mapping[str, Any],
    *,
    successor_ref: str,
    reason: str,
    actor: str,
    created_at: str,
    supersession_id: str,
) -> dict[str, Any]:
    record = {
        "schema_version": "0.1.0",
        "supersession_id": supersession_id,
        "old_object_id": original["settlement_id"],
        "successor_ref": successor_ref,
        "reason": reason,
        "actor": actor,
        "created_at": created_at,
    }
    validate_contract("supersession", record)
    return record


def _validated_item(item: EvidenceRef) -> EvidenceRef:
    if item.role not in _ROLES:
        raise ValueError(f"unknown evidence role: {item.role}")
    if not _SHA256.match(item.sha256):
        raise ValueError("evidence sha256 must be 64 lowercase hex characters")
    if item.payload is not None:
        actual = hashlib.sha256(item.payload).hexdigest()
        if actual != item.sha256:
            raise ValueError("settlement cannot cite nonexistent evidence")
    return item


def _assign_label(
    request: SettlementRequest,
    evidence: Sequence[EvidenceRef],
    missing: Sequence[str],
) -> str:
    if missing:
        return "NOT_COMPUTABLE"
    requested = request.requested_label or "INFERRED"
    if requested not in _LABEL_RANK:
        raise ValueError(f"unknown requested label: {requested}")
    assigned = requested
    if request.causal_claim and not _has_kind(evidence, "intervention"):
        assigned = _weaker(assigned, "SPECULATIVE")
    if _has_role(evidence, "contradicting"):
        assigned = _weaker(assigned, "INFERRED")
        if assigned == "OBSERVED":
            assigned = "INFERRED"
    supporting = [item for item in evidence if item.role == "supporting"]
    if assigned == "OBSERVED" and (
        not supporting or any(item.kind != "observation" for item in supporting)
    ):
        assigned = "INFERRED" if supporting else "SPECULATIVE"
    return assigned


def _assign_promotion(
    label: str,
    evidence: Sequence[EvidenceRef],
    independent_replication: bool,
) -> str:
    supporting = _has_role(evidence, "supporting")
    contradicting = _has_role(evidence, "contradicting")
    if label in {"NOT_COMPUTABLE", "SPECULATIVE"}:
        return "HOLD_SHADOW"
    if contradicting and not supporting:
        return "REJECT"
    if contradicting:
        return "HOLD_SHADOW"
    if label in {"OBSERVED", "INFERRED"} and independent_replication:
        return "ELIGIBLE_FOR_REVIEW"
    if label in {"OBSERVED", "INFERRED"}:
        return "ELIGIBLE_FOR_REPLICATION"
    return "HOLD_SHADOW"


def _has_role(evidence: Iterable[EvidenceRef], role: str) -> bool:
    return any(item.role == role for item in evidence)


def _has_kind(evidence: Iterable[EvidenceRef], kind: str) -> bool:
    return any(item.kind == kind for item in evidence)


def _weaker(current: str, cap: str) -> str:
    return current if _LABEL_RANK[current] >= _LABEL_RANK[cap] else cap


def _default_id(experiment_id: str, proposition: str) -> str:
    payload = f"{experiment_id}:{proposition}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]
