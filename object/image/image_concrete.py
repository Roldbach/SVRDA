"""Concrete classes for images.

This module contains all concrete implementations of
different types of images used in the application.
Data types have been carefully chosen to avoid waste of
resources.

Created by: Weixun Luo
Date: 05/04/2023
"""
from __future__ import annotations

import numpy as np

from object.image import image_abstract
from utils import image_processing_utils
from utils import matrix_utils


class SliceMask2D(
    image_abstract.ReadableImageABC,
    image_abstract.MutableImageABC,
):
    """A 2D mask defining the region of interest in a slice.

    A data structure that defines the representation of
    slice masks used in the application. Slice masks define
    the region of intrest within 2D slice. If no provided
    by users, only pixels with positive values are included. 
    """

    def _process(self, pixel_data: np.ndarray) -> np.ndarray:
        return image_processing_utils.binarise(np.nan_to_num(pixel_data))
        
class Body3D(image_abstract.RenderableImageABC):
    """A 3D image defining the patient's body.

    A data structure that defines the representation of 3D
    body images in the application. Body images are involved
    in the resampling and serve as the keystone of 2D/3D
    registration. 
    """

    def _process(self, pixel_data: np.ndarray) -> np.ndarray:
        pixel_data = np.nan_to_num(pixel_data)
        pixel_data = image_processing_utils.discretise(pixel_data)
        return pixel_data
    
class Organ3D(image_abstract.RenderableImageABC):
    """A 3D label defining the organ region in the body.

    A data structure that defines the representation of
    3D organ labels in the application. Organ labels
    highlight single/multiple organs in the body and serve
    as the keystone in the 2D/3D registration.
    """
    
    def _process(self, pixel_data: np.ndarray) -> np.ndarray:
        pixel_data = np.nan_to_num(pixel_data)
        pixel_data = matrix_utils.cast(pixel_data, np.uint8)
        return pixel_data
    
class Slice2D(image_abstract.TransformableImageABC):
    """A 2D image used as the fix image in the registration.

    A data structure that defines the representation of 2D
    slices in the application. 2D slices serve as the
    keystone of 2D/3D registration and transformation
    matrices can be applied to change their internal states.
    """

    def _process(self, pixel_data: np.ndarray) -> np.ndarray:
        pixel_data = np.nan_to_num(pixel_data)
        pixel_data = image_processing_utils.discretise(pixel_data)
        return pixel_data

class BodyResampled2D(image_abstract.MutableImageABC):
    """A 2D image obtained by resampling 3D body images.
    
    A data structure that defines the representation of
    body images after resampling onto a 2D plane. Resampled
    body images are often compared with the corresponding
    slices to evaluate the effect of registration.
    """

class OrganResampled2D(image_abstract.MutableImageABC):
    """A 2D image obtained by resampling 3D organ labels.

    A data structure that defines the representation of
    organ images after resampling onto a 2D plane. Futher
    processing is required before using it as a label/mask.
    """