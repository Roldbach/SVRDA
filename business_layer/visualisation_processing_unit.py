"""Visualisation Processing Unit.

This module contains the implementation of Visualisation
Processing Unit used in the application. It is a sub-
component of AppFactory, which contains default visual
properties of all data during setup.

Created by: Weixun Luo
Date: 10/04/2023
"""
from __future__ import annotations
import typing

from object import record
from utils import format_utils
from utils import image_processing_utils


BODY_VISIBILITY = 1
BODY_RESAMPLED_OPACITY = 1.0
ORGAN_VISIBILITY = 1
ORGAN_RESAMPLED_THRESHOLD = 0.5
ORGAN_RESAMPLED_OPACITY = 0.3
SLICE_OPACITY = 1.0
SLICE_VISIBILITY = 1
CONTOUR_LINE_WIDTH = 2
CHECKERBOARD_BOARD_WIDTH = 35
CAMERA_PROPERTY_MAP = {
    '+x': record.CameraProperty(position=(-1, 0, 0), view_up=(0, 0, 1)),
    '-x': record.CameraProperty(position=(1, 0, 0), view_up=(0, 0, 1)),
    '+y': record.CameraProperty(position=(0, -1, 0), view_up=(0, 0, 1)),
    '-y': record.CameraProperty(position=(0, 1, 0), view_up=(0, 0, 1)),
    '+z': record.CameraProperty(position=(0, 0, -1), view_up=(0, 1, 0)),
    '-z': record.CameraProperty(position=(0, 0, 1), view_up=(0, 1, 0)),
}  # This is the same as the camera properties in ParaView

Initialiser: typing.TypeAlias = record.VisualisationProcessingUnitInitialiser


class VisualisationProcessingUnit:
    """Visualisation Processing Unit.
    
    A sub-component of AppFactory, which contains default
    visual properties of all data during setup. Shallow
    copy is applied to ensure the encapsulation.
    """

    def __init__(self) -> None:
        self._body_property = None
        self._body_resampled_property = None
        self._organ_property = None
        self._organ_resampled_property = None
        self._slice_property = None
        self._contour_property = None
        self._checkerboard_property = None
        self._camera_property_map = None
    
    def set_up(self, initialiser: Initialiser) -> None:
        self._body_property = self._construct_body_property()
        self._body_resampled_property = self._construct_body_resampled_property(
            initialiser)
        self._organ_property = self._construct_organ_property()
        self._organ_resampled_property = self._construct_organ_resampled_property()
        self._slice_property = self._construct_slice_property(initialiser)
        self._contour_property = self._construct_contour_property()
        self._checkerboard_property = self._construct_checkerboard_property()
        self._camera_property_map = self._construct_camera_property_map()
    
    def _construct_body_property(self) -> record.Body3DProperty:
        return record.Body3DProperty(visibility=BODY_VISIBILITY)
    
    def _construct_body_resampled_property(
        self, initialiser: Initialiser) -> record.BodyResampled2DProperty:
        range = image_processing_utils.auto_contrast(
            initialiser['body_pixel_data'])
        window = format_utils.convert_range_to_window(range)
        return record.BodyResampled2DProperty(
            window_level = int(window[0]),
            window_width = int(window[1]),
            opacity = BODY_RESAMPLED_OPACITY,
        )
    
    def _construct_organ_property(self) -> record.Organ3DProperty:
        return record.Organ3DProperty(visibility=ORGAN_VISIBILITY)

    def _construct_organ_resampled_property(
        self) -> record.OrganResampled2DProperty:
        return record.OrganResampled2DProperty(
            threshold = ORGAN_RESAMPLED_THRESHOLD,
            opacity = ORGAN_RESAMPLED_OPACITY,
        )
    
    def _construct_slice_property(
        self, initialiser: Initialiser) -> record.Slice2DProperty:
        range = image_processing_utils.auto_contrast(
            initialiser['slice_pixel_data'])
        window = format_utils.convert_range_to_window(range)
        return record.Slice2DProperty(
            window_level = int(window[0]),
            window_width = int(window[1]),
            opacity = SLICE_OPACITY,
            visibility = SLICE_VISIBILITY,
        )
    
    def _construct_contour_property(self) -> record.ContourProperty:
        return record.ContourProperty(line_width=CONTOUR_LINE_WIDTH)
    
    def _construct_checkerboard_property(self) -> record.CheckerboardProperty:
        return record.CheckerboardProperty(board_width=CHECKERBOARD_BOARD_WIDTH)
    
    def _construct_camera_property_map(
        self) -> dict[str, record.CameraProperty]:
        return CAMERA_PROPERTY_MAP
    
    @property
    def body_property(self) -> record.Body3DProperty:
        return self._get_body_property_by_property()
    
    def _get_body_property_by_property(self) -> record.Body3DProperty:
        return dict(self._body_property)
    
    @property
    def body_resampled_property(self) -> record.BodyResampled2DProperty:
        return self._get_body_resampled_property_by_property()

    def _get_body_resampled_property_by_property(
        self) -> record.BodyResampled2DProperty:
        return dict(self._body_resampled_property)
    
    @property
    def organ_property(self) -> record.Organ3DProperty:
        return self._get_organ_property_by_property()
    
    def _get_organ_property_by_property(
        self) -> record.OrganResampled2DProperty:
        return dict(self._organ_property)
    
    @property
    def organ_resampled_property(self) -> record.OrganResampled2DProperty:
        return self._get_organ_resampled_property_by_property()
    
    def _get_organ_resampled_property_by_property(
        self) -> record.OrganResampled2DProperty:
        return dict(self._organ_resampled_property)
    
    @property
    def slice_property(self) -> record.Slice2DProperty:
        return self._get_slice_property_by_property()
    
    def _get_slice_property_by_property(self) -> record.Slice2DProperty:
        return dict(self._slice_property)
    
    @property
    def contour_property(self) -> record.ContourProperty:
        return self._get_contour_property_by_property()
    
    def _get_contour_property_by_property(self) -> record.ContourProperty:
        return dict(self._contour_property)
    
    @property
    def checkerboard_property(self) -> record.CheckerboardProperty:
        return self._get_checkerboard_property_by_property()
    
    def _get_checkerboard_property_by_property(
        self) -> record.CheckerboardProperty:
        return dict(self._checkerboard_property)

    @property
    def camera_property_map(self) -> dict[str, record.CameraProperty]:
        return self._get_camera_property_map_by_property()
    
    def _get_camera_property_map_by_property(
        self) -> dict[str, record.CameraProperty]:
        return dict(self._camera_property_map)