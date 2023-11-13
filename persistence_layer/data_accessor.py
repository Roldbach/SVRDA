"""Data Accessor.

This module contains the implementation of Data Accessor
used in the application. It contains data used for each case
and specifically designed interfaces, which offer efficient
and accurate data access to corresponding components in the
application.

Created by: Weixun Luo
Date: 08/04/2023
"""
from __future__ import annotations
import typing

import pandas as pd

from object import record
from object.image import image_concrete
from object import transformation
from persistence_layer import data_accessor_plugin
from utils import io_utils


TRANSFORMATION_TYPE = transformation.RigidTransformation

Initialiser: typing.TypeAlias = record.DataAccessorInitialiser


class DataAccessor(
    data_accessor_plugin.TransformationProcessingUnitPlugin,
    data_accessor_plugin.VisualisationProcessingUnitPlugin,
    data_accessor_plugin.ResamplingProcessingUnitPlugin,
    data_accessor_plugin.MaskingProcessingUnitPlugin,
    data_accessor_plugin.PlottingProcessingUnitPlugin,
    data_accessor_plugin.EvaluationProcessingUnitPlugin,
    data_accessor_plugin.IOProcessingUnitPlugin,
    data_accessor_plugin.AppFactoryPlugin,
):
    """Data Accessor.
    
    An object that contains data used for each case and
    specifically designed interfaces, which offer efficient
    and accurate data access to corresponding components in
    the application.
    """

    def __init__(self) -> None:
        self._case_id = None
        self._body = None
        self._body_resampled_map = None
        self._organ = None
        self._organ_resampled_map = None
        self._organ_resampled_file_path_map = None
        self._slice_map = None
        self._slice_mask_map = None
        self._transformation_map = None
        self._transformation_spreadsheet_file_path = None
    
    def set_up(self, initialiser: Initialiser) -> None:
        self._case_id = self._construct_case_id(initialiser)
        self._body = self._construct_body(initialiser)
        self._body_resampled_map = self._construct_body_resampled_map(
            initialiser)
        self._organ = self._construct_organ(initialiser)
        self._organ_resampled_map = self._construct_organ_resampled_map(
            initialiser)
        self._organ_resampled_file_path_map = self._construct_organ_resampled_file_path_map(
            initialiser)
        self._slice_map = self._construct_slice_map(initialiser)
        self._slice_mask_map = self._construct_slice_mask_map(initialiser)
        self._transformation_map = self._construct_transformation_map(
            initialiser) 
        self._transformation_spreadsheet_file_path = self._construct_transformation_spreadsheet_file_path(
            initialiser)

    def _construct_case_id(self, initialiser: Initialiser) -> str:
        return initialiser['case_id']
    
    def _construct_body(
        self, initialiser: Initialiser) -> image_concrete.Body3D:
        return image_concrete.Body3D(initialiser['body_file_path'])
    
    def _construct_body_resampled_map(
        self, initialiser: Initialiser) -> dict[str, image_concrete.BodyResampled2D]:
        return {
            slice_id: image_concrete.BodyResampled2D()
            for slice_id in initialiser['slice_file_path_map']
        }
    
    def _construct_organ(
        self, initialiser: Initialiser) -> image_concrete.Organ3D:
        return image_concrete.Organ3D(initialiser['organ_file_path'])
    
    def _construct_organ_resampled_map(
        self, initialiser: Initialiser,
    ) -> dict[str, image_concrete.OrganResampled2D]:
        return {
            slice_id: image_concrete.OrganResampled2D()
            for slice_id in initialiser['slice_file_path_map']
        }
    
    def _construct_organ_resampled_file_path_map(
        self, initialiser: Initialiser) -> dict[str, str]:
        return dict(initialiser['organ_resampled_file_path_map'])
    
    def _construct_slice_map(
        self, initialiser: Initialiser) -> dict[str, image_concrete.Slice2D]:
        return {
            slice_id: image_concrete.Slice2D(slice_file_path)
            for slice_id, slice_file_path
            in initialiser['slice_file_path_map'].items()
        }
    
    def _construct_slice_mask_map(
        self, initialiser: Initialiser,
    ) -> dict[str, image_concrete.SliceMask2D]:
        return {
            slice_id: image_concrete.SliceMask2D(slice_mask_file_path)
            for slice_id, slice_mask_file_path
            in initialiser['slice_mask_file_path_map'].items()
        }
    
    def _construct_transformation_map(
        self, initialiser: Initialiser,
    ) -> dict[str, transformation.RigidTransformation]:
        try:
            return self._construct_transformation_map_by_spreadsheet(
                initialiser)
        except:
            return self._construct_transformation_map_by_none(initialiser)
    
    def _construct_transformation_map_by_spreadsheet(
        self, initialiser: Initialiser) -> dict[str, TRANSFORMATION_TYPE]:
        transformation_spreadsheet = self._read_transformation_spreadsheet(
            initialiser)
        transformation_map = self._build_transformation_map(
            transformation_spreadsheet, initialiser)
        return transformation_map
    
    def _read_transformation_spreadsheet(
        self, initialiser: Initialiser) -> pd.DataFrame:
        return io_utils.read_file(
            initialiser['transformation_spreadsheet_file_path'])
    
    def _build_transformation_map(
        self,
        transformation_spreadsheet: pd.DataFrame,
        initialiser: Initialiser,
    ) -> dict[str, TRANSFORMATION_TYPE]:
        return {
            slice_id:
                self._build_transformation(slice_id, transformation_spreadsheet)
            for slice_id in initialiser['slice_file_path_map']
        }
    
    def _build_transformation(
        self, slice_id: str, transformation_spreadsheet: pd.DataFrame,
    )-> TRANSFORMATION_TYPE:
        """This function is hard-coded (Dangerous!!!) to use rigid transformations."""
        transformation_parameter = self._extract_transformation_parameter(
            slice_id, transformation_spreadsheet)
        transformation_rigid = TRANSFORMATION_TYPE(transformation_parameter)
        return transformation_rigid
    
    def _extract_transformation_parameter(
        self, slice_id: str, transformation_spreadsheet: pd.DataFrame,
    ) -> tuple[float, ...]:
        slice_row = transformation_spreadsheet.loc[
            transformation_spreadsheet['slice_id'] == slice_id]
        transformation_parameter = tuple(
            float(slice_row[column])
            for column in slice_row.columns[2:]  # Get rid of the first 2 'case_id' and 'slice_id' columns
        )
        return transformation_parameter
    
    def _construct_transformation_map_by_none(
        self, initialiser: Initialiser) -> dict[str, TRANSFORMATION_TYPE]:
        return {
            slice_id: TRANSFORMATION_TYPE()
            for slice_id in initialiser['slice_file_path_map']
        }
    
    def _construct_transformation_spreadsheet_file_path(
        self, initialiser: Initialiser) -> str:
        return initialiser['transformation_spreadsheet_file_path']