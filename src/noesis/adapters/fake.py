from __future__ import annotations

import hashlib
import random

from noesis.adapters.base import UnsupportedCausalIntervention, UnsupportedRepresentationSite
from noesis.domain.models import AdapterCapabilities, CaptureRequest, CaptureResult, ModelIdentity


class DeterministicFakeAdapter:
    """Deterministic CI adapter. Not scientific evidence from a real model."""

    def __init__(self, dimensions: int = 16, causal_intervention: bool = False) -> None:
        self._dimensions = dimensions
        self._identity = ModelIdentity(
            model_id="noesis/fake-deterministic",
            revision="1",
            tokenizer_revision="none",
            weights_sha256=None,
        )
        self._capabilities = AdapterCapabilities(
            frozenset({"embedding", "hidden_state"}),
            causal_intervention=causal_intervention,
        )

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    @property
    def capabilities(self) -> AdapterCapabilities:
        return self._capabilities

    def capture(self, request: CaptureRequest) -> CaptureResult:
        if not self.capabilities.supports(request.site):
            raise UnsupportedRepresentationSite(request.site.key())
        material = f"{request.text}|{request.site.key()}|{request.seed}|{self._dimensions}".encode()
        seed = int.from_bytes(hashlib.sha256(material).digest()[:8], "big")
        rng = random.Random(seed)
        vector = tuple(rng.uniform(-1.0, 1.0) for _ in range(self._dimensions))
        return CaptureResult(
            request=request,
            model=self.identity,
            vector=vector,
            runtime_metadata={"adapter": "deterministic_fake", "dimensions": self._dimensions},
        )

    def intervene(
        self,
        request: CaptureRequest,
        *,
        operation: str,
        magnitude: float,
    ) -> CaptureResult:
        if not self.capabilities.causal_intervention:
            raise UnsupportedCausalIntervention(self.identity.model_id)
        baseline = self.capture(request)
        if operation == "STEER":
            vector = tuple(value + magnitude for value in baseline.vector)
        elif operation == "ABLATE":
            vector = tuple(0.0 for _ in baseline.vector)
        elif operation == "INJECT":
            vector = tuple(
                value + magnitude if index == 0 else value
                for index, value in enumerate(baseline.vector)
            )
        elif operation == "PATCH":
            vector = tuple(magnitude for _ in baseline.vector)
        else:
            raise ValueError(f"unsupported intervention operation: {operation}")
        return CaptureResult(
            request=request,
            model=self.identity,
            vector=vector,
            runtime_metadata={
                "adapter": "deterministic_fake",
                "dimensions": self._dimensions,
                "operation": operation,
                "magnitude": magnitude,
            },
        )
