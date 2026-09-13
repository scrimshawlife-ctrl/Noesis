from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from typing import Any
from urllib import request as urllib_request

from noesis.contracts.registry import validate_contract


class DeterministicHyperlexAdapter:
    """Test-only adapter that preserves semantic metadata and deterministically rewrites text."""

    adapter_id = "noesis/hyperlex-deterministic"
    adapter_version = "1"

    def transform(self, request: dict[str, Any]) -> dict[str, Any]:
        validate_contract("hyperlex-transform-request", request)
        output_text = f"[{request['transform_class']}] {request['source_text']}"
        digest = hashlib.sha256(output_text.encode("utf-8")).hexdigest()
        result = {
            "schema_version": "1.0.0",
            "transform_id": f"hx-{digest[:16]}",
            "request_id": request["request_id"],
            "source_fixture_id": request["source_fixture_id"],
            "output_text": output_text,
            "transform_class": request["transform_class"],
            "transform_version": self.adapter_version,
            "transform_sha256": digest,
            "semantic_intent": request["semantic_intent"],
            "expected_invariants": list(request["expected_invariants"]),
            "expected_changed_attributes": list(request["expected_changed_attributes"]),
            "provider_metadata": {"adapter_id": self.adapter_id},
            "provenance": "OBSERVED",
        }
        validate_contract("hyperlex-transform-result", result)
        return result


class CallableHyperlexAdapter:
    """Wrap a local model/service function without coupling Noesis to its implementation."""

    def __init__(self, fn: Callable[[dict[str, Any]], dict[str, Any]], *, adapter_id: str, adapter_version: str) -> None:
        self._fn = fn
        self._adapter_id = adapter_id
        self._adapter_version = adapter_version

    @property
    def adapter_id(self) -> str:
        return self._adapter_id

    @property
    def adapter_version(self) -> str:
        return self._adapter_version

    def transform(self, request: dict[str, Any]) -> dict[str, Any]:
        validate_contract("hyperlex-transform-request", request)
        result = dict(self._fn(dict(request)))
        result.setdefault("provider_metadata", {})
        result["provider_metadata"] = {
            **result["provider_metadata"],
            "adapter_id": self.adapter_id,
            "adapter_version": self.adapter_version,
        }
        validate_contract("hyperlex-transform-result", result)
        return result


class HttpHyperlexAdapter:
    """Minimal JSON-over-HTTP transport adapter for a future trained Hyperlex service."""

    def __init__(self, endpoint: str, *, adapter_id: str = "hyperlex/http", adapter_version: str = "1", timeout_seconds: float = 30.0) -> None:
        self.endpoint = endpoint
        self._adapter_id = adapter_id
        self._adapter_version = adapter_version
        self.timeout_seconds = timeout_seconds

    @property
    def adapter_id(self) -> str:
        return self._adapter_id

    @property
    def adapter_version(self) -> str:
        return self._adapter_version

    def transform(self, request: dict[str, Any]) -> dict[str, Any]:
        validate_contract("hyperlex-transform-request", request)
        payload = json.dumps(request, sort_keys=True).encode("utf-8")
        req = urllib_request.Request(
            self.endpoint,
            data=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=self.timeout_seconds) as response:  # nosec B310 - endpoint is operator-configured
            result = json.loads(response.read().decode("utf-8"))
        if not isinstance(result, dict):
            raise ValueError("Hyperlex HTTP response must be a JSON object")
        result.setdefault("provider_metadata", {})
        result["provider_metadata"] = {
            **result["provider_metadata"],
            "adapter_id": self.adapter_id,
            "adapter_version": self.adapter_version,
            "endpoint": self.endpoint,
        }
        validate_contract("hyperlex-transform-result", result)
        return result
