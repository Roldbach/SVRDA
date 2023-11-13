"""Utils for processing images.

This module contains utility functions that facilitate
processing images at runtime.

Created by: Weixun Luo
Date: 05/04/2023
"""
from __future__ import annotations
import base64
import io
import typing

from PIL import Image
import cv2
import numpy as np
import orjson

from utils import format_utils
from utils import matrix_utils


PERCENTILE_RANGE = (2.5, 97.5)
PILLOW_IMAGE_MODE_MAP = {'grayscale':'L', 'rgba':'RGBA'}


def auto_contrast(
    pixel_data: np.ndarray,
    percentile_range: tuple[float, float] = PERCENTILE_RANGE,
) -> tuple[float, float]:
    return (
        np.percentile(pixel_data, percentile_range[0]),
        np.percentile(pixel_data, percentile_range[1]),
    )

def binarise(
    pixel_data: np.ndarray,
    threshold: int | float = 0,
    activation: int | float = 1,
) -> np.ndarray:
    return matrix_utils.cast(
        matrix = (pixel_data>threshold) * activation,
        data_type = _select_binarise_data_type(activation),
    )

def _select_binarise_data_type(activation: int | float) -> type:
    match activation:
        case int() if -128 <= activation and activation < 0:
            return np.int8
        case int() if 0 <= activation and activation <= 255:
            return np.uint8
        case float():
            return np.float32
        case _:
            raise ValueError(f'Unsupported activation: {activation}')

def compute_centroid(
    size: tuple[int, int, int], affine: np.ndarray,
) -> tuple[float, float, float]:
    centroid_image_index = _build_centroid_image_index(size)
    centroid_coordinate = affine @ centroid_image_index
    centroid = format_utils.convert_coordinate_to_array_index(
        centroid_coordinate)
    return centroid

def _build_centroid_image_index(size: tuple[int, int, int]) -> np.ndarray:
    return format_utils.convert_array_index_to_image_index(
        tuple(_/2 for _ in size)
    )

def correct_plotting_orientation(pixel_data: np.ndarray) -> np.ndarray:
    if _require_correct_plotting_orientation(pixel_data.shape):
        return np.rot90(pixel_data)
    else:
        return pixel_data

def _require_correct_plotting_orientation(size: tuple[int, ...]) -> bool:
    return len(size)==2 and size[0]>size[1]

def discretise(pixel_data: np.ndarray) -> np.ndarray:
    return matrix_utils.cast(
        pixel_data, _select_discretise_data_type(range(pixel_data)),
    )

def _select_discretise_data_type(range: tuple[float, float]) -> type:
    match range:
        case (min, max) if min < 0:
            return np.int16
        case (min, max) if 0 <= min and max <= 255:
            return np.uint8
        case (min, max) if 0 <= min and 255 < max:
            return np.uint16
        case _:
            raise ValueError(f'Unsupported range: {range}')

def look_up(pixel_data: np.ndarray, lookup_table: np.ndarray) -> np.ndarray:
    return cv2.LUT(pixel_data, lookup_table)

def mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    masker = _select_masker(len(mask.shape))
    output = masker(image, mask)
    return output

def _select_masker(dimension: int) -> typing.Callable:
    match dimension:
        case 2:
            return _mask_2d
        case _:
            raise ValueError(f'Unsupported dimension: {dimension}')

def _mask_2d(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return cv2.bitwise_and(src1=image, src2=image, mask=mask)

def range(pixel_data: np.ndarray) -> tuple[float, float]:
    return (np.amin(pixel_data), np.amax(pixel_data))

def serialise_to_array(pixel_data: np.ndarray) -> str:
    pixel_data = np.ascontiguousarray(pixel_data)
    encoding = orjson.dumps(pixel_data, option=orjson.OPT_SERIALIZE_NUMPY)
    decoding = encoding.decode()
    return decoding

def serialise_to_png(pixel_data: np.ndarray, pillow_image_mode: str) -> str:
    image = Image.fromarray(pixel_data, pillow_image_mode)
    decoding = _extract_png_decoding(image)
    decoding = _add_prefix(decoding)
    return decoding

def _extract_png_decoding(image: Image) -> str:
    with io.BytesIO() as stream:
        image.save(stream, format="png")
        encoding = base64.b64encode(stream.getvalue())
    decoding = encoding.decode()
    return decoding

def _add_prefix(png_decoding: str) -> str:
    return f'data:image/png;base64,{png_decoding}'

def quantise(pixel_data: np.ndarray, range: tuple[float, float]) -> np.ndarray:
    pixel_data = pixel_data.clip(*range)
    pixel_data = (pixel_data-range[0]) / (range[1]-range[0]) * 255
    pixel_data = matrix_utils.cast(pixel_data, np.uint8)
    return pixel_data