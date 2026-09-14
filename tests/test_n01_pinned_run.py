import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "specs/acceptance/n01-pinned-run.v1.json").read_text())
WORKFLOW = (ROOT / ".github/workflows/n01-real-model-acceptance.yml").read_text()


def test_pinned_manifest_uses_immutable_revision():
    revision = MANIFEST["revision"]
    assert len(revision) == 40
    assert all(char in "0123456789abcdef" for char in revision)
    assert MANIFEST["tokenizer_revision"] == revision


def test_workflow_defaults_match_pinned_manifest():
    for value in (
        MANIFEST["model_id"],
        MANIFEST["revision"],
        MANIFEST["fixture_text"],
    ):
        assert f'default: "{value}"' in WORKFLOW


def test_acceptance_includes_embedding_and_hidden_state_sites():
    assert "embedding" in MANIFEST["sites"]
    hidden = [site for site in MANIFEST["sites"] if site.startswith("hidden_state:")]
    assert len(hidden) >= 1
    assert MANIFEST["repeats"] >= 2


def test_pinned_run_does_not_grant_authority():
    assert all(value is False for value in MANIFEST["authority"].values())
