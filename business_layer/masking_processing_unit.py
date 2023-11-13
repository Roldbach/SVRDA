"""Masking Processing Unit.

This module contains the implementation of Masking
Processing Unit used in the application. It is a sub-
component of AppFactory, which can build all different types
of masks used in the application.

Created by: Weixun Luo
Date: 16/04/2023
"""
from __future__ import annotations

import numpy as np

from utils import image_processing_utils
from utils import matrix_utils


class MaskingProcessingUnit:
    """Masking Processing Unit.

    A sub-component of AppFactory, which can build all
    different types of masks used in the application.
    """

    def __init__(self) -> None:
        pass
    
    def build_organ_resampled_mask(
        self, organ_resampled: np.ndarray, threshold: float) -> np.ndarray:
        if self._is_single_organ(organ_resampled):
            return self._build_organ_resampled_mask_single(
                 organ_resampled, threshold)
        else:
            return self._build_organ_resampled_mask_multi(organ_resampled)
    
    def _is_single_organ(self, organ_resampled: np.ndarray) -> bool:
        return np.floor(np.amax(organ_resampled)) == 1
    
    def _build_organ_resampled_mask_single(
        self, organ_resampled: np.ndarray, threshold: float) -> np.ndarray:
        """For single-organ labels, this function assumes float data type."""
        return image_processing_utils.binarise(organ_resampled, threshold)
    
    def _build_organ_resampled_mask_multi(
        self, organ_resampled: np.ndarray) -> np.ndarray:
        """For multi-organ labels, this function assumes int data type."""
        return matrix_utils.cast(organ_resampled, np.uint8)
    
    def build_evaluation_mask(
        self, slice_mask: np.ndarray, body_resampled: np.ndarray,
    ) -> np.ndarray:
        """This is equivalent to Slice-body mask mentioned in the paper."""
        body_mask = self._build_body_mask(body_resampled)
        evaluation_mask = image_processing_utils.mask(slice_mask, body_mask)
        return evaluation_mask
    
    def _build_body_mask(self, body_resampled: np.ndarray) -> np.ndarray:
        return image_processing_utils.binarise(body_resampled)