from __future__ import annotations

import hashlib

import pytest

from noesis.contracts.registry import ContractRegistry
from noesis.settlement import EvidenceRef, SettlementRequest, settle_evidence, supersede_settlement


def digest(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def observation(role: str = "supporting", body: str = "obs-a") -> EvidenceRef:
    payload = body.encode("utf-8")
    return EvidenceRef(
        id=f"obs-{body}",
        sha256=hashlib.sha256(payload).hexdigest(),
        role=role,
        kind="observation",
        payload=payload,
    )


def test_supporting_observations_settle_observed_and_validate_contract():
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Repeated captures of fixture A are identical within tolerance.",
            evidence=(observation(),),
            requested_label="OBSERVED",
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-001",
        )
    )
    ContractRegistry("contracts").validate("settlement", settlement)
    assert settlement["label"] == "OBSERVED"
    assert settlement["governance_effect"] == "ADVISORY_ONLY"
    assert settlement["promotion"] == "ELIGIBLE_FOR_REPLICATION"
    assert settlement["evidence"][0]["role"] == "supporting"


def test_missing_required_evidence_is_not_computable():
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Hidden-state site L12 was captured.",
            evidence=(observation(),),
            required_ids=("obs-missing",),
            requested_label="OBSERVED",
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-missing",
        )
    )
    ContractRegistry("contracts").validate("settlement", settlement)
    assert settlement["label"] == "NOT_COMPUTABLE"
    assert settlement["promotion"] == "HOLD_SHADOW"
    assert "obs-missing" in settlement["unresolved"]


def test_hash_mismatch_cannot_cite_nonexistent_evidence():
    bad = EvidenceRef(
        id="obs-bad",
        sha256="a" * 64,
        role="supporting",
        kind="observation",
        payload=b"not-matching",
    )
    with pytest.raises(ValueError, match="nonexistent evidence"):
        settle_evidence(
            SettlementRequest(
                experiment_id="exp-settle-001",
                proposition="A claim",
                evidence=(bad,),
                created_at="2026-09-16T00:00:00Z",
                settlement_id="set-bad-hash",
            )
        )


def test_contradictions_remain_represented_and_block_observed():
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Feature F tracks agency.",
            evidence=(
                observation("supporting", "pos"),
                observation("contradicting", "neg"),
            ),
            requested_label="OBSERVED",
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-contradict",
        )
    )
    roles = {item["id"]: item["role"] for item in settlement["evidence"]}
    assert roles["obs-pos"] == "supporting"
    assert roles["obs-neg"] == "contradicting"
    assert settlement["label"] != "OBSERVED"
    assert settlement["promotion"] in {"HOLD_SHADOW", "REJECT"}


def test_causal_claim_without_intervention_is_bounded():
    metric = EvidenceRef(
        id="metric-1",
        sha256=digest("metric"),
        role="supporting",
        kind="metric",
        payload=b"metric",
    )
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Steering site L8 causes the agency feature to fire.",
            evidence=(metric,),
            requested_label="OBSERVED",
            causal_claim=True,
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-causal",
        )
    )
    assert settlement["label"] in {"SPECULATIVE", "NOT_COMPUTABLE"}
    assert settlement["promotion"] == "HOLD_SHADOW"
    assert any("intervention" in item.lower() for item in settlement["limitations"])


def test_review_promotion_requires_independent_replication():
    with_replication = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Repeated captures match.",
            evidence=(observation(),),
            requested_label="OBSERVED",
            independent_replication=True,
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-repl",
        )
    )
    without = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Repeated captures match.",
            evidence=(observation(),),
            requested_label="OBSERVED",
            independent_replication=False,
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-no-repl",
        )
    )
    assert with_replication["promotion"] == "ELIGIBLE_FOR_REVIEW"
    assert without["promotion"] != "ELIGIBLE_FOR_REVIEW"


def test_control_only_evidence_cannot_be_observed():
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Feature F tracks agency.",
            evidence=(observation("control", "ctrl"),),
            requested_label="OBSERVED",
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-control-only",
        )
    )
    assert settlement["label"] != "OBSERVED"
    assert settlement["promotion"] == "HOLD_SHADOW"


def test_empty_evidence_fails_closed():
    with pytest.raises(ValueError, match="evidence"):
        settle_evidence(
            SettlementRequest(
                experiment_id="exp-settle-001",
                proposition="Anything",
                evidence=(),
                created_at="2026-09-16T00:00:00Z",
                settlement_id="set-empty",
            )
        )


def test_supersession_preserves_original_settlement():
    original = settle_evidence(
        SettlementRequest(
            experiment_id="exp-settle-001",
            proposition="Repeated captures match.",
            evidence=(observation(),),
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-old",
        )
    )
    snapshot = dict(original)
    record = supersede_settlement(
        original,
        successor_ref="set-new",
        reason="method invalidated",
        actor="operator:test",
        created_at="2026-09-16T01:00:00Z",
        supersession_id="sup-001",
    )
    ContractRegistry("contracts").validate("supersession", record)
    assert original == snapshot
    assert record["old_object_id"] == "set-old"
    assert record["successor_ref"] == "set-new"
