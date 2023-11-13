"""Dataset.

This module contains the implementation of Dataset used in
the application. It is based on a spreadsheet that contains
corresponding paths of all data and offers convenient case
management through case ID.

Created by: Weixun Luo
Date: 08/04/2023
"""
from __future__ import annotations

import pandas as pd

from object import record
from object import spreadsheet_builder


class Dataset:
    """Dataset.
    
    An object used in the application, which contains all
    paths of data and offers convenient case management
    through case ID.
    """

    def __init__(self) -> None:
        self.case_id_sequence = None
        self._dataset_spreadsheet = None
        self._case_pointer = None
    
    def start_up(self, configuration: record.Configuration) -> None:
        dataset_spreadsheet = self._construct_dataset_spreadsheet(configuration)
        self.case_id_sequence = self._construct_case_id_sequence(
            dataset_spreadsheet)
        self._dataset_spreadsheet = dataset_spreadsheet
        self._case_pointer = 0
    
    def _construct_dataset_spreadsheet(
        self, configuration: record.Configuration) -> pd.DataFrame:
        builder = spreadsheet_builder.DatasetSpreadsheetBuilder(configuration)
        dataset_spreadsheet = builder.build_spreadsheet()
        return dataset_spreadsheet

    def _construct_case_id_sequence(
        self, dataset_spreadsheet: pd.DataFrame) -> tuple[str, ...]:
        return tuple(dataset_spreadsheet['case_id'].unique())
    
    def build_data_accessor_initialiser(self) -> record.DataAccessorInitialiser:
        case_id = self.case_id_sequence[self._case_pointer]
        case = self._extract_case(case_id)
        return record.DataAccessorInitialiser(
            case_id = case_id,
            body_file_path = self._extract_body_file_path(case),
            organ_file_path = self._extract_organ_file_path(case),
            organ_resampled_file_path_map = self.
                _extract_organ_resampled_file_path_map(case),
            slice_file_path_map = self._extract_slice_file_path_map(case),
            slice_mask_file_path_map = self.
                _extract_slice_mask_file_path_map(case),
            transformation_spreadsheet_file_path = self.
                _extract_transformation_spreadsheet_file_path(case),
        )
    
    def _extract_case(self, case_id: str) -> pd.DataFrame:
        return self._dataset_spreadsheet.loc[
            self._dataset_spreadsheet['case_id'] == case_id
        ]
    
    def _extract_body_file_path(self, case: pd.DataFrame) -> str:
        return case.iloc[0]['body_file_path']

    def _extract_organ_file_path(self, case: pd.DataFrame) -> str:
        return case.iloc[0]['organ_file_path']
    
    def _extract_organ_resampled_file_path_map(
        self, case: pd.DataFrame) -> dict[str, str]:
        return {
            slice_id: organ_resampled_file_path
            for slice_id, organ_resampled_file_path
            in zip(case['slice_id'], case['organ_resampled_file_path'])
        }
    
    def _extract_slice_file_path_map(
        self, case: pd.DataFrame) -> dict[str, str]:
        return {
            slice_id: slice_file_path
            for slice_id, slice_file_path
            in zip(case['slice_id'], case['slice_file_path'])
        }
    
    def _extract_slice_mask_file_path_map(
        self, case: pd.DataFrame) -> dict[str, str]:
        return {
            slice_id: slice_mask_file_path
            for slice_id, slice_mask_file_path
            in zip(case['slice_id'], case['slice_mask_file_path'])
        }
    
    def _extract_transformation_spreadsheet_file_path(
        self, case: pd.DataFrame) -> str:
        return case.iloc[0]['transformation_spreadsheet_file_path']

    def shift_previous_case(self) -> str:
        if self._case_pointer > 0:
            self._case_pointer -= 1
            return self.case_id_sequence[self._case_pointer]
        else:
            raise IndexError('Cannot access elements with indices less than 0')

    def shift_next_case(self) -> str:
        if self._case_pointer + 1 < len(self.case_id_sequence):
            self._case_pointer += 1
            return self.case_id_sequence[self._case_pointer]
        else:
            raise IndexError(
                'Cannot access elements with indices equal to the length')
    
    def shift_case(self, case_id: str) -> None:
        self._case_pointer = self.case_id_sequence.index(case_id)