"""Plugins of Data Accessor.

This module contains the implementation of all plugins 
of Transformation Processing Unit. They are specifically
designed interfaces which offer efficient and accurate data
access for corresponding components in the application.

Created by: Weixun Luo
Date: 10/04/2023
"""
from __future__ import annotations

import numpy as np

from object import record
from object import transformation
from utils import affine_utils
from utils import matrix_utils


# Use NifTI coordinate system by default
SCANNER_COORDINATE_DIRECTION = (-1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)


class TransformationProcessingUnitPlugin:
    """Interface designed for Transformation Processing Unit."""

    def build_transformation_processing_unit_initialiser(
        self) -> record.TransformationProcessingUnitInitialiser:
        return record.TransformationProcessingUnitInitialiser(
            transformation_map = self._transformation_map)
    
    def get_scanner_coordinate_translate_kwargs(
        self, axis_name: str) -> dict[str, tuple[float, float, float]]:
        return {
            'axis': affine_utils.extract_axis(
                SCANNER_COORDINATE_DIRECTION, axis_name),
        }
    
    def get_slice_coordinate_translate_kwargs(
        self, slice_id: str, axis_name: str) -> dict:
        slice = self._slice_map[slice_id]
        return {
            'axis': affine_utils.extract_axis(slice.affine_current, axis_name),
        }
    
    def get_slice_coordinate_rotate_macro_kwargs(
        self, slice_id: str, axis_name: str) -> dict:
        slice = self._slice_map[slice_id]
        return {
            'affine_current': slice.affine_current,
            'affine_original': slice.affine_original,
            'centre': self._get_mean_slice_centroid(),
            'axis': self._get_mean_slice_axis(axis_name),
        }

    def _get_mean_slice_centroid(self) -> tuple[float, float, float]:
        slice_centroid_matrix = matrix_utils.build_from_iterable(
            iterable = (slice.centroid for slice in self._slice_map.values()),
            data_type = np.float32,
            element_length = 3,
        )
        mean_slice_centroid = np.mean(slice_centroid_matrix, axis=0)
        mean_slice_centroid = tuple(mean_slice_centroid)
        return mean_slice_centroid

    def _get_mean_slice_axis(
        self, axis_name: str) -> tuple[float, float, float]:
        slice_axis_matrix = matrix_utils.build_from_iterable(
            iterable = (
                affine_utils.extract_axis(slice.affine_current, axis_name)
                for slice in self._slice_map.values()
            ),
            data_type = np.float32,
            element_length = 3,
        )
        mean_slice_axis = np.mean(slice_axis_matrix, axis=0)
        mean_slice_axis = tuple(mean_slice_axis)
        return mean_slice_axis
    
    def get_slice_coordinate_rotate_micro_kwargs(
        self, slice_id: str, axis_name: str) -> dict:
        slice = self._slice_map[slice_id]
        return {
            'affine_current': slice.affine_current,
            'affine_original': slice.affine_original,
            'centre': slice.centroid,
            'axis': affine_utils.extract_axis(slice.affine_current, axis_name),
        }

    def update_transformation(
        self,
        slice_id: str,
        transformation: transformation.TransformationABC,
    ) -> None:
        self._transformation_map[slice_id] = transformation

class VisualisationProcessingUnitPlugin:
    """Interface designed for Visualisation Processing Unit."""

    def build_visualisation_processing_unit_initialiser(
        self) -> record.VisualisationProcessingUnitInitialiser:
        slice = next(iter(self._slice_map.values()))
        return record.VisualisationProcessingUnitInitialiser(
            body_pixel_data = self._body.pixel_data,
            organ_pixel_data = self._organ.pixel_data,
            slice_pixel_data = slice.pixel_data,
        )

class ResamplingProcessingUnitPlugin:
    """Interface designed for Resampling Processing Unit."""

    def build_resampling_processing_unit_initialiser(
        self) -> record.ResamplingProcessingUnitInitialiser:
        return record.ResamplingProcessingUnitInitialiser(
            body_resampler_initialiser = self._get_body_resampler_initialiser(),
            organ_resampler_initialiser = self._get_organ_resampler_initialiser(),
        )
    
    def _get_body_resampler_initialiser(self) -> record.ResamplerInitialiser:
        slice = next(iter(self._slice_map.values()))
        return record.ResamplerInitialiser(
            plain_size = slice.pixel_data.shape,
            grid_pixel_data = self._body.pixel_data,
            grid_affine = self._body.affine_original,
        )
    
    def _get_organ_resampler_initialiser(self) -> record.ResamplerInitialiser:
        slice = next(iter(self._slice_map.values()))
        return record.ResamplerInitialiser(
            plain_size = slice.pixel_data.shape,
            grid_pixel_data = self._organ.pixel_data,
            grid_affine = self._organ.affine_original,
        )
    
    def get_resample_body_kwargs(self, slice_id: str) -> dict[str, np.ndarray]:
        return {'plain_affine':self._slice_map[slice_id].affine_current}

    def get_resample_organ_kwargs(self, slice_id: str) -> dict[str, np.ndarray]:
        return {'plain_affine':self._slice_map[slice_id].affine_current}
    
    def update_body_resampled(
        self, slice_id: str, pixel_data: np.ndarray) -> None:
        self._body_resampled_map[slice_id].pixel_data = pixel_data
    
    def update_organ_resampled(
        self, slice_id: str, pixel_data: np.ndarray) -> None:
        self._organ_resampled_map[slice_id].pixel_data = pixel_data

class MaskingProcessingUnitPlugin:
    """Interface designed for Masking Processing Unit."""

    def get_build_organ_resampled_mask_kwargs(
        self, slice_id: str) -> dict[str, np.ndarray]:
        return {
            'organ_resampled': self._organ_resampled_map[slice_id].pixel_data,
        }
    
    def get_build_evaluation_mask_kwargs(
        self, slice_id: str) -> dict[str, np.ndarray]:
        return {
            'slice_mask': self._slice_mask_map[slice_id].pixel_data,
            'body_resampled': self._body_resampled_map[slice_id].pixel_data,
        }

class PlottingProcessingUnitPlugin:
    """Interface designed for Plotting Processing Unit."""

    def get_build_slice_image_kwargs(
        self, slice_id: str) -> dict[str, np.ndarray]:
        return {'pixel_data':self._slice_map[slice_id].pixel_data}
    
    def get_build_body_resampled_image_kwargs(
        self, slice_id: str) -> dict[str, np.ndarray]:
        return {'pixel_data':self._body_resampled_map[slice_id].pixel_data}
    
    def get_build_slice_body_resampled_checkerboard_kwargs(
        self, slice_id: str) -> dict[str, tuple[np.ndarray, np.ndarray]]:
        return {
            'pixel_data_pair': (
                self._slice_map[slice_id].pixel_data,
                self._body_resampled_map[slice_id].pixel_data,
            ),
        }

class EvaluationProcessingUnitPlugin:
    """Interface designed for Evaluation Processing Unit."""

    def build_evaluation_processing_unit_initialiser(
        self) -> record.EvaluationProcessingUnitInitialiser:
        return record.EvaluationProcessingUnitInitialiser(
            evaluation_metric_name_sequence =
                self.build_evaluation_metric_name_sequence(),
            slice_id_sequence = tuple(self._slice_map.keys())
        )
    
    def build_evaluation_metric_name_sequence(self) -> tuple[str, ...]:
        """Also used by AppFactory."""
        return ('NMI', 'SAD')
    
    def get_evaluate_kwargs(self, slice_id: str) -> dict[str, np.ndarray]:
        return {
            'candidate': self._body_resampled_map[slice_id].pixel_data,
            'reference': self._slice_map[slice_id].pixel_data,
        }

class IOProcessingUnitPlugin:
    """Interface designed for IO Processig Unit."""

    def get_write_transformation_spreadsheet_kwargs(self) -> dict:
        return {
            'case_id': self._case_id,
            'slice_id_sequence': tuple(self._transformation_map.keys()),
            'transformation_parameter_matrix': matrix_utils.build_from_iterable(
                iterable = (
                    transformation.parameter
                    for transformation in self._transformation_map.values()
                ),
                data_type = np.float32,
                element_length = 6, # This is currently hard-coded to rigid transformations
            ),
            'file_path': self._transformation_spreadsheet_file_path,
        }
    
    def get_write_organ_resampled_map_kwargs(self) -> dict:
        return {
            'pixel_data_map': {
                slice_id: organ_resampled.pixel_data
                for slice_id, organ_resampled
                in self._organ_resampled_map.items()
            },
            'affine_map': {
                slice_id: slice.affine_current
                for slice_id, slice in self._slice_map.items()
            },
            'file_path_map': self._organ_resampled_file_path_map,
        }

class AppFactoryPlugin:
    """Interface designed for App Factory."""

    def get_build_body_representation_kwargs(self) -> dict:
        return {'state':self._body.state}

    def get_build_organ_representation_kwargs(self) -> dict:
        return {'state':self._organ.state}

    def get_build_slice_representation_sequence_kwargs(self) -> dict:
        return {
            'state_map': {
                slice_id: slice.state
                for slice_id, slice in self._slice_map.items()
            },
        }
    
    def get_slice_selection_dropdown_kwargs(self) -> dict:
        slice_id_sequence = tuple(self._slice_map.keys())
        return {'option':slice_id_sequence, 'value':slice_id_sequence[0]}
    
    def get_patch_refresh_slice_state_kwargs(self, slice_id: str) -> dict:
        affine_current = self._slice_map[slice_id].affine_current
        return {
            'spacing': affine_utils.extract_spacing(affine_current),
            'direction': affine_utils.extract_direction(affine_current),
            'origin': affine_utils.extract_origin(affine_current),
        }
    
    def transform_slice(self, slice_id:str) -> None:
        transformation = self._transformation_map[slice_id]
        self._slice_map[slice_id].transform(transformation.matrix)