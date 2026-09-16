from __future__ import annotations

from typing import Any, Mapping

from noesis.artifacts.store import ContentAddressedStore
from noesis.metrics.core import cosine_similarity


def cosine_of_observations(
    store: ContentAddressedStore,
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> float:
    left_art = left["artifact"]
    right_art = right["artifact"]
    left_vec = store.load_vector(left_art["uri"], left_art["sha256"], left_art["shape"])
    right_vec = store.load_vector(right_art["uri"], right_art["sha256"], right_art["shape"])
    return cosine_similarity(left_vec, right_vec)
