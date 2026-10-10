import json

import pytest

from noesis.contracts.epistemic_interchange import (
    append_provenance,
    assert_no_silent_promotion,
    canonical_sha256,
    validate_interchange_object,
)


def fixture():
    return json.loads(open("examples/epistemic-interchange-object.example.json", encoding="utf-8").read())


def test_eic_example_validates():
    validate_interchange_object(fixture())


def test_eic_canonical_hash_is_key_order_invariant():
    item = fixture()
    reversed_item = dict(reversed(list(item.items())))
    assert canonical_sha256(item) == canonical_sha256(reversed_item)


def test_eic_missing_evidence_fails_closed():
    item = fixture()
    item["evidence_refs"] = []
    with pytest.raises(ValueError):
        validate_interchange_object(item)


def test_noesis_q1_rejects_silent_observed_to_interpreted_promotion():
    before = fixture()
    after = fixture()
    after["epistemic_status"] = "INTERPRETED"
    with pytest.raises(ValueError, match="silent epistemic promotion"):
        assert_no_silent_promotion(before, after)


def test_noesis_q1_allows_bounded_interpretation_with_new_evidence_assertion():
    before = fixture()
    after = fixture()
    after["epistemic_status"] = "INTERPRETED"
    after["assertions"] = [{
        "assertion_id": "interpretation-1",
        "class": "INTERPRETATION",
        "component": "Noesis",
        "evidence_refs": ["sha256:example-observation"],
        "limitations": ["Q1 synthetic fixture only"],
    }]
    validate_interchange_object(after)
    assert_no_silent_promotion(before, after)


def test_noesis_q1_preserves_not_computable():
    before = fixture()
    after = fixture()
    after["epistemic_status"] = "NOT_COMPUTABLE"
    assert_no_silent_promotion(before, after)


def test_provenance_append_preserves_history():
    before = fixture()
    previous = list(before["provenance"])
    event = {
        "event_id": "prov-example-002",
        "component": "Noesis",
        "operation": "Q1_VALIDATE",
        "utc_time": "2026-09-19T20:00:00Z",
        "input_hashes": [canonical_sha256(before)],
        "output_hash": "sha256:q1-output",
        "revision": "codex/epistemic-interchange-q1",
        "authority": "Noesis Q1 qualification",
    }
    after = append_provenance(before, event, expected_previous_hash=canonical_sha256(before))
    assert after["provenance"][:-1] == previous
    assert len(after["provenance"]) == len(previous) + 1


def test_provenance_append_rejects_stale_input_hash():
    with pytest.raises(ValueError, match="hash mismatch"):
        append_provenance(fixture(), {
            "event_id": "prov-example-002",
            "component": "Noesis",
            "operation": "Q1_VALIDATE",
            "utc_time": "2026-09-19T20:00:00Z",
            "input_hashes": ["sha256:stale"],
            "output_hash": "sha256:q1-output",
            "authority": "Noesis Q1 qualification",
        }, expected_previous_hash="deadbeef")
