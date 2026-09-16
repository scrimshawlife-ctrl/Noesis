from __future__ import annotations

import hashlib

import pytest

from noesis.adapters.fake import DeterministicFakeAdapter
from noesis.contracts.registry import ContractRegistry
from noesis.domain.models import RepresentationSite
from noesis.interventions import InterventionSpec, run_intervention
from noesis.settlement import EvidenceRef, SettlementRequest, settle_evidence

SITE = RepresentationSite(kind="hidden_state", layer=1, token_index=-1)


def _spec(**overrides) -> InterventionSpec:
    base = dict(
        manifest_id="man-int-001",
        fixture_id="fx-int",
        text="synthetic causal fixture",
        site=SITE,
        seed=3,
        operation="STEER",
        magnitude=0.5,
        outcome="mean",
    )
    base.update(overrides)
    return InterventionSpec(**base)


def test_measured_intervention_is_schema_valid_and_preserves_order():
    result = run_intervention(DeterministicFakeAdapter(causal_intervention=True), _spec())
    ContractRegistry("contracts").validate("intervention-result", result)
    assert result["status"] == "MEASURED"
    assert result["operation"] == "STEER"
    assert result["configuration"]["sequence"] == ["baseline", "control", "intervention"]
    assert result["baseline_refs"]
    assert result["control_refs"]
    assert result["outcome_metric_ids"]


def test_null_steer_has_near_zero_effect():
    result = run_intervention(
        DeterministicFakeAdapter(causal_intervention=True, dimensions=8),
        _spec(magnitude=0.0),
    )
    assert result["status"] == "MEASURED"
    assert result["effect_estimate"] == pytest.approx(0.0, abs=1e-12)


def test_positive_steer_moves_outcome_in_expected_direction():
    adapter = DeterministicFakeAdapter(causal_intervention=True, dimensions=8)
    treated = run_intervention(adapter, _spec(magnitude=0.4))
    null = run_intervention(adapter, _spec(magnitude=0.0))
    assert treated["effect_estimate"] > null["effect_estimate"]
    assert treated["effect_estimate"] > 0


def test_unavailable_adapter_records_not_computable_instead_of_fabricating():
    result = run_intervention(DeterministicFakeAdapter(causal_intervention=False), _spec())
    ContractRegistry("contracts").validate("intervention-result", result)
    assert result["status"] == "NOT_COMPUTABLE"
    assert any("unavailable" in item.lower() for item in result["limitations"])
    assert result["effect_estimate"] is None


def test_failed_intervention_remains_visible():
    result = run_intervention(
        DeterministicFakeAdapter(causal_intervention=True),
        _spec(operation="OTHER", configuration_extra={"force_failure": True}),
    )
    assert result["status"] == "FAILED"
    assert result["limitations"]


def test_null_effects_are_preserved_on_the_record():
    result = run_intervention(
        DeterministicFakeAdapter(causal_intervention=True),
        _spec(magnitude=0.3),
    )
    assert "null_effect" in result["configuration"]
    assert result["configuration"]["null_effect"] == pytest.approx(0.0, abs=1e-12)


def test_causal_claim_with_intervention_evidence_is_not_observed_mechanism():
    result = run_intervention(DeterministicFakeAdapter(causal_intervention=True), _spec())
    payload = result["intervention_id"].encode("utf-8")
    settlement = settle_evidence(
        SettlementRequest(
            experiment_id="exp-int-001",
            proposition="Steering site L1 causes the hypothesized property.",
            evidence=(
                EvidenceRef(
                    id=result["intervention_id"],
                    sha256=hashlib.sha256(payload).hexdigest(),
                    role="supporting",
                    kind="intervention",
                    payload=payload,
                ),
            ),
            requested_label="OBSERVED",
            causal_claim=True,
            created_at="2026-09-16T00:00:00Z",
            settlement_id="set-int-001",
        )
    )
    assert settlement["label"] == "INFERRED"
    assert settlement["promotion"] != "ELIGIBLE_FOR_REVIEW"
