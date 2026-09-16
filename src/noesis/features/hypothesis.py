from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FeatureHypothesis:
    dictionary_id: str
    feature_index: int
    description: str
    proposer: str
    canonical: bool = False


def hypothesis_from_description(
    *,
    dictionary_id: str,
    feature_index: int,
    description: str,
    proposer: str,
) -> FeatureHypothesis:
    if not description.strip():
        raise ValueError("feature description is required")
    if feature_index < 0:
        raise ValueError("feature_index must be >= 0")
    return FeatureHypothesis(
        dictionary_id=dictionary_id,
        feature_index=feature_index,
        description=description,
        proposer=proposer,
        canonical=False,
    )
