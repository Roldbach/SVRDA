"""Utils for processing affine matrices.

This module contains utility functions that can facilitate
processing affine matrices at runtime. Affine matrix is a
4 by 4 transformation matrix that transforms image indices
to their corresponding physical coordinates.

Created by: Weixun Luo
Date: 21/03/2023
"""
from __future__ import annotations
import functools

import numpy as np

from utils import matrix_utils


DIRECTION_SLICE_MAP = {
    'x': slice(0, 3, 1),
    'y': slice(3, 6, 1),
    'z': slice(6, 9, 1),
}


@functools.singledispatch
def extract_axis(_: object, axis_name: str) -> tuple[float, float, float]:
    raise TypeError(f'Unsupported type: {type(_)}')

@extract_axis.register
def _(affine: np.ndarray, axis_name: str) -> tuple[float, float, float]:
    direction = extract_direction(affine)
    axis = direction[DIRECTION_SLICE_MAP[axis_name]]
    return axis

@extract_axis.register
def _(direction: tuple, axis_name: str) -> tuple[float, float, float]:
    return direction[DIRECTION_SLICE_MAP[axis_name]]

def extract_direction(affine: np.ndarray) -> tuple[float, ...]:
    direction = affine[:3, :3] / matrix_utils.norm_2_columnwise(affine[:3, :3])
    direction = tuple(direction.T.flatten())
    return direction

def extract_origin(affine: np.ndarray) -> tuple[float, float, float]:
    return tuple(affine[:3, 3])

def extract_spacing(affine: np.ndarray) -> tuple[float, float, float]:
    return tuple(matrix_utils.norm_2_columnwise(affine[:3, :3]))