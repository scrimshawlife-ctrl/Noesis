from noesis.capture.fingerprint import compare_environment_fingerprints, environment_fingerprint


def test_same_environment_has_stable_fingerprint():
    env = {"python": "3.12.3", "adapter": "deterministic_fake"}
    assert environment_fingerprint(env) == environment_fingerprint(dict(env))
    assert environment_fingerprint({**env, "fingerprint": "ignored"}) == environment_fingerprint(env)


def test_material_change_requires_new_run_identity():
    original = {"python": "3.12.3", "adapter": "deterministic_fake"}
    current = {"python": "3.13.0", "adapter": "deterministic_fake"}
    original = {**original, "fingerprint": environment_fingerprint(original)}
    current = {**current, "fingerprint": environment_fingerprint(current)}
    report = compare_environment_fingerprints(original, current)
    assert report["status"] == "NEW_RUN_REQUIRED"
    assert "python" in report["delta"]
    assert compare_environment_fingerprints(original, original)["status"] == "EQUIVALENT"
