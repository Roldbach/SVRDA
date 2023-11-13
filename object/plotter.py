"""Plotter.

This module contains the abstract template and concrete
implementations of different plotters used in the
application. Plotter is a tool that can build serialised
figure data for different types of 2D images.


Created by: Weixun Luo
Date: 12/04/2023
"""
from __future__ import annotations
import abc

import numpy as np

from utils import format_utils
from utils import image_processing_utils
from utils import matrix_utils


class PlotterABC(abc.ABC):
    """Template of plotters.

    A template of objects that can build serialised figure
    data for different types of 2D images.
    """

    @abc.abstractmethod
    def plot(self) -> str:
        pass

    @abc.abstractmethod
    def _process(self, pixel_data: np.ndarray) -> np.ndarray:
        pass
    
    @abc.abstractmethod
    def _serialise(self, pixel_data: np.ndarray) -> np.ndarray:
        pass


class ImagePlotter(PlotterABC):
    """Plotter for 2D grayscale images.
    
    An object that can build serialised figure data for 2D
    grayscale images.
    """

    def __init__(self) -> None:
        pass
    
    def plot(self, pixel_data: np.ndarray, window: tuple[int, int]) -> str:
        pixel_data = self._process(pixel_data, window)
        pixel_data = self._serialise(pixel_data)
        return pixel_data
    
    def _process(
        self, pixel_data: np.ndarray, window: tuple[int, int]) -> np.ndarray:
        range = format_utils.convert_window_to_range(window)
        pixel_data = image_processing_utils.quantise(pixel_data, range)
        pixel_data = image_processing_utils.correct_plotting_orientation(
            pixel_data)
        return pixel_data
    
    def _serialise(self, pixel_data: np.ndarray) -> np.ndarray:
        return image_processing_utils.serialise_to_png(
            pixel_data,
            image_processing_utils.PILLOW_IMAGE_MODE_MAP['grayscale'],
        )

class ContourPlotter(PlotterABC):
    """Plotter for 2D rgb contours.
    
    An object that can build serialised figure data for 2D
    RGB contours.
    """

    def __init__(self) -> None:
        pass

    def plot(self, pixel_data: np.ndarray) -> np.ndarray:
        pixel_data = self._process(pixel_data)
        pixel_data = self._serialise(pixel_data)
        return pixel_data

    def _process(self, pixel_data: np.ndarray) -> np.ndarray:
        return image_processing_utils.correct_plotting_orientation(pixel_data)
    
    def _serialise(self, pixel_data: np.ndarray) -> np.ndarray:
        return image_processing_utils.serialise_to_array(pixel_data)

class MaskPlotter(PlotterABC):
    """Plotter for 2D RGBA masks.

    An object that can build serialised figure data for 2D
    RGBA masks.
    """

    def __init__(self) -> None:
        self._lookup_table = self._construct_lookup_table()
    
    def _construct_lookup_table(self) -> np.ndarray:
        """This is hard-coded to the same one in the ITK Snap segmentation."""
        lookup_table = np.zeros((1, 256, 3), dtype=np.uint8)
        lookup_table[0][1][:] = (255, 0, 0)  # Label 1: Red
        lookup_table[0][2][:] = (0, 255, 0)  # Label 2: Blue
        lookup_table[0][3][:] = (0, 0, 255)  # Label 3: Green
        lookup_table[0][4][:] = (255, 255, 0)  # Label 4: Yellow 
        lookup_table[0][5][:] = (0, 255, 255)  # Label 5: Cyan
        lookup_table[0][6][:] = (255, 0, 255)  # Label 6: Magenta
        return lookup_table
    
    def plot(self, pixel_data: np.ndarray, opacity: float) -> str:
        pixel_data = self._process(pixel_data, opacity)
        pixel_data = self._serialise(pixel_data)
        return pixel_data
    
    def _process(self, pixel_data: np.ndarray, opacity: float) -> np.ndarray:
        pixel_data = image_processing_utils.correct_plotting_orientation(
            pixel_data)
        rgba = self._build_rgba(pixel_data, opacity)
        return rgba

    def _build_rgba(self, pixel_data: np.ndarray, opacity: float) -> np.ndarray:
        rgb = self._build_rgb(pixel_data)
        alpha = self._build_alpha(pixel_data, opacity)
        rgba = self._concatenate(rgb, alpha)
        return rgba
        
    def _build_rgb(self, pixel_data: np.ndarray) -> np.ndarray:
        rgb = self._stack(pixel_data)
        rgb = image_processing_utils.look_up(rgb, self._lookup_table)
        rgb = matrix_utils.cast(rgb, np.uint8)
        return rgb
    
    def _stack(self, pixel_data: np.ndarray) -> np.ndarray:
        return np.stack((pixel_data,)*3, axis=2)
    
    def _build_alpha(
        self, pixel_data: np.ndarray, opacity: float) -> np.ndarray:
        alpha = image_processing_utils.binarise(pixel_data, activation=opacity)
        alpha = image_processing_utils.quantise(alpha, (0.0, 1.0))
        alpha = np.expand_dims(alpha, axis=2)
        return alpha
    
    def _concatenate(self, rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        return np.concatenate((rgb, alpha), axis=2)

    def _serialise(self, pixel_data: np.ndarray) -> np.ndarray:
        return image_processing_utils.serialise_to_png(
            pixel_data,
            image_processing_utils.PILLOW_IMAGE_MODE_MAP['rgba'],
        )

class CheckerboardPlotter(PlotterABC):
    """Plotter for 2D grayscale checkerboard images.

    An object that can build serialised figure data for 2D
    grayscale checkerboard images.
    """

    def __init__(self) -> None:
        self._board_width = 0
        self._board_black = None
        self._board_white = None
    
    def plot(
        self,
        pixel_data_pair: tuple[np.ndarray, np.ndarray],
        window_pair: tuple[tuple[int, int], tuple[int, int]],
        board_width: int,
    ) -> str:
        pixel_data = self._process(pixel_data_pair, window_pair, board_width)
        pixel_data = self._serialise(pixel_data)
        return pixel_data
    
    def _process(
        self,
        pixel_data_pair: tuple[np.ndarray, np.ndarray],
        window_pair: tuple[tuple[int, int], tuple[int, int]],
        board_width: int,
    ) -> np.ndarray:
        pixel_data_pair = self._process_pair(pixel_data_pair, window_pair)
        self._update_board(pixel_data_pair[0].shape, board_width)
        checkerboard = self._build_checkerboard(pixel_data_pair)
        return checkerboard
        
    def _process_pair(
        self,
        pixel_data_pair: tuple[np.ndarray, np.ndarray],
        window_pair: tuple[tuple[int, int], tuple[int, int]],
    ) -> tuple[np.ndarray, np.ndarray]:
        return tuple(
            self._process_single(pixel_data, window)
            for pixel_data, window in zip(pixel_data_pair, window_pair)
        )

    def _process_single(
        self, pixel_data: np.ndarray, window: tuple[int, int]) -> np.ndarray:
        range = format_utils.convert_window_to_range(window)
        pixel_data = image_processing_utils.quantise(pixel_data, range)
        pixel_data = image_processing_utils.correct_plotting_orientation(
            pixel_data)
        return pixel_data
    
    def _update_board(self, size: tuple[int, int], board_width: int) -> None:
        if self._board_width != board_width:
            self._board_width = board_width
            self._board_black = self._build_board_black(size, board_width)
            self._board_white = self._build_board_white()
    
    def _build_board_black(
        self, size: tuple[int, int], board_width: int) -> np.ndarray:
        row_index, column_index = np.indices(size, np.uint16)
        board_black = np.zeros(size, np.uint8)
        board_black[(row_index//board_width)%2 == (column_index//board_width)%2] = 1
        return board_black

    def _build_board_white(self) -> np.ndarray:
        board = np.ones(self._board_black.shape, np.uint8)
        board_white = board - self._board_black
        return board_white
    
    def _build_checkerboard(
        self, pixel_data_pair: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
        pixel_data_black = image_processing_utils.mask(
            pixel_data_pair[0], self._board_black)
        pixel_data_white = image_processing_utils.mask(
            pixel_data_pair[1], self._board_white)
        checkerboard = pixel_data_black + pixel_data_white
        return checkerboard
    
    def _serialise(self, pixel_data: np.ndarray) -> np.ndarray:
        return image_processing_utils.serialise_to_png(
            pixel_data,
            image_processing_utils.PILLOW_IMAGE_MODE_MAP['grayscale'],
        )