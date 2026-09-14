from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import numpy as np


class ContentAddressedStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def digest(payload: bytes) -> str:
        return hashlib.sha256(payload).hexdigest()

    def put_bytes(self, payload: bytes, suffix: str) -> tuple[str, Path]:
        sha = self.digest(payload)
        path = self.root / sha[:2] / f"{sha}.{suffix.lstrip('.')}"
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(payload)
        elif path.read_bytes() != payload:
            raise RuntimeError(f"content-addressed artifact mismatch for {sha}")
        return sha, path

    def verify_path(self, path: str | Path, expected_sha256: str) -> bool:
        candidate = Path(path).resolve()
        if not candidate.is_file():
            raise FileNotFoundError(candidate)
        actual = self.digest(candidate.read_bytes())
        if actual != expected_sha256:
            raise RuntimeError(
                f"artifact hash mismatch: expected {expected_sha256}, got {actual}"
            )
        return True

    def verify_uri(self, uri: str, expected_sha256: str) -> bool:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            raise ValueError("only file:// artifact URIs are accepted by the local store verifier")
        return self.verify_path(Path(unquote(parsed.path)), expected_sha256)

    def put_json(self, value: Any) -> tuple[str, Path]:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        return self.put_bytes(payload, "json")

    def put_vector(self, vector: tuple[float, ...]) -> tuple[str, Path]:
        array = np.asarray(vector, dtype=np.float64)
        if not np.all(np.isfinite(array)):
            raise ValueError("vector contains non-finite values")
        return self.put_bytes(array.tobytes(order="C"), "f64")
