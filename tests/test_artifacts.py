import pytest

from noesis.artifacts.store import ContentAddressedStore
from noesis.metrics.compare import cosine_of_observations
from noesis.metrics.core import cosine_similarity


def test_content_addressed_store_deduplicates(tmp_path):
    store = ContentAddressedStore(tmp_path)
    sha_a, path_a = store.put_bytes(b"same", "bin")
    sha_b, path_b = store.put_bytes(b"same", "bin")
    assert sha_a == sha_b
    assert path_a == path_b
    assert path_a.read_bytes() == b"same"


def test_content_address_changes_with_payload(tmp_path):
    store = ContentAddressedStore(tmp_path)
    sha_a, _ = store.put_bytes(b"a", "bin")
    sha_b, _ = store.put_bytes(b"b", "bin")
    assert sha_a != sha_b


def test_load_vector_verifies_hash_and_shape(tmp_path):
    store = ContentAddressedStore(tmp_path)
    sha, path = store.put_vector((1.0, 0.0, 0.0))
    loaded = store.load_vector(path.as_uri(), sha, [3])
    assert list(loaded) == [1.0, 0.0, 0.0]
    with pytest.raises(ValueError, match="shape"):
        store.load_vector(path.as_uri(), sha, [2])
    path.write_bytes(b"not-the-original-payload!!!!")
    with pytest.raises(RuntimeError, match="hash mismatch"):
        store.load_vector(path.as_uri(), sha, [3])


def test_cosine_of_observations_refuses_substituted_artifact(tmp_path):
    store = ContentAddressedStore(tmp_path)
    sha_a, path_a = store.put_vector((1.0, 0.0))
    sha_b, path_b = store.put_vector((1.0, 0.0))
    left = {"artifact": {"uri": path_a.as_uri(), "sha256": sha_a, "shape": [2]}}
    right = {"artifact": {"uri": path_b.as_uri(), "sha256": sha_b, "shape": [2]}}
    assert cosine_of_observations(store, left, right) == pytest.approx(1.0)
    path_b.write_bytes(store.put_vector((0.0, 1.0))[1].read_bytes())
    with pytest.raises(RuntimeError, match="hash mismatch"):
        cosine_of_observations(store, left, right)
    assert cosine_similarity((1.0, 0.0), (0.0, 1.0)) == pytest.approx(0.0)
