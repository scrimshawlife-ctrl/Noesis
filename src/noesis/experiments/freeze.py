from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_sha256(document: dict[str, Any]) -> str:
    payload = json.dumps(
        document,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verify_freeze_receipt(
    corpus: dict[str, Any],
    catalog: dict[str, Any],
    receipt: dict[str, Any],
) -> None:
    expected = {
        "corpus_id": corpus["corpus_id"],
        "corpus_version": corpus["version"],
        "corpus_sha256": canonical_sha256(corpus),
        "catalog_id": catalog["catalog_id"],
        "catalog_version": catalog["version"],
        "catalog_sha256": canonical_sha256(catalog),
    }
    mismatches = [
        field
        for field, value in expected.items()
        if receipt.get(field) != value
    ]
    if mismatches:
        raise ValueError(
            "EXP-001 freeze receipt does not bind the supplied inputs: "
            + ", ".join(mismatches)
        )
