"""Record.

This module contains all data records used in the
application. A data record is a very specific dict that
defines the format of data for specific usages. These ensure
objects can communicate with each other in a standard way.

Created by: Weixun Luo
Date: 22/03/2023
"""
from __future__ import annotations
import typing

import numpy as np

from object import transformation


# ----- Configuration -----
class Configuration(typing.TypedDict):
    """Configuration used to start up the application."""
    dataset_directory_path: str
    directory_name: dict[str, str]
    file_name: dict[str, str]
    pattern: dict[str, str]
    tag: dict[str, str]


# ----- Event -----
class KeyboardEvent(typing.TypedDict):
    """Event caught when users press keyboards."""
    key: str
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool
    repeat: bool


# ----- Initialiser -----
class DataAccessorInitialiser(typing.TypedDict):
    """Data required to initialise Data Accessor."""
    case_id: str
    body_file_path: str
    organ_file_path: str
    organ_resampled_file_path_map: dict[str, str]
    slice_file_path_map: dict[str, str]
    slice_mask_file_path_map: dict[str, str]
    transformation_spreadsheet_file_path: str

class EvaluationProcessingUnitInitialiser(typing.TypedDict):
    """Data required to initialise Evaluation Processing Unit."""
    evaluation_metric_name_sequence: tuple[str, ...]
    slice_id_sequence: tuple[str, ...]

class EvaluatorInitialiser(typing.TypedDict):
    """Data required to initialise Evaluator."""
    evaluation_metric_name: str
    slice_id_sequence: tuple[str, ...]

class ResamplerInitialiser(typing.TypedDict):
    """Data required to initialise Resampler."""
    plain_size: tuple[int, int]
    grid_pixel_data: np.ndarray
    grid_affine: np.ndarray

class ResamplingProcessingUnitInitialiser(typing.TypedDict):
    """Data required to initialise Resampling Processing Unit."""
    body_resampler_initialiser: ResamplerInitialiser
    organ_resampler_initialiser: ResamplerInitialiser

class TransformationProcessingUnitInitialiser(typing.TypedDict):
    """Data required to initialise Transformation Processing Unit."""
    transformation_map: dict[str, transformation.TransformationABC]

class VisualisationProcessingUnitInitialiser(typing.TypedDict):
    """Data required to initialise Visualisation Processing Unit."""
    body_pixel_data: np.ndarray
    organ_pixel_data: np.ndarray
    slice_pixel_data: np.ndarray


# ----- Property -----
class Body3DProperty(typing.TypedDict):
    """Visual properties of 3D body images."""
    visibility: int

class BodyResampled2DProperty(typing.TypedDict):
    """Visual properties of 2D resampled body images."""
    window_level: int
    window_width: int
    opacity: float

class CameraProperty(typing.TypedDict):
    """Visual properties of the camera used in dash-vtk."""
    position: tuple[int, int, int]
    view_up: tuple[int, int, int]

class CheckerboardProperty(typing.TypedDict):
    """Visual properties of checkerboard plots."""
    board_width: int

class ContourProperty(typing.TypedDict):
    """Visual properties of contour plots."""
    line_width: int

class Organ3DProperty(typing.TypedDict):
    """Visual properties of 3D organ labels."""
    colorDataRange: tuple[int, int]
    colorMapPreset: str
    visibility: int

class OrganResampled2DProperty(typing.TypedDict):
    """Visual properties of 2D resampled organ images."""
    threshold: float
    opacity: float

class Slice2DProperty(typing.TypedDict):
    """Visual properties of 2D slices."""
    window_level: int
    window_width: int
    opacity: float
    visibility: int


# ----- State -----
class State(typing.TypedDict):
    """Data required to render the 3D object by dash-vtk."""
    image: Image
    field: Field

class Image(typing.TypedDict):
    """Structural information of images in dash-vtk."""
    dimensions: tuple[int, ...]
    spacing: tuple[float, float, float]
    direction: tuple[float, ...]
    origin: tuple[float, float, float]

class Field(typing.TypedDict):
    """Pixel data representation of images in dash-vtk."""
    name: str
    numberOfComponents: int
    dataRange: tuple[float, float]
    type: str
    values: dict | list