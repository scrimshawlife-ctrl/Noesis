from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelIdentity:
    model_id: str
    revision: str
    tokenizer_revision: str | None = None
    weights_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class RepresentationSite:
    kind: str  # embedding | hidden_state
    layer: int | None = None
    token_index: int = -1

    def key(self) -> str:
        if self.kind == "embedding":
            return f"embedding:token={self.token_index}"
        return f"hidden_state:layer={self.layer}:token={self.token_index}"


@dataclass(frozen=True, slots=True)
class CaptureRequest:
    fixture_id: str
    text: str
    site: RepresentationSite
    seed: int


@dataclass(frozen=True, slots=True)
class CaptureResult:
    request: CaptureRequest
    model: ModelIdentity
    vector: tuple[float, ...]
    runtime_metadata: dict[str, Any]
