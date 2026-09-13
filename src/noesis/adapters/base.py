from __future__ import annotations

from typing import Protocol

from noesis.domain.models import CaptureRequest, CaptureResult, ModelIdentity


class ModelAdapter(Protocol):
    @property
    def identity(self) -> ModelIdentity: ...

    def capture(self, request: CaptureRequest) -> CaptureResult: ...
