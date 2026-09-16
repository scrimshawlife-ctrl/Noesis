from __future__ import annotations

import hashlib
import platform
from datetime import UTC, datetime
from typing import Callable

from noesis.adapters.base import ModelAdapter
from noesis.artifacts.store import ContentAddressedStore
from noesis.capture.fingerprint import environment_fingerprint
from noesis.domain.models import CaptureRequest, CaptureResult

Clock = Callable[[], datetime]


def _utc_now() -> datetime:
    return datetime.now(UTC)


class CaptureRunner:
    def __init__(self, adapter: ModelAdapter, store: ContentAddressedStore, clock: Clock = _utc_now) -> None:
        self.adapter = adapter
        self.store = store
        self.clock = clock

    def run(self, experiment_id: str, run_id: str, request: CaptureRequest) -> dict:
        result = self.adapter.capture(request)
        return self.record(experiment_id, run_id, result)

    def record(self, experiment_id: str, run_id: str, result: CaptureResult) -> dict:
        request = result.request
        artifact_sha, artifact_path = self.store.put_vector(result.vector)
        input_sha = hashlib.sha256(request.text.encode("utf-8")).hexdigest()
        stable_material = "|".join(
            [experiment_id, run_id, request.fixture_id, request.site.key(), artifact_sha]
        ).encode()
        observation_id = "obs_" + hashlib.sha256(stable_material).hexdigest()[:24]
        identity = result.model
        created = self.clock().astimezone(UTC).isoformat().replace("+00:00", "Z")
        environment = {
            "python": platform.python_version(),
            **result.runtime_metadata,
        }
        environment["fingerprint"] = environment_fingerprint(environment)

        observation = {
            "schema_version": "0.1.0",
            "observation_id": observation_id,
            "experiment_id": experiment_id,
            "run_id": run_id,
            "created_at": created,
            "model": {
                "family": identity.model_id,
                "revision": identity.revision,
                "weights_sha256": identity.weights_sha256,
                "tokenizer_revision": identity.tokenizer_revision or identity.revision,
            },
            "input": {
                "fixture_id": request.fixture_id,
                "transform_id": None,
                "sha256": input_sha,
            },
            "site": {
                "kind": request.site.kind,
                "layer": request.site.layer if request.site.layer is not None else 0,
                "name": request.site.key(),
            },
            "artifact": {
                "uri": artifact_path.as_uri(),
                "sha256": artifact_sha,
                "dtype": "float64",
                "shape": [len(result.vector)],
            },
            "environment": environment,
            "seed": request.seed,
            "provenance": "OBSERVED",
        }
        self.store.put_json(observation)
        return observation
