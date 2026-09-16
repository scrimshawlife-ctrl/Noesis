from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Sequence

from noesis.settlement import EvidenceRef, SettlementRequest, settle_evidence


@dataclass(frozen=True, slots=True)
class ReplicationRequest:
    original_settlement: dict[str, Any]
    original_metrics: Sequence[float]
    replica_metrics: Sequence[float]
    original_operator: str
    replica_operator: str
    new_control_ids: Sequence[str]
    replica_settlement_id: str
    tolerance: float
    environment_delta: Sequence[str] = ()
    artifacts_resolvable: bool = True


@dataclass(frozen=True, slots=True)
class ReplicationReport:
    classification: str
    envelope: dict[str, Any]
    settlement: dict[str, Any]
    original_settlement_id: str
    environment_delta: tuple[str, ...]


def replicate_settlement(request: ReplicationRequest) -> ReplicationReport:
    original = request.original_settlement
    if "settlement_id" not in original or "proposition" not in original:
        raise ValueError("original settlement is incomplete")
    if len(request.original_metrics) != len(request.replica_metrics):
        raise ValueError("original and replica envelopes must have equal length")
    if request.tolerance < 0:
        raise ValueError("tolerance must be >= 0")

    deltas = tuple(
        abs(float(replica) - float(original_value))
        for original_value, replica in zip(request.original_metrics, request.replica_metrics, strict=True)
    )
    within = all(delta <= request.tolerance for delta in deltas)
    envelope = {
        "original": [float(value) for value in request.original_metrics],
        "replica": [float(value) for value in request.replica_metrics],
        "deltas": list(deltas),
        "tolerance": request.tolerance,
        "within_tolerance": within,
    }

    independent = request.original_operator != request.replica_operator
    has_new_control = bool(request.new_control_ids)
    if not request.artifacts_resolvable:
        classification = "NOT_COMPUTABLE"
    elif within and independent and has_new_control:
        classification = "REPLICATED"
    elif not within:
        classification = "FAILED_REPLICATION"
    else:
        classification = "PARTIAL"

    evidence = _evidence(original, request, classification)
    limitations = list(request.environment_delta)
    if classification == "NOT_COMPUTABLE":
        limitations.append("required artifacts were not resolvable by hash")
        requested = "NOT_COMPUTABLE"
        independent_flag = False
    elif classification == "FAILED_REPLICATION":
        limitations.append("replica envelope exceeded registered tolerance")
        requested = "INFERRED"
        independent_flag = False
    elif classification == "PARTIAL":
        if not independent:
            limitations.append("replica operator is not independent of the original producer")
        if not has_new_control:
            limitations.append("replication did not introduce a new control or independent fixture")
        requested = "INFERRED"
        independent_flag = False
    else:
        requested = "INFERRED"
        independent_flag = True

    settlement = settle_evidence(
        SettlementRequest(
            experiment_id=str(original.get("experiment_id", "replication")),
            proposition=f"Replication of {original['settlement_id']}: {original['proposition']}",
            evidence=evidence,
            requested_label=requested,
            created_at="2026-09-16T00:00:00Z",
            settlement_id=request.replica_settlement_id,
            independent_replication=independent_flag,
            limitations=tuple(limitations),
            confidence_basis=(f"classification={classification}",),
        )
    )
    return ReplicationReport(
        classification=classification,
        envelope=envelope,
        settlement=settlement,
        original_settlement_id=str(original["settlement_id"]),
        environment_delta=tuple(request.environment_delta),
    )


def _evidence(
    original: dict[str, Any],
    request: ReplicationRequest,
    classification: str,
) -> tuple[EvidenceRef, ...]:
    original_id = str(original["settlement_id"])
    original_payload = original_id.encode("utf-8")
    replica_payload = repr(list(request.replica_metrics)).encode("utf-8")
    items = [
        EvidenceRef(
            id=original_id,
            sha256=hashlib.sha256(original_payload).hexdigest(),
            role="supporting",
            kind="observation",
            payload=original_payload,
        ),
        EvidenceRef(
            id=request.replica_settlement_id + ":envelope",
            sha256=hashlib.sha256(replica_payload).hexdigest(),
            role="contradicting" if classification == "FAILED_REPLICATION" else "supporting",
            kind="metric",
            payload=replica_payload,
        ),
    ]
    for control_id in request.new_control_ids:
        payload = control_id.encode("utf-8")
        items.append(
            EvidenceRef(
                id=control_id,
                sha256=hashlib.sha256(payload).hexdigest(),
                role="control",
                kind="metric",
                payload=payload,
            )
        )
    return tuple(items)
