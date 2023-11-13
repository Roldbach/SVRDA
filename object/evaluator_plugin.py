"""Plugins of Evaluator.

This module contains the implementation of all plugins of
Evaluator, which define all available evaluation metrics
used at runtime.

Created by: Weixun Luo
Date: 20/04/2023
"""
from __future__ import annotations

import numpy as np


class MultiModalEvaluationMetricPlugin:
    """Plugin that contains multi-modal evaluation metrics."""

    def _compute_normalised_mutual_information(
        self, candidate: np.ndarray, reference:np.ndarray) -> float:
        """Computes the Normalised Mutual Information.

        Computes the Normalised Mutual Information between
        the candidate and reference.
        """
        # Joint histogram
        jh, _, _ = np.histogram2d(candidate.ravel(), reference.ravel(), bins=256)

        # Compute marginal histograms
        jh = jh / np.sum(jh)
        s1 = np.sum(jh,axis=0).reshape((-1,jh.shape[0]))
        s2 = np.sum(jh,axis=1).reshape((jh.shape[1],-1))

        # Compute entropy values. Note that the value of 
        # log(x + (x==0).astype(float)) equals 0 when x=0
        # and equals log(x) otherwise. This is just a trick  
        # to force log(0)=0
        H12 = -1 * np.sum(jh * np.log2(jh + (jh==0).astype(float)))
        H1 = -1 * np.sum(s1 * np.log2(s1 + (s1==0).astype(float)))
        H2 = -1 * np.sum(s2 * np.log2(s2 + (s2==0).astype(float)))

        return 2 * (H1 + H2 - H12) / (H1 + H2)

class PixelwiseEvaluationMetricPlugin:
    """Plugin that contains pixelwise evaluation metrics."""

    def _compute_sum_absolute_difference(
        self, candidate: np.ndarray, reference: np.ndarray) -> float:
        return np.abs(candidate - reference).sum()