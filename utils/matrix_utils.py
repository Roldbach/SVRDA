"""Utils for processing matrices.

This module contains utility functions that facilitate
processing matrices at runtime.

Created by: Weixun Luo
Date: 06/04/2023
"""
from __future__ import annotations
from collections import abc

import numpy as np


PRECISION = np.float32


def build_from_iterable(
    iterable: abc.Iterable, data_type: type, element_length: int) -> np.ndarray:
    return np.fromiter(iterable, dtype=np.dtype((data_type, element_length)))

def build_identity(length: int = 4) -> np.ndarray:
    return cast(np.diag((1.0,) * length))

def cast(matrix: np.ndarray, data_type: type = PRECISION) -> np.ndarray:
    return matrix if matrix.dtype == data_type else matrix.astype(data_type)

def norm_2_columnwise(matrix: np.ndarray) -> np.ndarray:
    return np.linalg.norm(matrix, axis=0)

def power(matrix: np.ndarray, exponent: int) -> np.ndarray:
    return np.linalg.matrix_power(matrix, exponent)
