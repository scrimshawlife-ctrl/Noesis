from __future__ import annotations

from typing import Any, Mapping, Sequence

import numpy as np

from noesis.artifacts.store import ContentAddressedStore
from noesis.metrics.core import cosine_similarity, euclidean_distance, linear_cka


def _vectors(
    store: ContentAddressedStore,
    left: Mapping[str, Any],
    right: Mapping[str, Any],
):
    left_art = left["artifact"]
    right_art = right["artifact"]
    return (
        store.load_vector(left_art["uri"], left_art["sha256"], left_art["shape"]),
        store.load_vector(right_art["uri"], right_art["sha256"], right_art["shape"]),
    )


def cosine_of_observations(
    store: ContentAddressedStore,
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> float:
    left_vec, right_vec = _vectors(store, left, right)
    return cosine_similarity(left_vec, right_vec)


def euclidean_of_observations(
    store: ContentAddressedStore,
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> float:
    left_vec, right_vec = _vectors(store, left, right)
    return euclidean_distance(left_vec, right_vec)


def cka_of_observation_sets(
    store: ContentAddressedStore,
    left: Sequence[Mapping[str, Any]],
    right: Sequence[Mapping[str, Any]],
) -> float:
    if len(left) != len(right) or len(left) < 2:
        raise ValueError("CKA requires two aligned observation sets with at least two samples")
    left_mat = np.stack(
        [store.load_vector(item["artifact"]["uri"], item["artifact"]["sha256"], item["artifact"]["shape"]) for item in left]
    )
    right_mat = np.stack(
        [store.load_vector(item["artifact"]["uri"], item["artifact"]["sha256"], item["artifact"]["shape"]) for item in right]
    )
    return linear_cka(left_mat, right_mat)


def replay_envelope(
    store: ContentAddressedStore,
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> dict[str, Any]:
    cosine = cosine_of_observations(store, left, right)
    distance = euclidean_of_observations(store, left, right)
    checks: dict[str, bool] = {}
    if "replay_cosine" in thresholds:
        checks["replay_cosine"] = cosine + 1e-12 >= float(thresholds["replay_cosine"])
    if "replay_euclidean" in thresholds:
        checks["replay_euclidean"] = distance - 1e-12 <= float(thresholds["replay_euclidean"])
    if thresholds.get("replay_artifact_hash_equal") is True:
        checks["replay_artifact_hash_equal"] = left["artifact"]["sha256"] == right["artifact"]["sha256"]
    return {
        "cosine": cosine,
        "euclidean": distance,
        "checks": checks,
        "within_thresholds": all(checks.values()) if checks else True,
    }
