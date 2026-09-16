from __future__ import annotations

import hashlib

from noesis.capture.fingerprint import environment_fingerprint
from noesis.contracts.registry import ContractRegistry
from noesis.replication import ReplicationRequest, replicate_settlement
from noesis.settlement import EvidenceRef, SettlementRequest, settle_evidence


def _original() -> dict:
    payload = b"original-metric"
    return settle_evidence(
        SettlementRequest(
            experiment_id="exp-rep-001",
            proposition="Repeated captures match within tolerance.",
            evidence=(
                EvidenceRef(
                    id="obs-orig",
                    sha256=hashlib.sha256(payload).hexdigest(),
                    role="supporting",
                    kind="observation",
                    payload=payload,
                ),
            ),
            requested_label="OBSERVED",
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-orig-001",
        )
    )


def test_independent_rerun_within_tolerance_is_replicated():
    original = _original()
    snapshot = dict(original)
    report = replicate_settlement(
        ReplicationRequest(
            original_settlement=original,
            original_metrics=(0.99, 0.02),
            replica_metrics=(0.988, 0.021),
            original_operator="operator:a",
            replica_operator="operator:b",
            new_control_ids=("ctrl-new-1",),
            replica_settlement_id="set-rep-001",
            tolerance=0.05,
            environment_delta=("python 3.12 vs 3.12",),
        )
    )
    assert original == snapshot
    assert report.classification == "REPLICATED"
    assert report.envelope["within_tolerance"] is True
    ContractRegistry("contracts").validate("settlement", report.settlement)
    assert report.settlement["settlement_id"] == "set-rep-001"
    assert report.settlement["settlement_id"] != original["settlement_id"]
    assert report.settlement["promotion"] == "ELIGIBLE_FOR_REVIEW"


def test_envelope_outside_tolerance_is_failed_replication():
    original = _original()
    report = replicate_settlement(
        ReplicationRequest(
            original_settlement=original,
            original_metrics=(0.99,),
            replica_metrics=(0.10,),
            original_operator="operator:a",
            replica_operator="operator:b",
            new_control_ids=("ctrl-new-1",),
            replica_settlement_id="set-rep-fail",
            tolerance=0.05,
            environment_delta=(),
        )
    )
    assert report.classification == "FAILED_REPLICATION"
    assert report.envelope["within_tolerance"] is False
    assert report.settlement["label"] != "OBSERVED"
    assert any(item["role"] == "contradicting" for item in report.settlement["evidence"])


def test_unresolvable_artifacts_are_not_computable():
    original = _original()
    snapshot = dict(original)
    report = replicate_settlement(
        ReplicationRequest(
            original_settlement=original,
            original_metrics=(0.99,),
            replica_metrics=(0.99,),
            original_operator="operator:a",
            replica_operator="operator:b",
            new_control_ids=("ctrl-new-1",),
            replica_settlement_id="set-rep-missing",
            tolerance=0.05,
            artifacts_resolvable=False,
            environment_delta=("artifact store unavailable",),
        )
    )
    assert original == snapshot
    assert report.classification == "NOT_COMPUTABLE"
    assert report.settlement["label"] == "NOT_COMPUTABLE"
    assert report.environment_delta


def test_same_operator_cannot_fully_replicate():
    original = _original()
    report = replicate_settlement(
        ReplicationRequest(
            original_settlement=original,
            original_metrics=(0.5,),
            replica_metrics=(0.5,),
            original_operator="operator:a",
            replica_operator="operator:a",
            new_control_ids=("ctrl-new-1",),
            replica_settlement_id="set-rep-same-op",
            tolerance=0.05,
            environment_delta=(),
        )
    )
    assert report.classification == "PARTIAL"
    assert report.settlement["promotion"] != "ELIGIBLE_FOR_REVIEW"


def test_equivalent_environment_requirement_blocks_full_replication():
    original = _original()
    original_env = {"python": "3.12.3", "adapter": "fake"}
    replica_env = {"python": "3.13.0", "adapter": "fake"}
    original_env = {**original_env, "fingerprint": environment_fingerprint(original_env)}
    replica_env = {**replica_env, "fingerprint": environment_fingerprint(replica_env)}
    report = replicate_settlement(
        ReplicationRequest(
            original_settlement=original,
            original_metrics=(0.5,),
            replica_metrics=(0.5,),
            original_operator="operator:a",
            replica_operator="operator:b",
            new_control_ids=("ctrl-new-1",),
            replica_settlement_id="set-rep-env",
            tolerance=0.05,
            original_environment=original_env,
            replica_environment=replica_env,
            require_equivalent_environment=True,
        )
    )
    assert report.classification == "PARTIAL"
    assert report.fingerprint_report["status"] == "NEW_RUN_REQUIRED"
    assert "python" in report.environment_delta


def test_missing_new_control_is_partial():
    original = _original()
    report = replicate_settlement(
        ReplicationRequest(
            original_settlement=original,
            original_metrics=(0.5,),
            replica_metrics=(0.5,),
            original_operator="operator:a",
            replica_operator="operator:b",
            new_control_ids=(),
            replica_settlement_id="set-rep-no-ctrl",
            tolerance=0.05,
            environment_delta=(),
        )
    )
    assert report.classification == "PARTIAL"
