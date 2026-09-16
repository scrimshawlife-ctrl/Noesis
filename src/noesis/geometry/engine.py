from __future__ import annotations

import copy
import hashlib
from datetime import UTC, datetime
from typing import Any, Mapping, Sequence

import numpy as np

from noesis.contracts.registry import validate_contract

_CREATED = datetime(2026, 9, 16, tzinfo=UTC).isoformat()
_EPS = 1e-12


def validate_geometry_profile(profile: Mapping[str, Any]) -> None:
    validate_contract("geometry-profile", dict(profile))
    families = {str(candidate["family"]) for candidate in profile["candidate_spaces"]}
    if "EUCLIDEAN" not in families:
        raise ValueError("geometry profile requires a Euclidean baseline")


def freeze_geometry_selection(profile: Mapping[str, Any], *, selected_id: str) -> dict[str, Any]:
    validate_geometry_profile(profile)
    ids = {str(candidate["candidate_id"]) for candidate in profile["candidate_spaces"]}
    if selected_id not in ids:
        raise ValueError(f"unknown candidate: {selected_id}")
    material = f"{profile['profile_id']}|{selected_id}".encode("utf-8")
    return {
        "profile_id": profile["profile_id"],
        "selected_id": selected_id,
        "frozen": True,
        "freeze_hash": hashlib.sha256(material).hexdigest(),
    }


def select_geometry_candidate(
    profile: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    validate_geometry_profile(profile)
    costs = {str(c["candidate_id"]): float(c["complexity_cost"]) for c in profile["candidate_spaces"]}
    penalty = float(profile["selection_rule"].get("complexity_penalty", 0.0))
    scored: list[tuple[float, str]] = []
    for result in results:
        if result.get("split") != "SELECTION" or result.get("status") != "MEASURED":
            continue
        candidate_id = str(result["candidate_id"])
        value = float(result["value"])
        scored.append((value + penalty * costs.get(candidate_id, 0.0), candidate_id))
    if not scored:
        raise ValueError("no MEASURED selection-split results to select from")
    scored.sort()
    return {"selected_id": scored[0][1], "frozen": False, "penalized_scores": scored}


def evaluate_geometry_candidate(
    profile: Mapping[str, Any],
    *,
    candidate_id: str,
    split: str,
    points,
    relations: Sequence[tuple[int, int, float]],
    frozen_selection: Mapping[str, Any] | None = None,
    result_suffix: str = "",
    extra_diagnostics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_geometry_profile(profile)
    if split == "CONFIRMATION" and not (frozen_selection and frozen_selection.get("frozen")):
        raise ValueError("confirmation partition is blocked until selection is frozen")
    candidate = _candidate(profile, candidate_id)
    matrix = _points(points, int(candidate["dimension"]))
    try:
        value = _geodesic_distortion(candidate, matrix, relations)
        status = "MEASURED"
        provenance = "OBSERVED"
        diagnostics = {"family": candidate["family"], "metric": candidate["metric"]}
    except ValueError as exc:
        if profile["failure_policy"] not in {"NOT_COMPUTABLE", "FAIL_CLOSED"}:
            raise
        value = None
        status = "NOT_COMPUTABLE"
        provenance = "NOT_COMPUTABLE"
        diagnostics = {"reason": str(exc), "family": candidate["family"]}
    if extra_diagnostics:
        diagnostics = {**diagnostics, **dict(extra_diagnostics)}
    suffix = f"-{result_suffix}" if result_suffix else ""
    result = {
        "schema_version": "0.1.0",
        "result_id": f"geo-{candidate_id}-{split.lower()}{suffix}",
        "profile_id": profile["profile_id"],
        "run_id": "geo-run-1",
        "candidate_id": candidate_id,
        "split": split,
        "metric": "geodesic_distortion",
        "value": value,
        "uncertainty": None,
        "status": status,
        "input_evidence_ids": [f"points:{candidate_id}"],
        "artifact_hash": None,
        "diagnostics": diagnostics,
        "null_result_ids": [],
        "limitations": ["geometric fit is not semantic truth or a universal geometry"],
        "provenance": provenance,
        "created_at": _CREATED,
    }
    validate_contract("geometric-metric-result", result)
    return result


def shuffled_relation_null(
    profile: Mapping[str, Any],
    *,
    candidate_id: str,
    split: str,
    points,
    relations: Sequence[tuple[int, int, float]],
    seed: int,
) -> dict[str, Any]:
    expected = [float(item[2]) for item in relations]
    rng = np.random.default_rng(seed)
    shuffled = list(expected)
    rng.shuffle(shuffled)
    null_relations = tuple((i, j, value) for (i, j, _), value in zip(relations, shuffled, strict=True))
    return evaluate_geometry_candidate(
        profile,
        candidate_id=candidate_id,
        split=split,
        points=points,
        relations=null_relations,
        result_suffix="shuffled",
        extra_diagnostics={"null": "shuffled_labels"},
    )


def evaluate_product_ablation(
    profile: Mapping[str, Any],
    *,
    candidate_id: str,
    split: str,
    points,
    relations: Sequence[tuple[int, int, float]],
) -> tuple[dict[str, Any], ...]:
    candidate = _candidate(profile, candidate_id)
    if candidate["family"] != "PRODUCT_MANIFOLD":
        raise ValueError("component ablation applies only to PRODUCT_MANIFOLD candidates")
    dims = candidate.get("fit_config", {}).get("component_dims")
    if not isinstance(dims, list) or len(dims) < 2:
        raise ValueError("product ablation requires at least two component_dims")
    results = []
    for index in range(len(dims)):
        cloned = copy.deepcopy(dict(profile))
        for item in cloned["candidate_spaces"]:
            if item["candidate_id"] == candidate_id:
                item.setdefault("fit_config", {})["ablate_component"] = index
        results.append(
            evaluate_geometry_candidate(
                cloned,
                candidate_id=candidate_id,
                split=split,
                points=points,
                relations=relations,
                result_suffix=f"ablate-{index}",
                extra_diagnostics={"ablated_component": index},
            )
        )
    return tuple(results)


def _candidate(profile: Mapping[str, Any], candidate_id: str) -> dict[str, Any]:
    for candidate in profile["candidate_spaces"]:
        if candidate["candidate_id"] == candidate_id:
            return dict(candidate)
    raise ValueError(f"unknown candidate: {candidate_id}")


def _points(values, dimension: int) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] < 2 or matrix.shape[1] != dimension:
        raise ValueError("points must be a 2D matrix matching candidate dimension")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("points contain non-finite values")
    return matrix


def _geodesic_distortion(
    candidate: Mapping[str, Any],
    points: np.ndarray,
    relations: Sequence[tuple[int, int, float]],
) -> float:
    if not relations:
        raise ValueError("registered relations are required")
    if candidate["family"] == "TOPOLOGICAL":
        return _topological_distortion(candidate, points, relations)
    errors = []
    for i, j, expected in relations:
        measured = _geodesic(candidate, points[i], points[j])
        errors.append(abs(measured - float(expected)))
    return float(np.mean(errors))


def _geodesic(candidate: Mapping[str, Any], a: np.ndarray, b: np.ndarray) -> float:
    family = candidate["family"]
    if family == "EUCLIDEAN":
        return float(np.linalg.norm(a - b))
    if family == "HYPERBOLIC":
        return _poincare_distance(a, b)
    if family == "SPHERICAL":
        return _spherical_distance(a, b)
    if family == "PRODUCT_MANIFOLD":
        return _product_distance(candidate, a, b)
    raise ValueError(f"geometry family is NOT_COMPUTABLE in this slice: {family}")


def _poincare_distance(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.dot(a, a))
    nb = float(np.dot(b, b))
    if na >= 1.0 - _EPS or nb >= 1.0 - _EPS:
        raise ValueError("hyperbolic point lies on or outside the Poincaré ball")
    numerator = float(np.linalg.norm(a - b) ** 2)
    denom = (1.0 - na) * (1.0 - nb)
    arg = 1.0 + 2.0 * numerator / max(denom, _EPS)
    if arg < 1.0:
        arg = 1.0
    return float(np.arccosh(arg))


def _product_distance(candidate: Mapping[str, Any], a: np.ndarray, b: np.ndarray) -> float:
    dims = candidate.get("fit_config", {}).get("component_dims")
    if not isinstance(dims, list) or not dims or sum(int(d) for d in dims) != a.size:
        raise ValueError("product manifold requires component_dims that sum to candidate dimension")
    ablate = candidate.get("fit_config", {}).get("ablate_component")
    offset = 0
    squares = 0.0
    for index, dim in enumerate(dims):
        width = int(dim)
        if ablate != index:
            squares += float(np.linalg.norm(a[offset : offset + width] - b[offset : offset + width]) ** 2)
        offset += width
    return float(np.sqrt(squares))


def _topological_distortion(
    candidate: Mapping[str, Any],
    points: np.ndarray,
    relations: Sequence[tuple[int, int, float]],
) -> float:
    max_scale = candidate.get("fit_config", {}).get("max_scale")
    if max_scale is None:
        raise ValueError("topological candidate requires fit_config.max_scale filtration")
    n = points.shape[0]
    if n < 3:
        raise ValueError("topological metric requires at least 3 samples")
    unreachable = 1e18
    dist = np.full((n, n), unreachable)
    np.fill_diagonal(dist, 0.0)
    limit = float(max_scale)
    for i in range(n):
        for j in range(i + 1, n):
            edge = float(np.linalg.norm(points[i] - points[j]))
            if edge <= limit + _EPS:
                dist[i, j] = dist[j, i] = edge
    for k in range(n):
        for i in range(n):
            for j in range(n):
                alt = dist[i, k] + dist[k, j]
                if alt < dist[i, j]:
                    dist[i, j] = alt
    errors = []
    for i, j, expected in relations:
        if dist[i, j] >= unreachable / 2:
            raise ValueError("topological graph is disconnected at this filtration")
        errors.append(abs(float(dist[i, j]) - float(expected)))
    return float(np.mean(errors))


def _spherical_distance(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na < _EPS or nb < _EPS:
        raise ValueError("spherical points cannot be the origin")
    cosine = float(np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0))
    return float(np.arccos(cosine))
