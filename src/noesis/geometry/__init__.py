"""Geometry-profile registry and candidate metrics. No preferred geometry."""

from .engine import (
    evaluate_geometry_candidate,
    freeze_geometry_selection,
    select_geometry_candidate,
    validate_geometry_profile,
)

__all__ = [
    "evaluate_geometry_candidate",
    "freeze_geometry_selection",
    "select_geometry_candidate",
    "validate_geometry_profile",
]
