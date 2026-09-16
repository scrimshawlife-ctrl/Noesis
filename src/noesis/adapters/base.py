from __future__ import annotations

from typing import Protocol

from noesis.domain.models import AdapterCapabilities, CaptureRequest, CaptureResult, ModelIdentity


class UnsupportedRepresentationSite(ValueError):
    pass


class UnsupportedCausalIntervention(ValueError):
    pass


class ModelAdapter(Protocol):
    @property
    def identity(self) -> ModelIdentity: ...

    @property
    def capabilities(self) -> AdapterCapabilities: ...

    def capture(self, request: CaptureRequest) -> CaptureResult: ...
