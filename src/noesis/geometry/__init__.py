"""Geometry-profile registry and candidate metrics. No preferred geometry."""

from .engine import (
    evaluate_geometry_candidate,
    evaluate_product_ablation,
    freeze_geometry_selection,
    select_geometry_candidate,
    shuffled_relation_null,
    validate_geometry_profile,
)

__all__ = [
    "evaluate_geometry_candidate",
    "evaluate_product_ablation",
    "freeze_geometry_selection",
    "select_geometry_candidate",
    "shuffled_relation_null",
    "validate_geometry_profile",
]
