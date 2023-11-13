"""Transformation Processing Unit.

This module contains the implementation of Transformation
Processing Unit used in the application. It is a sub-
component of AppFactory, which can handle all operations
related to the transformation of slices. It can also manage
the transformation history for all slices.

Created by: Weixun Luo
Date: 09/04/2023
"""
from __future__ import annotations
import typing

import numpy as np

from business_layer import transformation_processing_unit_plugin
from object import record
from object import transformation


Initialiser: typing.TypeAlias = record.TransformationProcessingUnitInitialiser
Transformation: typing.TypeAlias = transformation.TransformationABC
TransformationData: typing.TypeAlias = np.ndarray | tuple[float, ...] | None


class TransformationProcessingUnit(
    transformation_processing_unit_plugin.BasicAlgorithmPlugin,
):
    """Transformation Processing Unit.
    
    A sub-component of AppFactory, which can handle all
    operations related to the transformation of slices. It
    can also manage the transformation history for all
    slices.
    """

    def __init__(self) -> None:
        self._transformation_type = None
        self._history_map = None
        self._pointer_current_map = None
        self._pointer_optimal_map = None
    
    def set_up(self, initialiser: Initialiser) -> None:
        self._transformation_type = self._construct_transformation_type(
            initialiser)
        self._history_map = self._construct_history_map(initialiser)
        self._pointer_current_map = self._construct_pointer_current_map(
            initialiser)
        self._pointer_optimal_map = self._construct_pointer_optimal_map(
            initialiser)
    
    def _construct_transformation_type(
        self, initialiser: Initialiser) -> transformation.TransformationABC:
        transformation = next(iter(initialiser['transformation_map'].values()))
        return type(transformation)
    
    def _construct_history_map(
        self, initialiser: Initialiser) -> dict[str, list[Transformation]]:
        return {
            slice_id: [transformation]
            for slice_id, transformation
            in initialiser['transformation_map'].items()
        }
    
    def _construct_pointer_current_map(
        self, initialiser: Initialiser) -> dict[str, int]:
        return {slice_id: 0 for slice_id in initialiser['transformation_map']}

    def _construct_pointer_optimal_map(
        self, initialiser: Initialiser) -> dict[str, int]:
        return {slice_id: 0 for slice_id in initialiser['transformation_map']}
    
    def get_transformation(self, slice_id: str) -> Transformation:
        return self._history_map[slice_id][self._pointer_current_map[slice_id]]
    
    def insert_transformation(
        self, slice_id: str, data: TransformationData) -> None:
        self._pointer_current_map[slice_id] += 1
        self._history_map[slice_id].insert(
            self._pointer_current_map[slice_id],
            self._transformation_type(data),
        )

    def undo_transformation(self, slice_id: str) -> None:
        if self._pointer_current_map[slice_id] > 0:
            self._pointer_current_map[slice_id] -= 1
        else:
            raise IndexError('Cannot access elements with indices less than 0')
    
    def redo_transformation(self, slice_id: str) -> None:
        if self._pointer_current_map[slice_id] +1 < len(self._history_map[slice_id]):
            self._pointer_current_map[slice_id] += 1
        else:
            raise IndexError(
                'Cannot access elements with indices equal to the length')
    
    def optimise_transformation(self, slice_id: str) -> None:
        transformation_optimal = self._history_map[slice_id][self._pointer_optimal_map[slice_id]]
        self.insert_transformation(slice_id, transformation_optimal.matrix)

    def reset_transformation(self, slice_id: str) -> None:
        self.insert_transformation(slice_id, None)

    def assign_optimal_transformation(self, slice_id: str) -> None:
        self._pointer_optimal_map[slice_id] = self._pointer_current_map[slice_id]