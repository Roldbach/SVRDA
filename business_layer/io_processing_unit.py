"""IO Processing Unit.

This module contains the implementation of IO Processing
Unit used in the application. It is a sub-component of
AppFactory, which can handle all IO-related operations.

Created by: Weixun Luo
Date: 06/05/2023
"""
from __future__ import annotations
import typing

import numpy as np
import pandas as pd

from object import transformation
from utils import io_utils


TRANSFORMATION_PARAMETER_COLUMN_SEQUENCE = (
    'translation_x', 'translation_y', 'translation_z',
    'rotation_x', 'rotation_y', 'rotation_z',
    'scale_x', 'scale_y', 'scale_z',
    'skew_x', 'skew_y', 'skew_z',
)

Transformation: typing.TypeAlias = transformation.TransformationABC


class IOProcessingUnit:
    """IO Processing Unit.

    A sub-component of AppFactory that can handle all IO-
    related operations.
    """

    def __init__(self) -> None:
        pass
    
    def write_transformation_spreadsheet(
        self,
        case_id: str,
        slice_id_sequence: tuple[str, ...],
        transformation_parameter_matrix: np.ndarray,
        file_path: str,
    ) -> None:
        io_utils.write_file(
            self._build_transformation_spreadsheet_content(
                case_id,
                slice_id_sequence,
                transformation_parameter_matrix,
            ),
            file_path,
        )
    
    def _build_transformation_spreadsheet_content(
        self,
        case_id: str,
        slice_id_sequence: tuple[str, ...],
        transformation_parameter_matrix: np.ndarray,
    ) -> pd.DataFrame:
        """This function is compatible with affine transformations."""
        return pd.DataFrame(
            {
                'case_id': (case_id,) * len(slice_id_sequence),
                'slice_id': slice_id_sequence,
            } | {
                TRANSFORMATION_PARAMETER_COLUMN_SEQUENCE[i]:
                    tuple(transformation_parameter_matrix[:, i])
                for i in range(transformation_parameter_matrix.shape[1])
            }
        )
    
    def write_organ_resampled_map(
        self,
        pixel_data_map: dict[str, str],
        affine_map: dict[str, str],
        file_path_map: dict[str, str],
    ) -> None:
        for slice_id in file_path_map:
            io_utils.write_image(
                pixel_data_map[slice_id],
                affine_map[slice_id],
                file_path_map[slice_id],
            )