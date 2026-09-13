from noesis.artifacts.store import ContentAddressedStore


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
