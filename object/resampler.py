"""Resampler.

This module contains the abstract template and concrete
implementations of different resamplers used in the
application. Resampler is a tool that can resample 3D pixel
data onto a 2D plane defined by the given affine matrix.

Created by: Weixun Luo
Date: 06/04/2023
"""
from __future__ import annotations
import abc

import numpy as np
from scipy import interpolate

from object import record


# Please check here for more interpolation methods:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RegularGridInterpolator.html#scipy.interpolate.RegularGridInterpolator
BODY_INTERPOLATION_METHOD = 'linear'
SINGLE_ORGAN_INTERPOLATION_METHOD = 'linear'
MULTI_ORGAN_INTERPOLATION_METHOD = 'nearest'


class ResamplerABC(abc.ABC):
    """Template of resamplers.

    A template of object that can resample 3D pixel data
    onto the 2D plane defined by the given affine matrix.
    """

    @abc.abstractmethod
    def _select_interpolator_method(self, grid_pixel_data: np.ndarray) -> str:
        pass

    def __init__(self, initialiser: record.ResamplerInitialiser) -> None:
        self._plain_size = initialiser['plain_size']
        self._plain_index = self._construct_plain_index()
        self._grid_affine_inversed = self._construct_grid_affine_inversed(
            initialiser['grid_affine'])
        self._interpolator = self._construct_interpolator(
            initialiser['grid_pixel_data'])
    
    def _construct_plain_index(self) -> np.ndarray:
        # Plain index looks like
        # [
        #   [x_1, x_2, x_3, ...],
        #   [y_1, y_2, y_3, ...],
        #   [z_1, z_2, z_3, ...],
        #   [1, 1, 1, ...],
        # ]
        # where (x, y, z) are the index of points in the plain
        return np.column_stack(
            tuple(
                (x, y, 0, 1)
                for x in range(self._plain_size[0])
                for y in range(self._plain_size[1])
            )
        )
    
    def _construct_grid_affine_inversed(
        self, grid_affine: np.ndarray) -> np.ndarray:
        return np.linalg.inv(grid_affine)
    
    def _construct_interpolator(
        self, grid_pixel_data: np.ndarray,
    ) -> interpolate.RegularGridInterpolator:
        return interpolate.RegularGridInterpolator(
            points = self._build_grid_point(grid_pixel_data.shape),
            values = grid_pixel_data,
            method = self._select_interpolator_method(grid_pixel_data),
            bounds_error = False,
            fill_value = 0,
        )
    
    def _build_grid_point(
        self, grid_size: tuple[int, int, int],
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return tuple(
            np.linspace(start=0, stop=dimension, num=dimension, endpoint=False)
            for dimension in grid_size
        )
    
    def resample(self, plain_affine: np.ndarray) -> np.ndarray:
        plain_point = self._build_plain_point(plain_affine)
        plain_pixel_data = self._interpolator(plain_point)
        plain_pixel_data = np.reshape(plain_pixel_data, self._plain_size)
        return plain_pixel_data
    
    def _build_plain_point(self, plain_affine: np.ndarray) -> np.ndarray:
        grid_index = self._build_grid_index(plain_affine)
        plain_point = self._convert_grid_index_to_plain_point(grid_index)
        return plain_point
    
    def _build_grid_index(self, plain_affine: np.ndarray) -> np.ndarray:
        return self._grid_affine_inversed @ plain_affine @ self._plain_index
    
    def _convert_grid_index_to_plain_point(
        # Convert the grid index from
        # [
        #   [x_1, x_2, x_3, ...],
        #   [y_1, y_2, y_3, ...],
        #   [z_1, z_2, z_3, ...],
        #   [1, 1, 1, ...],
        # ]
        # to
        # [
        #   [x_1, y_1, z_1],
        #   [x_2, y_2, z_2],
        #   [x_3, y_3, z_3],
        #   ...
        # ]
        self, grid_index: np.ndarray) -> np.ndarray:
        plain_point = grid_index[:3, :]
        plain_point = np.transpose(plain_point)
        return plain_point


class Body3DResampler(ResamplerABC):
    """Resampler for 3D body images.

    An object that can resample 3D body image pixel data
    onto the 2D plane defined by the given affine matrix.
    """

    def _select_interpolator_method(self, grid_pixel_data: np.ndarray) -> str:
        return BODY_INTERPOLATION_METHOD

class Organ3DResampler(ResamplerABC):
    """Resampler for 3D organ labels.

    An object that can resample 3D organ label pixel data
    onto the 2D plane defined by the given affine matrix.
    """

    def _select_interpolator_method(self, grid_pixel_data: np.ndarray) -> str:
        if np.amax(grid_pixel_data) == 1:
            return SINGLE_ORGAN_INTERPOLATION_METHOD
        else:
            return MULTI_ORGAN_INTERPOLATION_METHOD