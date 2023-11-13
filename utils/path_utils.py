"""Utils for processing paths.

This module contains utility functions that facilitate
processing paths at runtime.

Created by: Weixun Luo
Date: 21/03/2023
"""
from __future__ import annotations
import pathlib
import typing


PathSequence: typing.TypeAlias = tuple[pathlib.Path, ...]
StrSequence: typing.TypeAlias = tuple[str, ...]


def extract_directory_name(directory_path: str) -> str:
    return pathlib.Path(directory_path).name

def extract_file_extension(file_path: str) -> str:
    return ''.join(pathlib.Path(file_path).suffixes)

def extract_file_name(file_path: str) -> str:
    return pathlib.Path(file_path).name

def is_on_server() -> bool:
    return str(pathlib.Path.home().parent) == '/home'

def list_subdirectory(
    directory_path: str,
    require_absolute: bool = True,
    require_sort: bool = True,
) -> StrSequence:
    subdirectory = _list_subdirectory(directory_path)
    subdirectory = _resolve(subdirectory, require_absolute)
    subdirectory = _sort(subdirectory, require_sort)
    subdirectory = _to_str_sequence(subdirectory)
    return subdirectory

def _list_subdirectory(directory_path: str) -> PathSequence:
    return tuple(
        subdirectory
        for subdirectory in pathlib.Path(directory_path).iterdir()
        if subdirectory.is_dir()
    )

def _resolve(
    path_sequence: PathSequence, require_absolute: bool) -> PathSequence:
    if require_absolute:
        return tuple(path.resolve() for path in path_sequence)
    else:
        return path_sequence

def _sort(path_sequence:PathSequence, require_sort: bool) -> PathSequence:
    if require_sort:
        return sorted(path_sequence)
    else:
        return path_sequence

def _to_str_sequence(path_sequence: PathSequence) -> StrSequence:
    return tuple(str(path) for path in path_sequence)

def make_directory(directory_path: str) -> None:
    pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)

def search_directory(
    directory_path: str,
    pattern: str,
    require_absolute: bool = True,
    require_sort: bool = True,
) -> tuple[str, ...]:
    path_matched = _search_directory(directory_path, pattern)
    path_matched = _resolve(path_matched, require_absolute)
    path_matched = _sort(path_matched, require_sort)
    path_matched = _to_str_sequence(path_matched)
    return path_matched

def _search_directory(directory_path: str, pattern: str) -> PathSequence:
    return tuple(pathlib.Path(directory_path).glob(pattern))