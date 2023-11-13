"""Optimiser.

This module contains the abstract template and concrete
implementations of different optimisers used in the
application. Optimiser is a tool that can record the best
value for all slices so far and automatically update it
once the new optimal value is received.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations
import abc
import operator
import typing


class OptimiserABC(abc.ABC):
    """Template of optimisers.

    A template of objects that can record the best value for
    all slices so far and automatically update it once the
    new optimal value is received.
    """
    
    @abc.abstractmethod
    def _construct_candidate_optimal_map(
        self, slice_id_sequence: tuple[str, ...]) -> dict[str, float]:
        pass

    @abc.abstractmethod
    def _construct_comparator(self) -> typing.Callable:
        pass

    def __init__(self, slice_id_sequence: tuple[str, ...]) -> None:
        self._candidate_optimal_map = self._construct_candidate_optimal_map(
            slice_id_sequence)
        self._comparator = self._construct_comparator()

    def is_optimal(self, slice_id: str, candidate: float):
        if self._comparator(candidate, self._candidate_optimal_map[slice_id]):
            self._candidate_optimal_map[slice_id] = candidate
            return True
        else:
            return False


class MaximumOptimiser(OptimiserABC):
    """Optimiser to optimise the maximum value.

    An object that can record the maximum value for all
    slices so far and automatically update it once the new
    maximum is received.
    """

    def _construct_candidate_optimal_map(
        self, slice_id_sequence: tuple[str, ...]) -> dict[str, float]:
        return {slice_id:float('-inf') for slice_id in slice_id_sequence}
    
    def _construct_comparator(self) -> typing.Callable:
        return operator.gt
    
class MinimumOptimiser(OptimiserABC):
    """Optimiser to optimise the minimum value.

    An object that can record the minimum value for all
    slices so far and automatically update it once the new
    minimum is received.
    """

    def _construct_candidate_optimal_map(
        self, slice_id_sequence: tuple[str, ...]) -> dict[str, float]:
        return {slice_id:float('inf') for slice_id in slice_id_sequence}
    
    def _construct_comparator(self) -> typing.Callable:
        return operator.lt