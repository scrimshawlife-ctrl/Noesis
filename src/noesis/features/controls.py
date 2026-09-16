from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class ControlReport:
    feature_index: int
    decision: str
    reason: str
    mean_trigger: float
    mean_semantic: float
    mean_negative: float


def _mean_feature(activations, feature_index: int) -> float:
    matrix = np.asarray(activations, dtype=np.float64)
    if matrix.ndim != 2 or matrix.size == 0:
        raise ValueError("expected a non-empty 2D activation matrix")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("activations contain non-finite values")
    if not 0 <= feature_index < matrix.shape[1]:
        raise ValueError("feature_index is out of range")
    return float(matrix[:, feature_index].mean())


def evaluate_feature_controls(
    *,
    feature_index: int,
    trigger_activations,
    semantic_positive_activations,
    negative_activations,
    margin: float = 0.25,
) -> ControlReport:
    mean_trigger = _mean_feature(trigger_activations, feature_index)
    mean_semantic = _mean_feature(semantic_positive_activations, feature_index)
    mean_negative = _mean_feature(negative_activations, feature_index)

    if mean_negative >= mean_semantic and mean_negative >= mean_trigger:
        decision = "REJECTED"
        reason = "negative/confound activations are at least as strong as hypothesized positives"
    elif mean_trigger >= mean_semantic + margin:
        decision = "WEAKENED"
        reason = "lexical trigger activates without matching semantic-positive activation"
    else:
        decision = "SURVIVES"
        reason = "controls did not reject the candidate; description remains a hypothesis"

    return ControlReport(
        feature_index=feature_index,
        decision=decision,
        reason=reason,
        mean_trigger=mean_trigger,
        mean_semantic=mean_semantic,
        mean_negative=mean_negative,
    )
