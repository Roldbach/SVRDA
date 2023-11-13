"""Evaluation Processing Unit.

This module contains the implementation of Evaluation
Processing Unit used in the application. It is a sub-
component of AppFactory, which can use various evaluation
metrics to evaluate the candidate and reference. It can
also determine whether the received result is the optimal
so far or not.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations
import typing

import numpy as np

from object import evaluator
from object import record


Initialiser: typing.TypeAlias = record.EvaluationProcessingUnitInitialiser


class EvaluationProcessingUnit:
    """Evaluation Processing Unit.

    A sub-component of AppFactory and can use various
    evaluation metrics to evaluate the candidate and 
    reference. It can also determine whether the received
    result is the optimal so far or not.
    """

    def __init__(self) -> None:
        self._evaluator_map = None
    
    def set_up(self, initialiser: Initialiser) -> None:
        self._evaluator_map = self._construct_evaluator_map(initialiser)
    
    def _construct_evaluator_map(
        self, initialiser: Initialiser) -> dict[str, evaluator.Evaluator]:
        return {
            evaluation_metric_name: evaluator.Evaluator(
                record.EvaluatorInitialiser(
                    evaluation_metric_name = evaluation_metric_name,
                    slice_id_sequence = initialiser['slice_id_sequence'],
                )
            )
            for evaluation_metric_name
            in initialiser['evaluation_metric_name_sequence']
        }
    
    def evaluate(
        self,
        slice_id: str,
        evaluation_metric_name: str,
        candidate: np.ndarray,
        reference: np.ndarray,
    ) -> tuple[float, bool]:
        return self._evaluator_map[evaluation_metric_name].evaluate(
            slice_id, candidate, reference)