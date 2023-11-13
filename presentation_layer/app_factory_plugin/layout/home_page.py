"""Home Page Plugin of App Factory.

This module contains the implementation of App Factory
Plugin. It defines the layout and structure of Home Page.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from application import id
from utils import io_utils
from utils import widget_utils


TITLE_CHILDREN = 'SVRDA: Dataset Annotation Tool for SVR'
CONFIGURATION_FILE_UPLOAD_CHILDREN = 'Please drag and drop your configuration file, or click here to select files.'
INVALID_CONFIGURATION_FILE_ERROR_MODAL_CHILDREN = (
    f'Invalid configuration file. '
    f'Please check the example in the documentation and try again.'
)


class HomePagePlugin:
    """Plugin that defines the layout of Home Page."""
    
    def _build_home_page(self, configuration_file_path: str | None) -> dbc.Card:
        return dbc.Card(
            id = id.home_page_id,
            children = dbc.CardBody(
                dbc.Row(
                    children = dbc.Col(
                        children = (
                            dbc.Row(style={'height':'30%'}),
                            dbc.Row(
                                children = self._build_title(),
                                align = 'center',
                            ),
                            dbc.Row(style={'height':'20%'}),
                            dbc.Row(
                                children = self._build_configuration_file_upload(),
                                style = {'height':'20%'},
                                align = 'center',
                            ),
                            dbc.Row(style={'height':'10%'}),
                            dbc.Row(self._build_configuration_store(configuration_file_path)),
                            dbc.Row(self._build_invalid_configuration_file_error_modal()),
                        ),
                        width = {'size':8, 'offset':2},
                    ),
                    style = {'height':'100%'},
                ),
            ),
            class_name = 'page',
            style = {'display':'none'},
        )
    
    def _build_title(self) -> html.H1:
        return html.H1(
            id = id.title_id,
            children = TITLE_CHILDREN,
            className = 'text_centred_label',
        )
    
    def _build_configuration_file_upload(self) -> dcc.Upload:
        return dcc.Upload(
            id = id.configuration_file_upload_id, 
            children = CONFIGURATION_FILE_UPLOAD_CHILDREN,
        )
    
    def _build_configuration_store(
        self, configuration_file_path: str | None) -> dcc.Store:
        try:
            return widget_utils.build_store(
                id = id.configuration_store_id,
                data = io_utils.read_file(configuration_file_path),
            )
        except:
            return widget_utils.build_store(id.configuration_store_id)
    
    def _build_invalid_configuration_file_error_modal(self) -> dbc.Modal:
        return widget_utils.build_error_modal(
            modal_id = id.invalid_configuration_file_error_modal_id,
            close_button_id = id.close_invalid_configuration_file_error_modal_button_id,
            children = INVALID_CONFIGURATION_FILE_ERROR_MODAL_CHILDREN,
        )
