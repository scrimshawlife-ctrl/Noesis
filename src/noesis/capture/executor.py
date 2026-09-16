from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable

from noesis.adapters.base import ModelAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.capture.runner import CaptureRunner
from noesis.contracts.registry import ContractRegistry
from noesis.domain.models import CaptureRequest, FailureRecord, InputFixture, RepresentationSite
from noesis.security import classify_fixture

_SITE_RE = re.compile(r"^(embedding|hidden_state)(?::layer=(-?\d+))?:token=(-?\d+)$")


def parse_site(value: str) -> RepresentationSite:
    match = _SITE_RE.match(value)
    if not match:
        raise ValueError(f"invalid representation site: {value}")
    kind, layer, token = match.groups()
    return RepresentationSite(kind=kind, layer=int(layer) if layer is not None else None, token_index=int(token))


@dataclass(frozen=True, slots=True)
class ExecutionReport:
    observations: tuple[dict[str, Any], ...]
    failures: tuple[dict[str, Any], ...]


class ManifestExecutor:
    def __init__(
        self,
        adapter: ModelAdapter,
        store: ContentAddressedStore,
        registry: ContractRegistry,
        runner: CaptureRunner | None = None,
    ) -> None:
        self.adapter = adapter
        self.store = store
        self.registry = registry
        self.runner = runner or CaptureRunner(adapter, store)

    def execute(
        self,
        manifest: dict[str, Any],
        fixtures: Iterable[InputFixture],
        run_id: str,
    ) -> ExecutionReport:
        self.registry.validate("experiment-manifest", manifest)
        fixture_map = {fixture.fixture_id: fixture for fixture in fixtures}
        observations: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []

        for fixture_id in manifest["fixture_ids"]:
            fixture = fixture_map.get(fixture_id)
            if fixture is None:
                failures.append(self._failure(manifest["experiment_id"], run_id, fixture_id, "fixture", 0, KeyError(fixture_id)))
                continue
            try:
                classify_fixture(
                    {
                        "text": fixture.text,
                        "data_classification": fixture.data_classification,
                        "retention": fixture.retention,
                        "access_scope": fixture.access_scope,
                    }
                )
            except ValueError as exc:
                failures.append(
                    self._failure(manifest["experiment_id"], run_id, fixture_id, "classification", 0, exc)
                )
                continue
            for site_text in manifest["representation_sites"]:
                for seed in manifest["seeds"]:
                    try:
                        site = parse_site(site_text)
                        request = CaptureRequest(fixture_id=fixture_id, text=fixture.text, site=site, seed=seed)
                        observation = self.runner.run(manifest["experiment_id"], run_id, request)
                        self.registry.validate("observation", observation)
                        observations.append(observation)
                    except Exception as exc:  # failures are evidence; continue independent cells
                        failures.append(self._failure(manifest["experiment_id"], run_id, fixture_id, site_text, seed, exc))

        return ExecutionReport(tuple(observations), tuple(failures))

    def _failure(self, experiment_id: str, run_id: str, fixture_id: str, site: str, seed: int, exc: Exception) -> dict[str, Any]:
        record = FailureRecord(
            experiment_id=experiment_id,
            run_id=run_id,
            fixture_id=fixture_id,
            site=site,
            seed=seed,
            error_type=type(exc).__name__,
            message=str(exc),
        ).as_dict()
        self.registry.validate("failure-record", record)
        self.store.put_json(record)
        return record
