"""Geometry-profile registry and candidate metrics. No preferred geometry."""

from .engine import (
    bootstrap_geodesic_uncertainty,
    evaluate_geometry_candidate,
    evaluate_knn_retention,
    evaluate_product_ablation,
    evaluate_projection_loss,
    evaluate_rank_preservation,
    evaluate_relation_prediction,
    freeze_geometry_selection,
    label_geometric_rupture,
    random_pair_null,
    select_geometry_candidate,
    shuffled_relation_null,
    validate_geometry_profile,
)

__all__ = [
    "bootstrap_geodesic_uncertainty",
    "evaluate_geometry_candidate",
    "evaluate_knn_retention",
    "evaluate_product_ablation",
    "evaluate_projection_loss",
    "evaluate_rank_preservation",
    "evaluate_relation_prediction",
    "freeze_geometry_selection",
    "label_geometric_rupture",
    "random_pair_null",
    "select_geometry_candidate",
    "shuffled_relation_null",
    "validate_geometry_profile",
]
