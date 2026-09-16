"""Sparse feature dictionary lab, probes, and control evaluation."""

from .controls import ControlReport, evaluate_feature_controls
from .dictionary import DictionaryRecord, fit_sparse_dictionary, run_dictionary_consistency
from .hypothesis import FeatureHypothesis, hypothesis_from_description
from .probe import LeakageReport, ProbeRecord, detect_probe_leakage, evaluate_probe, train_linear_probe

__all__ = [
    "ControlReport",
    "DictionaryRecord",
    "FeatureHypothesis",
    "LeakageReport",
    "ProbeRecord",
    "detect_probe_leakage",
    "evaluate_feature_controls",
    "evaluate_probe",
    "fit_sparse_dictionary",
    "hypothesis_from_description",
    "run_dictionary_consistency",
    "train_linear_probe",
]
