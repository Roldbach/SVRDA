"""Abtract classes for images.

This module contains all templates that define different
types of images used in the application.

Created by: Weixun Luo
Date: 04/04/2023
"""
from __future__ import annotations
import abc

import numpy as np

from object import record
from utils import affine_utils
from utils import image_processing_utils
from utils import io_utils
from utils import matrix_utils


class ImageABC(abc.ABC):
    """Template of images.

    A template of data structure that defines the
    representation of images in the application.
    """

    @abc.abstractmethod
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def _construct_pixel_data(self) -> np.ndarray:
        pass

    @property
    def pixel_data(self) -> np.ndarray:
        return self._get_pixel_data_by_property()
    
    def _get_pixel_data_by_property(self) -> np.ndarray:
        return np.array(self._pixel_data)

class ReadableImageABC(ImageABC):
    """Template of readable images.

    A template of data structure that defines the
    representation of readable images in the application.
    Pixel data is constructed by loading from the given
    image file and applying pre-processing to it.
    """

    @abc.abstractmethod
    def _process(self, pixel_data: np.ndarray) -> np.ndarray:
        pass

    def __init__(self, file_path: str) -> None:
        self._pixel_data = self._construct_pixel_data(file_path)
    
    def _construct_pixel_data(self, file_path: str) -> np.ndarray:
        pixel_data = io_utils.read_pixel_data(file_path)
        pixel_data = self._process(pixel_data)
        return pixel_data

class RenderableImageABC(ReadableImageABC):
    """Template of renderable images in dash-vtk.

    A template of data structure that defines the
    representation of renderable images in the application.
    Renderable images contain all required data and can be
    plotted in the 3D plot by dash-vtk.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._affine_original = self._construct_affine_original(file_path)
        self._field = self._construct_field(file_path)

    def _construct_affine_original(self, file_path: str) -> np.ndarray:
        return matrix_utils.cast(io_utils.read_affine(file_path))
    
    def _construct_field(self, file_path: str) -> record.Field:
        return io_utils.read_field(file_path)

    @property
    def affine_original(self) -> np.ndarray:
        return self._get_affine_original_by_property()
    
    def _get_affine_original_by_property(self) -> np.ndarray:
        return np.array(self._affine_original)
    
    @property
    def state(self) -> record.State:
        return self._get_state_by_property(self._affine_original)
    
    def _get_state_by_property(self, affine: np.ndarray) -> record.State:
        return record.State(
            image = record.Image(
                dimensions = self._pixel_data.shape,
                spacing = affine_utils.extract_spacing(affine),
                direction = affine_utils.extract_direction(affine),
                origin = affine_utils.extract_origin(affine),
            ),
            field = dict(self._field),
        )
    
class TransformableImageABC(RenderableImageABC):
    """Template of renderable images in dash-vtk.

    A template of data structure that defines the
    representation of renderable images in the application.
    Transformable images contain all required data and can
    be plotted in the 3D plot by dash-vtk. Alongside this,
    their states can be modified by transformation.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._affine_current = self._construct_affine_current(file_path)

    def _construct_affine_current(self, file_path: str) -> np.ndarray:
        return matrix_utils.cast(io_utils.read_affine(file_path))
    
    @property
    def state(self) -> record.State:
        return self._get_state_by_property(self._affine_current)

    @property
    def affine_current(self) -> np.ndarray:
        return self._get_affine_current_by_property()
    
    def _get_affine_current_by_property(self) -> np.ndarray:
        return np.array(self._affine_current)
    
    @property
    def centroid(self) -> tuple[float, float, float]:
        return self._get_centroid_by_property()
    
    def _get_centroid_by_property(self) -> tuple[float, float, float]:
        return image_processing_utils.compute_centroid(
            (*self._pixel_data.shape, 0), self.affine_current)

    def transform(self, transformation_matrix: np.ndarray) -> None:
        affine_current = transformation_matrix @ self._affine_original
        affine_current = matrix_utils.cast(affine_current)
        self._affine_current = affine_current
    
class MutableImageABC(ImageABC):
    """Template of mutable images.

    A template of data structure that defines the
    representation of mutable images in the application.
    Pixel data is mutable and shallow copy is applied to
    both getter and setter to ensure its encapsulation.
    """
    def __init__(self) -> None:
        self._pixel_data = self._construct_pixel_data()
    
    def _construct_pixel_data(self) -> None:
        return None

    @property
    def pixel_data(self) -> np.ndarray:
        return self._get_pixel_data_by_property()
    
    @pixel_data.setter
    def pixel_data(self, pixel_data: np.ndarray) -> None:
        self._set_pixel_data_by_property(pixel_data)
    
    def _set_pixel_data_by_property(self, pixel_data: np.ndarray) -> None:
        self._pixel_data = np.array(pixel_data)