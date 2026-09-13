#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
    "specs/REQUIREMENTS.md",
    "specs/JOURNEYS.md",
    "specs/WORKFLOWS.md",
    "specs/STATE-MACHINES.md",
    "specs/CONTRACTS.md",
    "specs/DATA-MODEL.md",
    "specs/SECURITY-GOVERNANCE.md",
    "specs/ACCEPTANCE.md",
    "specs/TASKS.md",
    "specs/VERIFICATION.md",
    "specs/EXP-001-SEMANTIC-INVARIANCE.md",
    "specs/EXP-002-LATENT-COMMUNICATION.md",
    "docs/RESEARCH.md",
    "docs/HYPERLEX-INTEGRATION.md",
    "contracts/observation.schema.json",
    "contracts/settlement.schema.json",
    "contracts/experiment-manifest.schema.json",
    "contracts/metric-result.schema.json",
    "contracts/intervention-result.schema.json",
    "contracts/alignment-map.schema.json",
    "contracts/latent-channel-result.schema.json",
    "contracts/hyperlex-transform-request.schema.json",
    "contracts/hyperlex-transform-result.schema.json",
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

PROVENANCE = ("OBSERVED", "INFERRED", "SPECULATIVE", "NOT_COMPUTABLE")

ID_PATTERNS = {
    "FR-": r"\bFR-\d+",
    "NFR-": r"\bNFR-\d+",
    "J-": r"\bJ-\d+",
    "WF-": r"\bWF-\d+",
    "AC-": r"\bAC-[A-Z]+\d+",
    "T-": r"\bT-\d+",
    "V-": r"\bV-\d+",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    spec = read("specs/NOESIS-SYSTEM-SPEC.md")
    absent = [marker for marker in REQUIRED_SPEC_MARKERS if marker not in spec]
    if absent:
        fail("system spec missing sections: " + ", ".join(absent))

    schema_files = sorted(ROOT.glob("contracts/*.schema.json"))
    if len(schema_files) < 9:
        fail("expected at least nine canonical JSON schemas")
    for schema_path in schema_files:
        try:
            data = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON in {schema_path.relative_to(ROOT)}: {exc}")
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(f"{schema_path.relative_to(ROOT)} must use JSON Schema draft 2020-12")
        if "required" not in data or "properties" not in data:
            fail(f"{schema_path.relative_to(ROOT)} lacks required/properties declarations")
        if not data.get("$id") or not data.get("title"):
            fail(f"{schema_path.relative_to(ROOT)} lacks $id/title")

    canonical_text = {
        "FR-": read("specs/REQUIREMENTS.md"),
        "NFR-": read("specs/REQUIREMENTS.md"),
        "J-": read("specs/JOURNEYS.md"),
        "WF-": read("specs/WORKFLOWS.md"),
        "AC-": read("specs/ACCEPTANCE.md"),
        "T-": read("specs/TASKS.md"),
        "V-": read("specs/VERIFICATION.md"),
    }
    for prefix, text in canonical_text.items():
        if not re.search(ID_PATTERNS[prefix], text):
            fail(f"canonical spec missing {prefix} identifiers")

    traceability = read("TRACEABILITY.md")
    for prefix in ID_PATTERNS:
        if prefix not in traceability:
            fail(f"traceability missing {prefix} references")

    constitution = read("CONSTITUTION.md")
    for label in PROVENANCE:
        if label not in constitution:
            fail(f"constitution missing provenance label {label}")

    security = read("specs/SECURITY-GOVERNANCE.md")
    for marker in ("ADVISORY_ONLY", "FIELD", "PROMOTION_ELIGIBLE"):
        if marker not in security:
            fail(f"security/governance spec missing {marker}")

    latent = read("specs/EXP-002-LATENT-COMMUNICATION.md")
    if "BLOCKED" not in latent or "AC-N4" not in latent:
        fail("latent communication experiment must remain gated by AC-N4")

    hyperlex = read("docs/HYPERLEX-INTEGRATION.md")
    for marker in ("ADAPTER_READY", "MODEL_BINDING_PENDING", "may not state"):
        if marker not in hyperlex:
            fail(f"Hyperlex integration boundary missing {marker}")

    print("Noesis specification validation: PASS")


if __name__ == "__main__":
    main()
