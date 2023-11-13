"""Utils for reading/writing files.

This module contains utility functions that can facilitate
reading/writing files at runtime.

Created by: Weixun Luo
Date: 21/03/2023
"""
from __future__ import annotations
import base64
import functools
import typing

import itk
import nibabel
import numpy as np
import orjson
import pandas as pd
from plotly import graph_objects
from vtkmodules.util import numpy_support

from object import record
from utils import image_processing_utils
from utils import path_utils


JSON_DATA_TYPE_MAP = {
    np.dtype(np.int8): 'Int8Array',
    np.dtype(np.int16): 'Int16Array',
    np.dtype(np.float32): 'Float32Array',
    np.dtype(np.float64): 'Float64Array',
    np.dtype(np.uint8): 'Uint8Array',
    np.dtype(np.uint16): 'Uint16Array',
}

ReadableContent: typing.TypeAlias = pd.DataFrame | dict | np.ndarray


# ----- File Reading -----
def read_file(file_path: str) -> ReadableContent:
    file_reader = _select_file_reader(
        path_utils.extract_file_extension(file_path))
    content = file_reader(file_path)
    return content

def _select_file_reader(file_extension: str) -> typing.Callable:
    match file_extension:
        case '.csv':
            return _read_csv_file
        case '.json':
            return _read_json_file
        case '.npy':
            return _read_npy_file
        case _:
            raise ValueError(f'Unsupported file extension: {file_extension}')

def _read_csv_file(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def _read_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        content = file.read()
    content = orjson.loads(content)
    return content

def _read_npy_file(file_path: str) -> np.ndarray:
    return np.load(file_path)

def read_pixel_data(file_path: str) -> np.ndarray:
    pixel_data_reader = _select_pixel_data_reader(
        path_utils.extract_file_extension(file_path))
    pixel_data = pixel_data_reader(file_path)
    return pixel_data
    
def _select_pixel_data_reader(file_extension: str) -> typing.Callable:
    match file_extension:
        case '.nii' | '.nii.gz':
            return _read_nii_pixel_data
        case _:
            raise ValueError(f'Unsupported file extension: {file_extension}')

def _read_nii_pixel_data(file_path: str) -> np.ndarray:
    image = nibabel.load(file_path)
    pixel_data = np.asanyarray(image.dataobj)
    return pixel_data

def read_affine(file_path: str) -> np.ndarray:
    affine_reader = _select_affine_reader(
        path_utils.extract_file_extension(file_path))
    affine = affine_reader(file_path)
    return affine
    
def _select_affine_reader(file_extension: str) -> typing.Callable:
    match file_extension:
        case '.nii' | '.nii.gz':
            return _read_nii_affine
        case _:
            raise ValueError(f'Unsupported file extension: {file_extension}')

def _read_nii_affine(file_path: str) -> np.ndarray:
    image = nibabel.load(file_path)
    affine = image.affine
    return affine

def read_field(file_path: str) -> record.Field:
    def _read_pixel_data(file_path: str) -> np.ndarray:
        """Reads the pixel data from the given file.
        
        Reads and returns the pixel data from the given file
        by using ITK and VTK. This function is referenced
        from the dash-vtk demo and should only be used in
        reading field.
        """
        image_itk = itk.imread(file_path)
        image_vtk = itk.vtk_image_from_image(image_itk)
        pixel_data = numpy_support.vtk_to_numpy(
            image_vtk.GetPointData().GetScalars())
        return pixel_data

    def _encode(array: np.ndarray) -> dict | list:
        """Encodes the array using base64.

        Encodes the given array using base64 and returns the
        object that could be further used in dash-vtk. This
        function is referenced from the dash-vtk demo and
        should only be used in reading field.
        """
        if len(array) == 0:
            return array.tolist()

        dtype = array.dtype
        if (
            dtype.kind in ["u", "i", "f"]
            and str(dtype) != "int64"
            and str(dtype) != "uint64"
        ):
            buffer = base64.b64encode(memoryview(array.ravel(order="C"))).decode("utf-8")
            return {"bvals": buffer, "dtype": str(dtype), "shape": array.shape}
        else:
            buffer = None
            dtype_str = None
            max_value = np.amax(array)
            min_value = np.amin(array)
            signed = min_value < 0
            test_value = max(max_value, -min_value)
            if test_value < np.iinfo(np.int16).max and signed:
                dtype_str = 'int16'
                buffer = base64.b64encode(memoryview(array.astype(np.int16).ravel(order="C"))).decode("utf-8")
            elif test_value < np.iinfo(np.int32).max and signed:
                dtype_str = 'int32'
                buffer = base64.b64encode(memoryview(array.astype(np.int32).ravel(order="C"))).decode("utf-8")
            elif test_value < np.iinfo(np.uint16).max and not signed:
                dtype_str = 'uint16'
                buffer = base64.b64encode(memoryview(array.astype(np.uint16).ravel(order="C"))).decode("utf-8")
            elif test_value < np.iinfo(np.uint32).max and not signed:
                dtype_str = 'uint32'
                buffer = base64.b64encode(memoryview(array.astype(np.uint32).ravel(order="C"))).decode("utf-8")

            if dtype:
                return {"bvals": buffer, "dtype": dtype_str, "shape": array.shape}

        return array.tolist()

    pixel_data = _read_pixel_data(file_path)
    field = record.Field(
        name = 'Scalars',
        numberOfComponents = 1,
        dataRange = image_processing_utils.range(pixel_data),
        type = JSON_DATA_TYPE_MAP[pixel_data.dtype],
        values = _encode(pixel_data),
    )
    return field


# ----- File Writing -----
@functools.singledispatch
def write_file(_: object, file_path: str) -> None:
    raise TypeError(f'Unsupported type: {type(_)}')

@write_file.register
def _(content: pd.DataFrame, file_path: str) -> None:
    content.to_csv(file_path, index=False)

@write_file.register
def _(content: dict, file_path: str) -> None:
    with open(file_path, 'w') as file:
        file.write(orjson.dumps(content).decode())

@write_file.register
def _(content: np.ndarray, file_path: str) -> None:
    np.save(file_path, content)

@write_file.register
def _(content: graph_objects.Figure, file_path: str) -> None:
    content.write_image(file_path)

def write_image(
    pixel_data: np.ndarray, affine: np.ndarray, file_path: str) -> None:
    image_writer = _select_image_writer(
        path_utils.extract_file_extension(file_path))
    image_writer(pixel_data, affine, file_path)

def _select_image_writer(file_extension: str) -> typing.Callable:
    match file_extension:
        case '.nii' | '.nii.gz':
            return _write_nii_image
        case '_':
            raise ValueError(f'Unsupported file extension: {file_extension}')

def _write_nii_image(
    pixel_data: np.ndarray, affine: np.ndarray, file_path: str) -> None:
    nibabel.save(nibabel.Nifti1Image(pixel_data, affine), file_path)