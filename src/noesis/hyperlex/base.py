from __future__ import annotations

from typing import Any, Protocol


class HyperlexAdapter(Protocol):
    @property
    def adapter_id(self) -> str: ...

    @property
    def adapter_version(self) -> str: ...

    def transform(self, request: dict[str, Any]) -> dict[str, Any]: ...
