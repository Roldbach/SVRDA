"""Home Page Callback Plugin of App Factory.

This module contains the implementation of App Factory
Plugin. It adds callbacks triggered in Home Page.

Created by: Weixun Luo
Date: 04/05/2023
"""
from __future__ import annotations
import base64
import orjson
import typing

import dash

from application import id
from object import record


class HomePageCallbackPlugin:
    """Plugin that adds callbacks triggered in Home Page."""

    def _add_home_page_callback(self) -> None:
        @dash.callback(
            {
                'path_name': dash.Output(id.location_id, 'pathname'),
                'case_selection_dropdown_kwargs': {
                    'option': dash.Output(id.case_selection_dropdown_id, 'options'),
                    'value': dash.Output(id.case_selection_dropdown_id, 'value'),
                },
                'open_invalid_configuration_file_error_modal':
                    dash.Output(id.invalid_configuration_file_error_modal_id, 'is_open'),
            },
            {
                'configuration': dash.Input(id.configuration_store_id, 'data'),
                'href_map': {
                    'home_page': dash.State(id.home_page_link_id, 'href'),
                    'main_page': dash.State(id.main_page_link_id, 'href'),
                },
            },
        )
        def start_up(
            configuration: record.Configuration,
            href_map: dict[str, str],
        ) -> dict:
            try:
                self._start_up(configuration)
                return {
                    'path_name': href_map['main_page'],
                    'case_selection_dropdown_kwargs': 
                        self._build_case_selection_dropdown_kwargs(),
                    'open_invalid_configuration_file_error_modal': False,
                }
            except:
                return {
                    'path_name': href_map['home_page'],
                    'case_selection_dropdown_kwargs': {
                        'option': dash.no_update,
                        'value': dash.no_update,
                    },
                    'open_invalid_configuration_file_error_modal': configuration is not None,
                }

        @dash.callback(
            {
                'configuration': dash.Output(id.configuration_store_id, 'data'),
                'open_invalid_configuration_file_error_modal': 
                    dash.Output(id.invalid_configuration_file_error_modal_id, 'is_open', allow_duplicate=True),
                'configuration_file_upload_data':
                    dash.Output(id.configuration_file_upload_id, 'contents'),
            },
            dash.Input(id.configuration_file_upload_id, 'contents'),
            prevent_initial_call = True,
        )
        def upload_configuration(configuration_encoded: str) -> dict:
            try:
                return {
                    'configuration':
                        self._build_configuration(configuration_encoded),
                    'open_invalid_configuration_file_error_modal': False,
                    'configuration_file_upload_data':
                        None,  # Reset this so files can be uploaded repeatedly
                }
            except:
                return {
                    'configuration': dash.no_update,
                    'open_invalid_configuration_file_error_modal': True,
                    'configuration_file_upload_data': None,
                }

        # Close Invalid Configuration File Error Modal
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'close_modal',
            ),
            dash.Output(id.invalid_configuration_file_error_modal_id, 'is_open', allow_duplicate=True),
            dash.Input(id.close_invalid_configuration_file_error_modal_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )
        
    def _start_up(self, configuration: record.Configuration) -> None:
        self._dataset.start_up(configuration)

    def _build_case_selection_dropdown_kwargs(self) -> dict:
        return {
            'option': self._dataset.case_id_sequence,
            'value': self._dataset.case_id_sequence[0],
        }

    def _build_configuration(self, configuration_encoded: str) -> record.Configuration:
        configuration_encoded = self._trim_prefix(configuration_encoded)
        configuration_decoded = self._decode(configuration_encoded)
        configuration = self._parse(configuration_decoded)
        return configuration
    
    def _trim_prefix(self, configuration_encoded: str) -> str:
        return configuration_encoded.split(',')[1]
    
    def _decode(self, configuration_encoded: str) -> bytes:
        return base64.b64decode(configuration_encoded)
    
    def _parse(self, configuration_decoded: bytes) -> typing.Any:
        configuration =  orjson.loads(configuration_decoded)
        return record.Configuration(
            dataset_directory_path = configuration['dataset_directory_path'],
            directory_name = configuration['directory_name'],
            file_name = configuration['file_name'],
            pattern = configuration['pattern'],
            tag = configuration['tag'],
        )  # Soft-check whether the decoded object contains all required fields