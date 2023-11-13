"""Plugins of Transformation Processing Unit.

This module contains the implementation of all plugins 
of Transformation Processing Unit, which contain algorithms
used to transform slices.

Created by: Weixun Luo
Date: 09/04/2023
"""
from __future__ import annotations

import numpy as np

from utils import affine_utils
from utils import matrix_utils
from utils import transformation_utils


class BasicAlgorithmPlugin:
    """Basic Algorithm Plugin.
    
    A plugin of Transformation Processing Unit, which
    contains algorithms for basic transformations including 
    translation and rotation.
    """

    def translate(
        self,
        transformation_matrix: np.ndarray,
        axis: tuple[float, float, float],
        step_size: float,
    ) -> np.ndarray:
        transformation_matrix[:3, 3] += step_size * np.array(axis)
        return transformation_matrix
    
    def rotate(
        self,
        affine_current: np.ndarray, 
        affine_original: np.ndarray,
        centre: tuple[float, float, float],
        axis: tuple[float, float, float],
        step_size: float,
    ) -> np.ndarray:
        rodrigues_matrix = transformation_utils.build_rodrigues_matrix(
            axis, step_size)
        affine_rotated = self._build_affine_rotated(
            rodrigues_matrix, affine_current, centre)
        output = affine_rotated @ np.linalg.inv(affine_original)
        return output
    
    def _build_affine_rotated(
        self,
        rodrigues_matrix: np.ndarray,
        affine_current: np.ndarray,
        centre: tuple[float, float, float],
    ) -> np.ndarray:
        affine_rotated = matrix_utils.build_identity()
        affine_rotated[:3, :3] = self._build_direction_matrix_rotated(
            rodrigues_matrix, affine_current)
        affine_rotated[:3, 3] = self._build_origin_rotated(
            rodrigues_matrix, affine_current, centre)
        return affine_rotated
    
    def _build_direction_matrix_rotated(
        self, rodrigues_matrix: np.ndarray, affine_current: np.ndarray,
    ) -> np.ndarray:
        return rodrigues_matrix @ affine_current[:3, :3]
    
    def _build_origin_rotated(
        self,
        rodrigues_matrix: np.ndarray,
        affine_current: np.ndarray,
        centre: tuple[float, float, float],
    ) -> tuple[float, float, float]:
        origin_current = affine_utils.extract_origin(affine_current)
        centre_to_origin_current = np.subtract(origin_current, centre)
        centre_to_origin_rotated = rodrigues_matrix @ centre_to_origin_current
        origin_rotated = np.add(centre_to_origin_rotated, centre)
        return origin_rotated