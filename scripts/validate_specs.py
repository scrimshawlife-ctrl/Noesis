#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "CONSTITUTION.md",
    "ARCHITECTURE.md",
    "AGENTS.md",
    "GLOSSARY.md",
    "STATUS.md",
    "PLANS.md",
    "TRACEABILITY.md",
    "specs/NOESIS-SYSTEM-SPEC.md",
    "specs/EXP-001-SEMANTIC-INVARIANCE.md",
    "specs/EXP-002-LATENT-COMMUNICATION.md",
    "docs/RESEARCH.md",
    "contracts/observation.schema.json",
    "contracts/settlement.schema.json",
]

REQUIRED_SPEC_MARKERS = [
    "## 3. Requirements",
    "## 4. Journeys",
    "## 5. Workflows",
    "## 6. State machines",
    "## 7. Contracts",
    "## 8. Data model",
    "## 9. Security, privacy, governance",
    "## 10. Architecture",
    "## 11. Acceptance criteria",
    "## 12. Traceability",
    "## 13. Implementation task families",
    "## 14. Verification",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    spec = (ROOT / "specs/NOESIS-SYSTEM-SPEC.md").read_text(encoding="utf-8")
    absent = [marker for marker in REQUIRED_SPEC_MARKERS if marker not in spec]
    if absent:
        fail("system spec missing sections: " + ", ".join(absent))

    for schema_path in ROOT.glob("contracts/*.schema.json"):
        try:
            data = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON in {schema_path.relative_to(ROOT)}: {exc}")
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(f"{schema_path.relative_to(ROOT)} must use JSON Schema draft 2020-12")
        if "required" not in data or "properties" not in data:
            fail(f"{schema_path.relative_to(ROOT)} lacks required/properties declarations")

    traceability = (ROOT / "TRACEABILITY.md").read_text(encoding="utf-8")
    for prefix in ("FR-", "WF-", "AC-"):
        if prefix not in traceability:
            fail(f"traceability missing {prefix} references")

    constitution = (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
    for label in ("OBSERVED", "INFERRED", "SPECULATIVE", "NOT_COMPUTABLE"):
        if label not in constitution:
            fail(f"constitution missing provenance label {label}")

    print("Noesis specification validation: PASS")


if __name__ == "__main__":
    main()
