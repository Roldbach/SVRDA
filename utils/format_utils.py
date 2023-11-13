"""Utils for formatting data.

This module contains utility functions that facilitate
formatting data at runtime. The following data formats are
used across the whole application:
    (1) array_index: A tuple[float, float, float] that
                     specifies the index of a pixel in the
                     array as (i, j, k)
    (2) image_index: A numpy.ndarray that specifies the
                     index of a pixel in the image as a
                     4 by 1 array (i, j, k, 1)
    (3) coordinate: A numpy.ndarray that specifies the
                    physical coordinate of a pixel as a
                    4 by 1 array (x, y, z, 1)
    (4) degree: A float that specifies the angle in degree
    (5) radian: A float that specifies the angle in radian
    (6) range: A tuple[float, float] that specifies the
               range of an image as (min, max)
    (7) window: A tuple[float, float] that specifies the
                range of an image as (level, width)
        level: A float that controls the brightness of an
               image, calculated by (min+max) / 2
        width: A float that controls the contrast of an
               image, calculated by max - min

Created by: Weixun Luo
Date: 10/04/2023
"""
from __future__ import annotations
import re

import numpy as np


NUMBER_FORMATTER = '{:.4f}'


def convert_array_index_to_image_index(
    array_index: tuple[float, float, float]) -> np.ndarray:
    return np.array((*array_index, 1)).reshape((4, 1))

def convert_coordinate_to_array_index(
    coordinate: np.ndarray) -> tuple[float, float, float]:
    return tuple(coordinate[:3].flatten())

def convert_degree_to_radian(degree: float) -> float:
    return np.deg2rad(degree)

def convert_range_to_window(range: tuple[float, float]) -> tuple[float, float]:
    return (
        (range[0]+range[1]) / 2,
        range[1] - range[0],
    )

def convert_window_to_range(window: tuple[int, int]) -> tuple[float, float]:
    return (
        window[0] - window[1]/2,
        window[0] + window[1]/2,
    )

def format_number(number: float) -> str:
    return NUMBER_FORMATTER.format(number)

def format_transformation_parameter(transformation_parameter: float) -> str:
    """This function can trim leading +/- in transformation parameters."""
    return re.sub (r"^-(0\.?0*)$", r"\1", format_number(transformation_parameter))