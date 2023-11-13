"""Transformation.

This module contains the abstract template and concrete
implementations of different transformations used in the
application. Transformation is a data structure that
defines a mapping between points in the domain and range.
Values are casted to float32 to avoid wasting resources
when the accuracy is constrained anyway.

Created by: Weixun Luo
Date: 06/04/2023
"""
from __future__ import annotations
import abc
import typing

import numpy as np

from utils import matrix_utils
from utils import transformation_utils


Data: typing.TypeAlias = np.ndarray | tuple[float, ...] | None


class TransformationABC(abc.ABC):
    """Template of transformations.

    A template of data structure that defines a mapping
    between points in the domain and range.
    """

    @abc.abstractmethod
    def _convert_matrix_to_parameter(
        self, matrix: np.ndarray) -> tuple[float, ...]:
        pass
    
    @abc.abstractmethod
    def _convert_parameter_to_matrix(
        self, parameter: tuple[float, ...]) -> np.ndarray:
        pass

    def __init__(self, data: Data = None) -> None:
        self._matrix = self._construct_matrix(data)
    
    def _construct_matrix(self, data: Data) -> np.ndarray:
        constructor = self._select_constructor(data)
        matrix = constructor(data)
        return matrix
    
    def _select_constructor(self, data: Data) -> typing.Callable:
        match data:
            case np.ndarray():
                return self._construct_matrix_by_matrix
            case tuple():
                return self._construct_matrix_by_parameter
            case None:
                return self._construct_matrix_by_none
            case _:
                raise TypeError(f'Unsupported data type: {type(data)}')
    
    def _construct_matrix_by_matrix(self, data: np.ndarray) -> np.ndarray:
        return matrix_utils.cast(np.array(data))
    
    def _construct_matrix_by_parameter(
        self, data: tuple[float, ...]) -> np.ndarray:
        return matrix_utils.cast(self._convert_parameter_to_matrix(data))
    
    def _construct_matrix_by_none(self, _: None) -> np.ndarray:
        return matrix_utils.build_identity()


    @property
    def matrix(self) -> np.ndarray:
        return self._get_matrix_by_property()
    
    def _get_matrix_by_property(self) -> np.ndarray:
        return np.array(self._matrix)
    
    @property
    def parameter(self) -> tuple[float, ...]:
        return self._get_parameter_by_property()
    
    def _get_parameter_by_property(self) -> tuple[float, ...]:
        return self._convert_matrix_to_parameter(self._matrix)
    

class RigidTransformation(TransformationABC):
    """An affine transformation with 6 degrees of freedom.

    A data structure that defines a linear mapping with 6
    degrees of freedom between points in the domain and
    range.
    """

    def _convert_matrix_to_parameter(
        self, matrix: np.ndarray) -> tuple[float, ...]:
        translation_parameter = transformation_utils.extract_translation_parameter(matrix)
        rotation_parameter = transformation_utils.extract_rotation_parameter(matrix)
        parameter = translation_parameter + rotation_parameter
        return parameter
    
    def _convert_parameter_to_matrix(
        self, parameter: tuple[float, ...]) -> np.ndarray:
        translation_matrix = transformation_utils.build_translation_matrix(
            parameter[:3])
        rotation_matrix = transformation_utils.build_rotation_matrix(
            parameter[3:6])
        matrix = translation_matrix @ rotation_matrix
        return matrix