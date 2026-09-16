"""Geometry-profile registry and candidate metrics. No preferred geometry."""

from .engine import (
    evaluate_geometry_candidate,
    evaluate_knn_retention,
    evaluate_product_ablation,
    evaluate_rank_preservation,
    freeze_geometry_selection,
    select_geometry_candidate,
    shuffled_relation_null,
    validate_geometry_profile,
)

__all__ = [
    "evaluate_geometry_candidate",
    "evaluate_knn_retention",
    "evaluate_product_ablation",
    "evaluate_rank_preservation",
    "freeze_geometry_selection",
    "select_geometry_candidate",
    "shuffled_relation_null",
    "validate_geometry_profile",
]
