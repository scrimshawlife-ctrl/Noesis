from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


class ContractRegistry:
    def __init__(self, contracts_dir: str | Path) -> None:
        self.contracts_dir = Path(contracts_dir)

    def schema(self, name: str) -> dict[str, Any]:
        path = self.contracts_dir / f"{name}.schema.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def validate(self, name: str, instance: Any) -> None:
        validator = Draft202012Validator(self.schema(name), format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
        if errors:
            joined = "; ".join(error.message for error in errors)
            raise ValueError(f"{name} contract violation: {joined}")
