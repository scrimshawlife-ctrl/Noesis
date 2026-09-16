from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelIdentity:
    model_id: str
    revision: str
    tokenizer_revision: str | None = None
    weights_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class AdapterCapabilities:
    representation_kinds: frozenset[str]
    causal_intervention: bool = False

    def supports(self, site: "RepresentationSite") -> bool:
        return site.kind in self.representation_kinds


@dataclass(frozen=True, slots=True)
class RepresentationSite:
    kind: str
    layer: int | None = None
    token_index: int = -1

    def __post_init__(self) -> None:
        if self.kind == "hidden_state" and self.layer is None:
            raise ValueError("hidden_state requires a layer")
        if self.kind == "embedding" and self.layer is not None:
            raise ValueError("embedding does not accept a layer")

    def key(self) -> str:
        if self.kind == "embedding":
            return f"embedding:token={self.token_index}"
        return f"{self.kind}:layer={self.layer}:token={self.token_index}"


@dataclass(frozen=True, slots=True)
class InputFixture:
    fixture_id: str
    text: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()


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


@dataclass(frozen=True, slots=True)
class FailureRecord:
    experiment_id: str
    run_id: str
    fixture_id: str
    site: str
    seed: int
    error_type: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        material = "|".join(
            [self.experiment_id, self.run_id, self.fixture_id, self.site, str(self.seed), self.error_type]
        ).encode("utf-8")
        return {
            "schema_version": "0.1.0",
            "failure_id": "fail_" + hashlib.sha256(material).hexdigest()[:24],
            "experiment_id": self.experiment_id,
            "run_id": self.run_id,
            "fixture_id": self.fixture_id,
            "site": self.site,
            "seed": self.seed,
            "stage": "capture",
            "error_type": self.error_type,
            "message": self.message,
            "provenance": "OBSERVED",
        }
