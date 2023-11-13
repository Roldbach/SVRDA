"""App Factory.

This module contains the implementation of App Factory used
in the application. App Factory can build the layout of the
application and add callbacks to it.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations

import dash_bootstrap_components as dbc

from application import id
from business_layer import evaluation_processing_unit
from business_layer import io_processing_unit
from business_layer import masking_processing_unit
from business_layer import plotting_processing_unit
from business_layer import resampling_processing_unit
from business_layer import transformation_processing_unit
from business_layer import visualisation_processing_unit
from database_layer import dataset
from persistence_layer import data_accessor
from presentation_layer.app_factory_plugin.callback import basic_callback
from presentation_layer.app_factory_plugin.callback import home_page_callback
from presentation_layer.app_factory_plugin.callback import main_page_callback
from presentation_layer.app_factory_plugin.callback import menu_callback
from presentation_layer.app_factory_plugin.layout import basic
from presentation_layer.app_factory_plugin.layout import home_page
from presentation_layer.app_factory_plugin.layout import main_page
from utils import widget_utils


class AppFactory(
    basic.PageSelectionSectionPlugin,
    home_page.HomePagePlugin,
    main_page.MainPagePlugin,
    basic_callback.BasicCallbackPlugin,
    home_page_callback.HomePageCallbackPlugin,
    main_page_callback.MainPageCallbackPlugin,
    menu_callback.MenuCallbackPlugin,
):
    """App Factory.

    An object that can build the layout of the application
    and add callbacks to it.
    """
    
    def __init__(self) -> None:
        self._transformation_processing_unit = transformation_processing_unit.TransformationProcessingUnit()
        self._visualisation_processing_unit = visualisation_processing_unit.VisualisationProcessingUnit()
        self._resampling_processing_unit = resampling_processing_unit.ResamplingProcessingUnit()
        self._masking_processing_unit = masking_processing_unit.MaskingProcessingUnit()
        self._plotting_processing_unit = plotting_processing_unit.PlottingProcessingUnit()
        self._evaluation_processing_unit = evaluation_processing_unit.EvaluationProcessingUnit()
        self._io_processing_unit = io_processing_unit.IOProcessingUnit()
        self._data_accessor = data_accessor.DataAccessor()
        self._dataset = dataset.Dataset()

    def build_app_layout(
        self, configuration_file_path: str | None) -> dbc.Container:
        return dbc.Container(
            children = (
                self._build_page_selection_section(),
                self._build_home_page(configuration_file_path),
                self._build_main_page(),
                widget_utils.build_keyboard_listener(id.keyboard_id),
            ),
            fluid = True,
        )

    def add_callback(self) -> None:
        self._add_basic_callback()
        self._add_home_page_callback()
        self._add_main_page_callback()
        self._add_menu_callback()