from noesis.experiments import SourceFixtureSpec, TransformSpec, compile_exp001_requests


def test_exp001_plan_is_deterministic_and_preserves_declared_hypotheses():
    sources = [SourceFixtureSpec(fixture_id="source-001", text="A crossed a boundary.")]
    transforms = [
        TransformSpec(
            transform_class="literal_paraphrase",
            semantic_intent="preserve boundary-crossing event",
            expected_invariants=("boundary-crossing",),
            expected_changed_attributes=("lexical surface",),
        ),
        TransformSpec(
            transform_class="semantic_mismatch_control",
            semantic_intent="control: do not preserve target event",
            expected_invariants=(),
            expected_changed_attributes=("event semantics",),
        ),
    ]
    first = compile_exp001_requests(sources, transforms, seed=17)
    second = compile_exp001_requests(sources, transforms, seed=17)
    assert first == second
    assert len(first) == 2
    assert first[0]["expected_invariants"] == ["boundary-crossing"]
    assert first[1]["transform_class"] == "semantic_mismatch_control"


def test_exp001_plan_rejects_missing_source_identity():
    sources = [SourceFixtureSpec(fixture_id="", text="text")]
    transforms = [
        TransformSpec(
            transform_class="slang",
            semantic_intent="preserve event",
            expected_invariants=("event",),
            expected_changed_attributes=("register",),
        )
    ]
    try:
        compile_exp001_requests(sources, transforms, seed=1)
    except ValueError as exc:
        assert "fixture_id" in str(exc)
    else:
        raise AssertionError("missing source fixture identity must fail closed")
