"""Evaluator.

This module contains the concrete implementation of
Evaluator in the application. Evaluator is a tool that can
use the selected evaluation metric to evaluate the given
candidate and reference and determine whether it is the
optimal result so far.

Created: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations
import typing

import numpy as np

from object import evaluator_plugin
from object import optimiser
from object import record


Initialiser: typing.TypeAlias = record.EvaluatorInitialiser


class Evaluator(
    evaluator_plugin.MultiModalEvaluationMetricPlugin,
    evaluator_plugin.PixelwiseEvaluationMetricPlugin,
):
    """Evaluator.

    An object that can use the selected evaluation metric
    to evaluate the given candidate and reference and
    determine whether it is the optimal result so far.
    """

    def __init__(self, initialiser: Initialiser) -> None:
        self._evaluation_metric = self._construct_evaluation_metric(initialiser)
        self._optimiser = self._construct_optimiser(initialiser)
    
    def _construct_evaluation_metric(
        self, initialiser: Initialiser) -> typing.Callable:
        match initialiser['evaluation_metric_name']:
            case 'normalised_mutual_information' | 'NMI':
                return self._compute_normalised_mutual_information
            case 'sum_absolute_difference' | 'SAD':
                return self._compute_sum_absolute_difference
            case _:
                raise ValueError((
                    f'Unsupported evaluation metric: '
                    f'{initialiser["evaluation_metric_name"]}'
                ))
    
    def _construct_optimiser(
        self, initialiser: Initialiser) -> optimiser.OptimiserABC:
        match initialiser['evaluation_metric_name']:
            case 'normalised_mutual_information' | 'NMI':
                return optimiser.MaximumOptimiser(
                    initialiser['slice_id_sequence'])
            case 'sum_absolute_difference' | 'SAD':
                return optimiser.MinimumOptimiser(
                    initialiser['slice_id_sequence'])
            case _:
                raise ValueError((
                    f'Unsupported evaluation metric: '
                    f'{initialiser["evaluation_metric_name"]}'
                ))
    
    def evaluate(
        self, slice_id: str, candidate: np.ndarray, reference: np.ndarray,
    ) -> tuple[float, bool]:
        evaluation_output = self._evaluation_metric(candidate, reference)
        is_optimal = self._optimiser.is_optimal(slice_id, evaluation_output)
        return evaluation_output, is_optimal