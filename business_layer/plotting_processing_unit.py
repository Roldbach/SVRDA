"""Plotting Processing Unit.

This module contains the implementation of Plotting
Processing Unit used in the application. It is a sub-
component of AppFactory, which can handle all operations
related to the plotting of 2D images.

Created by: Weixun Luo
Date: 11/04/2023
"""
from __future__ import annotations

import numpy as np

from object import plotter


class PlottingProcessingUnit:
    """Plotting Processing Unit.
    
    A sub-component of AppFactory, which can handle all
    operations related to the plotting of 2D images.
    """

    def __init__(self) -> None:
        self._image_plotter = plotter.ImagePlotter()
        self._contour_plotter = plotter.ContourPlotter()
        self._mask_plotter = plotter.MaskPlotter()
        self._checkerboard_plotter = plotter.CheckerboardPlotter()
    
    def build_slice_image(
        self, pixel_data: np.ndarray, window: tuple[int, int]) -> str:
        return self._image_plotter.plot(pixel_data, window)
    
    def build_body_resampled_image(
        self, pixel_data: np.ndarray, window: tuple[int, int]) -> str:
        return self._image_plotter.plot(pixel_data, window)
    
    def build_organ_resampled_contour(self, pixel_data: np.ndarray) -> str:
        return self._contour_plotter.plot(pixel_data)
    
    def build_evaluation_mask_contour(self, pixel_data: np.ndarray) -> str:
        return self._contour_plotter.plot(pixel_data)
    
    def build_organ_resampled_mask(
        self, pixel_data: np.ndarray, opacity: float) -> str:
        return self._mask_plotter.plot(pixel_data, opacity)
    
    def build_evaluation_mask(
        self, pixel_data: np.ndarray, opacity: float) -> str:
        return self._mask_plotter.plot(pixel_data, opacity)
    
    def build_slice_body_resampled_checkerboard(
        self,
        pixel_data_pair: tuple[np.ndarray, np.ndarray],
        window_pair: tuple[tuple[int, int], tuple[int, int]],
        board_width: int,
    ) -> str:
        return self._checkerboard_plotter.plot(
            pixel_data_pair, window_pair, board_width)