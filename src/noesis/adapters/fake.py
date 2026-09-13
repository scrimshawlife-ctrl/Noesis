from __future__ import annotations

import hashlib
import random

from noesis.domain.models import CaptureRequest, CaptureResult, ModelIdentity


class DeterministicFakeAdapter:
    """Deterministic CI adapter. Not scientific evidence from a real model."""

    def __init__(self, dimensions: int = 16) -> None:
        self._dimensions = dimensions
        self._identity = ModelIdentity(
            model_id="noesis/fake-deterministic",
            revision="1",
            tokenizer_revision="none",
            weights_sha256=None,
        )

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    def capture(self, request: CaptureRequest) -> CaptureResult:
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
