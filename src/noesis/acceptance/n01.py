from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from noesis.adapters.base import ModelAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.capture.runner import CaptureRunner
from noesis.domain.models import CaptureRequest, RepresentationSite
from noesis.metrics.core import cosine_similarity, euclidean_distance


@dataclass(frozen=True, slots=True)
class N01AcceptanceConfig:
    experiment_id: str
    fixture_id: str
    text: str
    sites: tuple[RepresentationSite, ...]
    seed: int = 0
    repeats: int = 2
    cosine_floor: float = 0.999999
    euclidean_ceiling: float = 1e-9


def run_n01_acceptance(
    adapter: ModelAdapter,
    store: ContentAddressedStore,
    config: N01AcceptanceConfig,
) -> dict:
    if config.repeats < 2:
        raise ValueError("acceptance requires at least two repeats")
    if not config.sites:
        raise ValueError("acceptance requires at least one representation site")

    runner = CaptureRunner(adapter, store)
    site_results: list[dict] = []
    overall_pass = True

    for site in config.sites:
        observations = []
        vectors = []
        failures = []
        for repeat_index in range(config.repeats):
            request = CaptureRequest(
                fixture_id=config.fixture_id,
                text=config.text,
                site=site,
                seed=config.seed,
            )
            try:
                result = adapter.capture(request)
                observation = runner.record(
                    config.experiment_id,
                    f"accept-{site.key()}-{repeat_index}",
                    result,
                )
                store.verify_uri(
                    observation["artifact"]["uri"],
                    observation["artifact"]["sha256"],
                )
                vectors.append(result.vector)
                observations.append(observation)
            except Exception as exc:  # noqa: BLE001 - evidence must preserve adapter/artifact failures
                failures.append({
                    "repeat_index": repeat_index,
                    "error_class": exc.__class__.__name__,
                    "message": str(exc),
                })

        comparisons = []
        if not failures and len(vectors) >= 2:
            baseline = vectors[0]
            for index, vector in enumerate(vectors[1:], start=1):
                cos = cosine_similarity(baseline, vector)
                euclid = euclidean_distance(baseline, vector)
                comparisons.append({
                    "against_repeat": index,
                    "cosine": cos,
                    "euclidean": euclid,
                    "within_tolerance": cos >= config.cosine_floor and euclid <= config.euclidean_ceiling,
                })
        site_pass = not failures and bool(comparisons) and all(item["within_tolerance"] for item in comparisons)
        overall_pass = overall_pass and site_pass
        site_results.append({
            "site": site.key(),
            "observations": observations,
            "failures": failures,
            "comparisons": comparisons,
            "decision": "ACCEPT" if site_pass else "REJECT",
        })

    hidden_sites = [site for site in config.sites if site.kind == "hidden_state"]
    n1_pass = overall_pass and bool(hidden_sites)
    return {
        "schema_version": "1.0.0",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "experiment_id": config.experiment_id,
        "model": {
            "model_id": adapter.identity.model_id,
            "revision": adapter.identity.revision,
            "tokenizer_revision": adapter.identity.tokenizer_revision,
            "weights_sha256": adapter.identity.weights_sha256,
        },
        "fixture": {
            "fixture_id": config.fixture_id,
            "seed": config.seed,
        },
        "tolerance": {
            "cosine_floor": config.cosine_floor,
            "euclidean_ceiling": config.euclidean_ceiling,
        },
        "site_results": site_results,
        "gate_decisions": {
            "AC-N0": "ACCEPT" if overall_pass else "REJECT",
            "AC-N1": "ACCEPT" if n1_pass else ("REJECT" if hidden_sites else "NOT_COMPUTABLE"),
        },
        "limitations": [
            "This packet evaluates capture reproducibility only; it does not establish semantic invariance or mechanistic interpretation."
        ],
    }
