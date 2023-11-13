"""Tools to build spreadsheets.

This module contains all objects that can build spreadsheets
in the application.

Created: Weixun Luo
Date: 07/04/2023
"""
from __future__ import annotations
import itertools
import typing

import pandas as pd

from object import record
from utils import affine_utils
from utils import io_utils
from utils import path_utils


DataFrameGenerator: typing.TypeAlias = typing.Generator[pd.DataFrame, None, None]
StrSequence: typing.TypeAlias = tuple[str, ...]


class DatasetSpreadsheetBuilder:
    """Tool to build a dataset spreadsheet.

    An object used to build the dataframe that can describe
    the given dataset.
    """

    def __init__(self, configuration: record.Configuration) -> None:
        self._configuration = configuration
    
    def build_spreadsheet(self) -> pd.DataFrame:
        return pd.concat(self._build_case_iterable(), ignore_index=True)

    def _build_case_iterable(self) -> DataFrameGenerator:
        return (
            self._build_case(case_directory_path)
            for case_directory_path
            in self._build_case_directory_path_sequence()
        )
    
    def _build_case(self, case_directory_path: str) -> pd.DataFrame:
        return pd.concat(
            self._build_subcase_iterable(case_directory_path),
            ignore_index = True,
        )
    
    def _build_subcase_iterable(
        self, case_directory_path: str) -> DataFrameGenerator:
        slice_file_path_group = self._build_slice_file_path_group(
            case_directory_path)
        slice_mask_file_path_group = self._build_slice_mask_file_path_group(
            case_directory_path, slice_file_path_group)
        return (
            self._build_subcase(
                i+1,
                slice_file_path_subgroup,
                slice_mask_file_path_subgroup,
                case_directory_path,
            )
            for i, (slice_file_path_subgroup, slice_mask_file_path_subgroup)
            in enumerate(zip(slice_file_path_group, slice_mask_file_path_group))
        )
    
    def _build_subcase(
        self,
        group_index: int,
        slice_file_path_subgroup: StrSequence,
        slice_mask_file_path_subgroup: StrSequence,
        case_directory_path: str,
    ) -> pd.DataFrame:
        case_id_sequence = self._build_case_id_sequence(
            group_index, len(slice_file_path_subgroup), case_directory_path)
        slice_id_sequence = self._build_slice_id_sequence(
            slice_file_path_subgroup)
        body_file_path_sequence = self._build_body_file_path_sequence(
            len(slice_file_path_subgroup), case_directory_path)
        organ_file_path_sequence = self._build_organ_file_path_sequence(
            len(slice_file_path_subgroup), case_directory_path)
        organ_resampled_file_path_sequence = self._build_organ_resampled_file_path_sequence(
            slice_file_path_subgroup, case_directory_path)
        transformation_spreadsheet_file_path_sequence = self._build_transformation_spreadsheet_file_path_sequence(
            group_index, len(slice_file_path_subgroup), case_directory_path)
        subcase = pd.DataFrame({
            'case_id': case_id_sequence,
            'slice_id': slice_id_sequence,
            'body_file_path': body_file_path_sequence,
            'organ_file_path': organ_file_path_sequence,
            'organ_resampled_file_path': organ_resampled_file_path_sequence,
            'slice_file_path': slice_file_path_subgroup,
            'slice_mask_file_path': slice_mask_file_path_subgroup,
            'transformation_spreadsheet_file_path':
                transformation_spreadsheet_file_path_sequence,
        })
        return subcase
    
    def _build_case_id_sequence(
        self, group_index: int, slice_number: int, case_directory_path: str,
    ) -> StrSequence:
        case_id = self._build_case_id(group_index, case_directory_path)
        case_id_sequence = (case_id,) * slice_number
        return case_id_sequence
    
    def _build_case_id(
        self, group_index: int, case_directory_path: str) -> str:
        case_name = path_utils.extract_directory_name(case_directory_path)
        case_id = f'{case_name}-{group_index}'
        return case_id

    def _build_slice_id_sequence(
        self, slice_file_path_subgroup: StrSequence) -> StrSequence:
        return tuple(
            self._extract_slice_id(slice_file_path)
            for slice_file_path in slice_file_path_subgroup
        )
    
    def _extract_slice_id(self, slice_file_path: str) -> str:
        """slice_id is the name of the slice file, including the extension."""
        slice_file_path_splitted = slice_file_path.split('/')
        slice_id = slice_file_path_splitted[-1]
        return slice_id

    def _build_body_file_path_sequence(
        self, slice_number: int, case_directory_path: str) -> StrSequence:
        body_file_path = self._search_body_file_path_first(case_directory_path)
        body_file_path_sequence = (body_file_path,) * slice_number
        return body_file_path_sequence

    def _search_body_file_path_first(self, case_directory_path: str) -> str:
        try:
            return self._search_body_file_path_first_helper(case_directory_path)
        except IndexError:
            raise ValueError(
                f'Can not find body file with '
                f'<{self._configuration["pattern"]["body"]}> in'
                f'{self._build_body_directory_path(case_directory_path)}'
            )
    
    def _search_body_file_path_first_helper(
        self, case_directory_path: str) -> str:
        return path_utils.search_directory(
            directory_path = self._build_body_directory_path(
                case_directory_path),
            pattern = self._configuration['pattern']['body'],
        )[0]
    
    def _build_body_directory_path(self, case_directory_path: str) -> str:
        return f'{case_directory_path}/{self._configuration["directory_name"]["body"]}'
    
    def _build_organ_file_path_sequence(
        self, slice_number: int, case_directory_path: str) -> StrSequence:
        organ_file_path = self._search_organ_file_path_first(
            case_directory_path)
        organ_file_path_sequence = (organ_file_path,) * slice_number
        return organ_file_path_sequence

    def _search_organ_file_path_first(self, case_directory_path: str) -> str:
        try:
            return self._search_organ_file_path_first_helper(
                case_directory_path)
        except IndexError:
            raise ValueError(
                f'Can not find organ file with '
                f'<{self._configuration["pattern"]["organ"]}> in'
                f'{self._build_organ_directory_path(case_directory_path)}'
            )
    
    def _search_organ_file_path_first_helper(
        self, case_directory_path: str) -> str:
        return path_utils.search_directory(
            directory_path = self._build_organ_directory_path(
                case_directory_path),
            pattern = self._configuration['pattern']['organ'],
        )[0]

    def _build_organ_directory_path(self, case_directory_path: str) -> str:
        return f'{case_directory_path}/{self._configuration["directory_name"]["organ"]}'

    def _build_organ_resampled_file_path_sequence(
        self,
        slice_file_path_subgroup: StrSequence,
        case_directory_path: str,
    ) -> StrSequence:
        organ_resampled_directory_path = self._build_organ_resampled_directory_path(
            case_directory_path)
        organ_resampled_file_path_sequence = tuple(
            self._build_organ_resampled_file_path(
                slice_file_path, organ_resampled_directory_path)
            for slice_file_path in slice_file_path_subgroup
        )
        return organ_resampled_file_path_sequence
    
    def _build_organ_resampled_directory_path(self, case_directory_path: str) -> str:
        organ_resampled_directory_path = f'{case_directory_path}/{self._configuration["directory_name"]["organ_resampled"]}'
        path_utils.make_directory(organ_resampled_directory_path)  # Ensure smooth file writing in the future
        return organ_resampled_directory_path
    
    def _build_organ_resampled_file_path(
        self, slice_file_path: str, organ_resampled_directory_path: str) -> str:
        organ_resampled_file_name = self._build_organ_resampled_file_name(
            slice_file_path)
        organ_resampled_file_path = f'{organ_resampled_directory_path}/{organ_resampled_file_name}'
        return organ_resampled_file_path
    
    def _build_organ_resampled_file_name(self, slice_file_path: str) -> str:
        slice_file_name = self._extract_slice_file_name(slice_file_path)
        organ_resampled_file_name = self._add_organ_resampled_tag(slice_file_name)
        return organ_resampled_file_name
    
    def _extract_slice_file_name(self, slice_file_path: str) -> str:
        return path_utils.extract_file_name(slice_file_path)
    
    def _add_organ_resampled_tag(self, slice_file_name: str) -> str:
        """resampled mask will have the name: slice_id + tag, where tag comes from the configuration file."""
        slice_file_name_splitted = slice_file_name.split('.nii')
        slice_file_name_splitted[-2] = f'{slice_file_name_splitted[-2]}{self._configuration["tag"]["organ_resampled"]}'
        slice_file_name_tagged = '.nii'.join(slice_file_name_splitted)
        return slice_file_name_tagged
    
    def _build_transformation_spreadsheet_file_path_sequence(
        self,
        group_index: int,
        slice_number: int,
        case_directory_path: str) -> StrSequence:
        transformation_spreadsheet_file_path = self._build_transformation_spreadsheet_file_path(
            group_index, case_directory_path)
        transformation_spreadsheet_file_path_sequence = (transformation_spreadsheet_file_path,) * slice_number
        return transformation_spreadsheet_file_path_sequence
    
    def _build_transformation_spreadsheet_file_path(
        self, group_index: int, case_directory_path: str) -> str:
        return f'{case_directory_path}/{self._configuration["file_name"]["transformation_spreadsheet"]}-{group_index}.csv'

    def _build_slice_file_path_group(
        self, case_directory_path: str) -> tuple[StrSequence, ...]:
        slice_file_path_sequence = self._build_slice_file_path_sequence(
            case_directory_path)
        slice_file_path_group = self._group_by_axis_z(slice_file_path_sequence)
        return slice_file_path_group
    
    def _build_slice_file_path_sequence(
        self, case_directory_path: str) -> StrSequence:
        slice_file_path_sequence = self._build_slice_file_path_sequence_helper(
            case_directory_path)
        slice_file_path_sequence = self._sort_by_axis_z(
            slice_file_path_sequence)  # This is necessary for the following groupby operation
        return slice_file_path_sequence
        
    def _build_slice_file_path_sequence_helper(
        self, case_directory_path: str) -> StrSequence:
        slice_file_path_sequence = self._search_slice_file_path(
            case_directory_path)
        if len(slice_file_path_sequence) == 0:
            raise ValueError(
                f'Can not find slice files with '
                f'<{self._configuration["pattern"]["slice"]}> in '
                f'{self._build_slice_directory_path(case_directory_path)}'
            ) 
        else:
            return slice_file_path_sequence
    
    def _search_slice_file_path(self, case_directory_path: str) -> StrSequence:
        return path_utils.search_directory(
            self._build_slice_directory_path(case_directory_path),
            self._configuration['pattern']['slice'],
        )
    
    def _build_slice_directory_path(self, case_directory_path: str) -> str:
        return f'{case_directory_path}/{self._configuration["directory_name"]["slice"]}'

    def _sort_by_axis_z(
        self, slice_file_path_sequence: StrSequence) -> StrSequence:
        return tuple(sorted(slice_file_path_sequence, key=self._extract_axis_z))
    
    def _extract_axis_z(
        self, slice_file_path: str) -> tuple[float, float, float]:
        affine = io_utils.read_affine(slice_file_path)
        axis_z = affine_utils.extract_axis(affine, 'z')
        return axis_z
    
    def _group_by_axis_z(
        self, slice_file_path_sequence: StrSequence) -> tuple[StrSequence, ...] | None:
        return tuple(
            self._sort_by_orgin_z(slice_file_path_subgroup)
            for _, slice_file_path_subgroup
            in itertools.groupby(
                slice_file_path_sequence, key=self._extract_axis_z)
        ) if len(slice_file_path_sequence) != 0 else None

    def _sort_by_orgin_z(
        self,
        slice_file_path_subgroup: typing.Generator[str, None, None],
    ) -> StrSequence:
        return tuple(
            sorted(slice_file_path_subgroup, key=self._extract_origin_z))
    
    def _extract_origin_z(
        self, slice_file_path: str) -> float:
        affine = io_utils.read_affine(slice_file_path)
        origin_z = -1 * affine[2, 3]  # This ensures that the first slice is at the top
        return origin_z

    def _build_slice_mask_file_path_group(
        self,
        case_directory_path: str,
        slice_file_path_group: tuple[StrSequence, ...],
    ) -> tuple:
        slice_mask_file_path_sequence = self._build_slice_mask_file_path_sequence(
            case_directory_path)
        slice_mask_file_path_group = self._group_by_axis_z(
            slice_mask_file_path_sequence)
        return slice_mask_file_path_group if slice_mask_file_path_group is not None else slice_file_path_group
    
    def _build_slice_mask_file_path_sequence(
        self, case_directory_path: str) -> tuple:
        slice_mask_file_path_sequence = self._search_slice_mask_file_path(
            case_directory_path)
        slice_mask_file_path_sequence = self._sort_by_axis_z(
            slice_mask_file_path_sequence)
        return slice_mask_file_path_sequence
    
    def _search_slice_mask_file_path(
        self, case_directory_path: str) -> tuple:
        return path_utils.search_directory(
            self._build_slice_mask_directory_path(case_directory_path),
            self._configuration['pattern']['slice_mask'],
        )
    
    def _build_slice_mask_directory_path(self, case_directory_path: str) -> str:
        return f'{case_directory_path}/{self._configuration["directory_name"]["slice_mask"]}'

    def _build_case_directory_path_sequence(self) -> StrSequence:
        return path_utils.list_subdirectory(
            self._configuration['dataset_directory_path'])