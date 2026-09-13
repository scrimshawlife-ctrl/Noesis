import hashlib

import pytest

from noesis.hyperlex import CallableHyperlexAdapter, DeterministicHyperlexAdapter, materialize_transform_result


def request_fixture():
    return {
        "schema_version": "1.0.0",
        "request_id": "req-001",
        "source_fixture_id": "source-001",
        "source_text": "The king betrayed his brother.",
        "transform_class": "slang",
        "semantic_intent": "preserve betrayal while changing register",
        "expected_invariants": ["betrayal", "agent-patient relation"],
        "expected_changed_attributes": ["register", "lexical surface"],
        "seed": 7,
        "parameters": {},
    }


def test_deterministic_adapter_materializes_replayable_fixture():
    adapter = DeterministicHyperlexAdapter()
    first = adapter.transform(request_fixture())
    second = adapter.transform(request_fixture())
    assert first == second

    fixture = materialize_transform_result(first)
    assert fixture.transform_id == first["transform_id"]
    assert fixture.sha256 == hashlib.sha256(fixture.text.encode("utf-8")).hexdigest()
    assert fixture.expected_invariants == ("betrayal", "agent-patient relation")


def test_callable_adapter_does_not_grant_semantic_truth_authority():
    req = request_fixture()

    def transform(payload):
        text = payload["source_text"].upper()
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return {
            "schema_version": "1.0.0",
            "transform_id": "hx-callable-001",
            "request_id": payload["request_id"],
            "source_fixture_id": payload["source_fixture_id"],
            "output_text": text,
            "transform_class": payload["transform_class"],
            "transform_version": "training-snapshot",
            "transform_sha256": digest,
            "semantic_intent": payload["semantic_intent"],
            "expected_invariants": payload["expected_invariants"],
            "expected_changed_attributes": payload["expected_changed_attributes"],
            "provider_metadata": {},
            "provenance": "OBSERVED",
        }

    adapter = CallableHyperlexAdapter(transform, adapter_id="hyperlex/local", adapter_version="training-snapshot")
    result = adapter.transform(req)
    assert "latent_truth" not in result
    assert result["provider_metadata"]["adapter_id"] == "hyperlex/local"


def test_materializer_rejects_mutated_transform_output():
    result = DeterministicHyperlexAdapter().transform(request_fixture())
    result["output_text"] += " mutation"
    with pytest.raises(ValueError, match="hash mismatch"):
        materialize_transform_result(result)
