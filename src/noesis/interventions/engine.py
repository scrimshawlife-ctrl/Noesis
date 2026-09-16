from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping, Protocol

from noesis.contracts.registry import validate_contract
from noesis.domain.models import CaptureRequest, CaptureResult, RepresentationSite

_CREATED = datetime(2026, 9, 16, tzinfo=UTC).isoformat()
_OPERATIONS = frozenset({"PATCH", "ABLATE", "STEER", "INJECT", "OTHER"})


class _CausalAdapter(Protocol):
    @property
    def capabilities(self) -> Any: ...

    def capture(self, request: CaptureRequest) -> CaptureResult: ...

    def intervene(
        self,
        request: CaptureRequest,
        *,
        operation: str,
        magnitude: float,
    ) -> CaptureResult: ...


@dataclass(frozen=True, slots=True)
class InterventionSpec:
    manifest_id: str
    fixture_id: str
    text: str
    site: RepresentationSite
    seed: int
    operation: str
    magnitude: float
    outcome: str = "mean"
    source_site: str | None = None
    configuration_extra: Mapping[str, Any] = field(default_factory=dict)


def run_intervention(adapter: _CausalAdapter, spec: InterventionSpec) -> dict[str, Any]:
    if spec.operation not in _OPERATIONS:
        raise ValueError(f"unknown intervention operation: {spec.operation}")
    request = CaptureRequest(
        fixture_id=spec.fixture_id,
        text=spec.text,
        site=spec.site,
        seed=spec.seed,
    )
    intervention_id = _identity(spec)
    if not adapter.capabilities.causal_intervention:
        return _result(
            spec,
            intervention_id,
            status="NOT_COMPUTABLE",
            baseline_refs=("unavailable",),
            control_refs=("unavailable",),
            outcome_metric_ids=("unavailable",),
            effect=None,
            configuration={"sequence": ["baseline", "control", "intervention"]},
            limitations=("causal access unavailable for this adapter",),
        )
    if spec.configuration_extra.get("force_failure"):
        return _result(
            spec,
            intervention_id,
            status="FAILED",
            baseline_refs=(f"{intervention_id}:baseline",),
            control_refs=(f"{intervention_id}:control",),
            outcome_metric_ids=(f"{intervention_id}:effect",),
            effect=None,
            configuration={"sequence": ["baseline", "control", "intervention"]},
            limitations=("intervention failed and remains visible",),
        )

    baseline = adapter.capture(request)
    control = adapter.intervene(request, operation="STEER", magnitude=0.0)
    treated = adapter.intervene(request, operation=spec.operation, magnitude=spec.magnitude)
    baseline_outcome = _outcome(baseline, spec.outcome)
    control_outcome = _outcome(control, spec.outcome)
    treated_outcome = _outcome(treated, spec.outcome)
    effect = treated_outcome - baseline_outcome
    null_effect = control_outcome - baseline_outcome
    return _result(
        spec,
        intervention_id,
        status="MEASURED",
        baseline_refs=(f"{intervention_id}:baseline",),
        control_refs=(f"{intervention_id}:control",),
        outcome_metric_ids=(f"{intervention_id}:effect",),
        effect=effect,
        configuration={
            "sequence": ["baseline", "control", "intervention"],
            "magnitude": spec.magnitude,
            "outcome": spec.outcome,
            "null_effect": null_effect,
            "baseline_outcome": baseline_outcome,
            "control_outcome": control_outcome,
            "treated_outcome": treated_outcome,
        },
        limitations=("synthetic adapter interventions are not scientific model evidence",),
    )


def _outcome(result: CaptureResult, name: str) -> float:
    if name != "mean":
        raise ValueError(f"unsupported outcome metric: {name}")
    if not result.vector:
        raise ValueError("intervention outcome requires a non-empty vector")
    return float(sum(result.vector) / len(result.vector))


def _identity(spec: InterventionSpec) -> str:
    material = (
        f"{spec.manifest_id}|{spec.fixture_id}|{spec.site.key()}|{spec.operation}|"
        f"{spec.magnitude}|{spec.seed}"
    ).encode("utf-8")
    return f"int-{hashlib.sha256(material).hexdigest()[:12]}"


def _result(
    spec: InterventionSpec,
    intervention_id: str,
    *,
    status: str,
    baseline_refs: tuple[str, ...],
    control_refs: tuple[str, ...],
    outcome_metric_ids: tuple[str, ...],
    effect: float | None,
    configuration: dict[str, Any],
    limitations: tuple[str, ...],
) -> dict[str, Any]:
    record = {
        "schema_version": "1.0.0",
        "intervention_id": intervention_id,
        "manifest_id": spec.manifest_id,
        "operation": spec.operation,
        "source_site": spec.source_site,
        "target_site": spec.site.key(),
        "configuration": {**dict(spec.configuration_extra), **configuration},
        "baseline_refs": list(baseline_refs),
        "control_refs": list(control_refs),
        "outcome_metric_ids": list(outcome_metric_ids),
        "effect_estimate": effect,
        "uncertainty": None,
        "status": status,
        "limitations": list(limitations),
        "created_at_utc": _CREATED,
    }
    validate_contract("intervention-result", record)
    return record
