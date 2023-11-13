"""Resampling Processing Unit.

This module contains the implementation of Resampling
Processing Unit used in the application. It is a sub-
component of AppFactory, which can handle all operations
related to the resampling of body images/organ labels.

Created by: Weixun Luo
Date: 10/04/2023
"""
from __future__ import annotations
import typing

import numpy as np

from object import record
from object import resampler


Initialiser: typing.TypeAlias = record.ResamplingProcessingUnitInitialiser


class ResamplingProcessingUnit:
    """Resampling Processing Unit.
    
    A sub-component of AppFactory, which can handle all
    operations related to the resampling of body images and
    organ labels.
    """

    def __init__(self) -> None:
        self._body_resampler = None
        self._organ_resampler = None
    
    def set_up(self, initialiser: Initialiser) -> None:
        self._body_resampler = self._construct_body_resampler(initialiser)
        self._organ_resampler = self._construct_organ_resampler(initialiser)
    
    def _construct_body_resampler(
        self, initialiser: Initialiser) -> resampler.Body3DResampler:
        return resampler.Body3DResampler(
            initialiser['body_resampler_initialiser'])
        
    def _construct_organ_resampler(
        self, initialiser: Initialiser) -> resampler.Organ3DResampler:
        return resampler.Organ3DResampler(
            initialiser['organ_resampler_initialiser'])
    
    def resample_body(self, plain_affine: np.ndarray) -> np.ndarray:
        return self._body_resampler.resample(plain_affine)
    
    def resample_organ(self, plain_affine: np.ndarray) -> np.ndarray:
        return self._organ_resampler.resample(plain_affine)