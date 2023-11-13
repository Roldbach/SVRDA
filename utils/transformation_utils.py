"""Utils for processing transformation parameters/matrices.

This module contains utility functions that facilitate
processing transformation parameters/matrices at runtime.

Created by: Weixun Luo
Date: 06/04/2023
"""
from __future__ import annotations

import numpy as np

from utils import matrix_utils


# Modified from the NifTI coordinate system to fit extract_rotation_parameter()
SCANNER_COORDINATE_ROTATION_AXIS_SEQUENCE = (
    (-1.0, 0.0, 0.0),
    (0.0, -1.0, 0.0),
    (0.0, 0.0, -1.0),
)


def build_translation_matrix(
    translation_parameter: tuple[float, float, float]) -> np.ndarray:
    translation_matrix = matrix_utils.build_identity()
    translation_matrix[:3, 3] = translation_parameter
    return translation_matrix

def build_rotation_matrix(
    rotation_parameter: tuple[float, float, float]) -> np.ndarray:
    output = matrix_utils.build_identity(3)
    for axis, radian in zip(SCANNER_COORDINATE_ROTATION_AXIS_SEQUENCE, rotation_parameter):
        output = output @ build_rodrigues_matrix(axis, radian)
    output = _convert_rodrigues_matrix_to_rotation_matrix(output)
    return output

def build_rodrigues_matrix(
    axis: tuple[float, float, float], radian: float) -> np.ndarray:
    """Builds a rotation matrix using Rodrigues' formula.

    Builds a transformation matrix that represents a rotation
    about the central direction in 3D space using Rodrigues'
    formula. For more information please check:
    https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    """
    I = _build_rodrigues_I()
    K = _build_rodrigues_K(axis)
    return I + np.sin(radian)*K + (1-np.cos(radian))*matrix_utils.power(K, 2)

def _build_rodrigues_I() -> np.ndarray:
    return matrix_utils.build_identity(3)

def _build_rodrigues_K(axis: tuple[float, float, float]) -> np.ndarray:
    return matrix_utils.cast(
        np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
    )

def _convert_rodrigues_matrix_to_rotation_matrix(
    rodrigues_matrix: np.ndarray) -> np.ndarray:
    rotation_matrix = matrix_utils.build_identity()
    rotation_matrix[:3, :3] = rodrigues_matrix
    return rotation_matrix

def extract_translation_parameter(
    transformation_matrix: np.ndarray) -> tuple[float, float, float]:
    return tuple(transformation_matrix[:3, 3])

def extract_rotation_parameter(
    transformation_matrix: np.ndarray) -> tuple[float, float, float]:
    """Extracts rotation parameters from the given transformation matrix.

    Extracts and returns rotation parameters from the given
    transformation matrix. This function has been simplified
    and can only work with rigid transformation matrices.
    """
    column_0 = transformation_matrix[:3, 0]
    column_1 = transformation_matrix[:3, 1]
    column_2 = transformation_matrix[:3, 2]
    
    if np.dot(column_0, np.cross(column_1, column_2)) < 0:
        column_0 *= -1
        column_1 *= -1
        column_2 *= -1
        
    rotation_y = np.arcsin(-1 * column_2[0])

    if np.abs(np.cos(rotation_y)) > 0:
        rotation_x = np.arctan2(column_2[1], column_2[2])
        rotaiton_z = np.arctan2(column_1[0], column_0[0])
    else:
        rotation_x = np.arctan2(-column_2[0]*column_0[2], -column_2[0]*column_0[2])
        rotaiton_z = 0
    
    return (rotation_x, rotation_y, rotaiton_z)