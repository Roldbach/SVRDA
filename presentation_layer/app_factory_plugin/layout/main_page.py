"""Main Page Plugin of App Factory.

This module contains the implementation of App Factory
Plugin. It defines the layout and structure of Main Page.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations

from dash import dcc
import dash_bootstrap_components as dbc
import dash_vtk

from application import id
from presentation_layer.app_factory_plugin.layout import menu
from utils import widget_utils


# ----- Main Menu Section -----
MAIN_MENU_SELECTION_DROPDOWN_OPTION = {
    id.transformation_menu_id: 'Transformation',
    id.body_menu_id: '2D Resampled Slice',
    id.organ_menu_id: '2D Segmentation Label',
    id.slice_menu_id: '2D Slice',
}

# ----- Mode Section -----
MODE_SELECTION_INLINE_RADIO_ITEMS_OPTION = {
    id.macro_mode_id: 'Macro Mode',
    id.micro_mode_id: 'Micro Mode',
}
MODE_SELECTION_INLINE_RADIO_ITEMS_VALUE = id.micro_mode_id

# ----- Evaluation Section -----
EVALUATION_RESULT_VISIBILITY_SWITCH_CHILDREN = 'Show'

# ----- Camera Section -----
CAMERA_VIEW_OUTLINE_BUTTON_CHILDREN_MAP = {
    id.camera_view_positive_x_outline_button_id: '+X',
    id.camera_view_negative_x_outline_button_id: '-X',
    id.camera_view_positive_y_outline_button_id: '+Y',
    id.camera_view_negative_y_outline_button_id: '-Y',
    id.camera_view_positive_z_outline_button_id: '+Z',
    id.camera_view_negative_z_outline_button_id: '-Z',
}

# ----- Case Section -----
SHIFT_PREVIOUS_CASE_OUTLINE_BUTTON_CHILDREN = 'Previous'
SHIFT_NEXT_CASE_OUTLINE_BUTTON_CHILDREN = 'Next'
SAVE_CASE_OUTLINE_BUTTON_CHILDREN = 'Save'
CASE_SELECTION_DROPDOWN_DISPLAY_NUMBER = 3
SHIFT_PREVIOUS_CASE_FAILURE_ERROR_MODAL_CHILDREN = (
    f'Cannot shift to the previous case '
    f'as this is the first one in the dataset.'
)
SHIFT_NEXT_CASE_FAILURE_ERROR_MODAL_CHILDREN = (
    f'Cannot shift to the next case '
    f'as this is the last one in the dataset.'
)
SAVE_CASE_SUCCESS_INFORMATION_MODAL_CHILDREN = 'Successfully saved the current case.'
SAVE_CASE_FAILURE_ERROR_MODAL_CHILDREN = (
    f'Failed to save the current case. '
    f'Please contact the administrator for futher help.'
) 

# ----- Main Plot 2D Section -----
MAIN_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_OPTION = {
    id.organ_resampled_mask_id: 'Resampled Label',
    id.evaluation_mask_id: 'Resultant Mask',
    id.none_mask_id: 'None',
}
MAIN_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_VALUE = id.organ_resampled_mask_id
MAIN_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_OPTION = {
    id.mask_id: 'Mask', id.contour_id: 'Contour',
}
MAIN_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_VALUE = id.contour_id

# ----- Support Plot 2D Section -----
SUPPORT_GRAPH_IMAGE_TYPE_SELECTION_DROPDOWN_OPTION = {
    id.body_resampled_image_id: 'Resampled Slice',
    id.checkerboard_id: 'Checkerboard',
}
SUPPORT_GRAPH_IMAGE_TYPE_SELECTION_DROPDOWN_VALUE = id.body_resampled_image_id
SUPPORT_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_OPTION = {
    id.organ_resampled_mask_id: 'Resampled Label',
    id.evaluation_mask_id: 'Resultant Mask',
    id.none_mask_id: 'None',
}
SUPPORT_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_VALUE = id.organ_resampled_mask_id
SUPPORT_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_OPTION = {
    id.mask_id: 'Mask', id.contour_id: 'Contour',
}
SUPPORT_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_VALUE = id.contour_id


class MainMenuSectionPlugin(
    menu.TransformationMenuPlugin,
    menu.BodyMenuPlugin,
    menu.OrganMenuPlugin,
    menu.SliceMenuPlugin,
):
    """Plugin that defines the layout of Main Menu Section."""

    def _build_main_menu_section(self) -> dbc.Card:
        return dbc.Card(
            children = (
                dbc.CardHeader(self._build_main_menu_selection_dropdown()),
                dbc.CardBody(
                    children = (
                        self._build_transformation_menu(),
                        self._build_body_menu(),
                        self._build_organ_menu(),
                        self._build_slice_menu(),
                    ),
                ),
            ),
        )

    def _build_main_menu_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id = id.main_menu_selection_dropdown_id,
            option = MAIN_MENU_SELECTION_DROPDOWN_OPTION,
        )

class ModeSectionPlugin:
    """Plugin that defines the layout of Mode Section."""

    def _build_mode_section(self) -> dbc.Card:
        return dbc.Card(
            children = dbc.CardBody(
                children = dbc.Row(
                    children = self._build_mode_selection_inline_radio_items(),
                    justify = 'center',
                    align = 'center',
                    style = {'height':'100%'},
                ),
            ),
        )
    
    def _build_mode_selection_inline_radio_items(self) -> dbc.RadioItems:
        return widget_utils.build_inline_radio_items(
            id = id.mode_selection_inline_radio_items_id,
            option = MODE_SELECTION_INLINE_RADIO_ITEMS_OPTION,
            value = MODE_SELECTION_INLINE_RADIO_ITEMS_VALUE,
        )

class EvaluationSectionPlugin:
    """Plugin that defines the layout of Evaluation Section."""

    def _build_evaluation_section(self) -> dbc.Card:
        return dbc.Card(
            children = dbc.CardBody(
                children = dbc.Row(
                    children = (
                        dbc.Col(self._build_evaluation_metric_selection_dropdown(), width=4),
                        dbc.Col(self._build_evaluation_result_label(), width=4),
                        dbc.Col(self._build_evaluation_result_visibility_switch(), width=4),
                    ),
                    justify = 'center',
                    align = 'center',
                    style = {'height':'100%'},
                ),
            ),
        )
    
    def _build_evaluation_metric_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id.evaluation_metric_selection_dropdown_id)
    
    def _build_evaluation_result_label(self) -> dbc.Label:
        return widget_utils.build_label(
            id = id.evaluation_result_label_id,
            class_name = 'text_centred_label',
        )
    
    def _build_evaluation_result_visibility_switch(self) -> dbc.Switch:
        return widget_utils.build_switch(
            id = id.evaluation_result_visibility_switch_id,
            children = EVALUATION_RESULT_VISIBILITY_SWITCH_CHILDREN,
        )

class SupportMenuSectionPlugin(
    menu.ContourMenuPlugin,
    menu.CheckerboardMenuPlugin,
):
    """Plugin that defines the layout of Support Menu Section."""

    def _build_support_menu_section(self) -> dbc.Card:
        return dbc.Card(
            id = id.support_menu_section_id,
            children = (
                dbc.CardHeader(self._build_support_menu_selection_dropdown()),
                dbc.CardBody(
                    children = (
                        self._build_contour_menu(),
                        self._build_checkerboard_menu(),
                    ),
                ),
            ),
            style = {'display':'none'},
        )
    
    def _build_support_menu_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id.support_menu_selection_dropdown_id)

class CameraSectionPlugin:
    """Plugin that defines the layout of Camera Section."""

    def _build_camera_section(self) -> dbc.Card:
        return dbc.Card(
            children = dbc.CardBody(
                children = dbc.Row(
                    children = self._build_camera_control_button_group(),
                    justify = 'center',
                    align = 'center',
                    style = {'height':'100%'},
                ),
            ),
        )
    
    def _build_camera_control_button_group(self) -> dbc.ButtonGroup:
        return dbc.ButtonGroup(
            children = tuple(
                widget_utils.build_outline_button(id, children)
                for id, children
                in CAMERA_VIEW_OUTLINE_BUTTON_CHILDREN_MAP.items()
            ),
        )

class Plot3DSectionPlugin:
    """Plugin that defines the layout of Plot 3D Section."""

    def _build_plot_3d_section(self) -> dbc.Card:
        return dbc.Card(self._build_plot_3d_view())
    
    def _build_plot_3d_view(self) -> dash_vtk.View:
        return dash_vtk.View(id=id.plot_3d_view_id, triggerRender=0)

class CaseSectionPlugin:
    """Plugin that defines the layout of Case Section."""

    def _build_case_section(self) -> dbc.Card:
        return dbc.Card(
            children = dbc.CardBody(
                children = (
                    dbc.Row(
                        children = (
                            dbc.Col(self._build_case_control_button_group(), width=8),
                            dbc.Col(self._build_case_selection_dropdown(), width=4)
                        ),
                        justify = 'center',
                        align = 'center',
                        style = {'height':'100%'},
                    ),
                    dbc.Row(
                        children = (
                            self._build_shift_previous_case_failure_error_modal(),
                            self._build_shift_next_case_failure_error_modal(),
                            self._build_save_case_success_information_modal(),
                            self._build_save_case_failure_error_modal(),
                        ),
                    ),
                ),
            ),
        )
    
    def _build_case_control_button_group(self) -> dbc.ButtonGroup:
        return dbc.ButtonGroup(
            children = (
                self._build_shift_previous_case_outline_button(),
                self._build_shift_next_case_outline_button(),
                self._build_save_case_outline_button(),
            ),
        )
    
    def _build_shift_previous_case_outline_button(self) -> dbc.Button:
        return widget_utils.build_outline_button(
            id = id.shift_previous_case_outline_button_id,
            children = SHIFT_PREVIOUS_CASE_OUTLINE_BUTTON_CHILDREN,
        )
    
    def _build_shift_next_case_outline_button(self) -> dbc.Button:
        return widget_utils.build_outline_button(
            id = id.shift_next_case_outline_button_id,
            children = SHIFT_NEXT_CASE_OUTLINE_BUTTON_CHILDREN,
        )
    
    def _build_save_case_outline_button(self) -> dbc.Button:
        return widget_utils.build_outline_button(
            id = id.save_case_outline_button_id,
            children = SAVE_CASE_OUTLINE_BUTTON_CHILDREN,
        )

    def _build_case_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id = id.case_selection_dropdown_id,
            display_number = CASE_SELECTION_DROPDOWN_DISPLAY_NUMBER,
        )
    
    def _build_shift_previous_case_failure_error_modal(self) -> dbc.Modal:
        return widget_utils.build_error_modal(
            modal_id = id.shift_previous_case_failure_error_modal_id,
            close_button_id = id.close_shift_previous_case_failure_error_modal_button_id,
            children = SHIFT_PREVIOUS_CASE_FAILURE_ERROR_MODAL_CHILDREN,
        )
    
    def _build_shift_next_case_failure_error_modal(self) -> dbc.Modal:
        return widget_utils.build_error_modal(
            modal_id = id.shift_next_case_failure_error_modal_id,
            close_button_id = id.close_shift_next_case_failure_error_modal_button_id,
            children = SHIFT_NEXT_CASE_FAILURE_ERROR_MODAL_CHILDREN,
        )

    def _build_save_case_success_information_modal(self) -> dbc.Modal:
        return widget_utils.build_information_modal(
            modal_id = id.save_case_success_information_modal_id,
            close_button_id = id.close_save_case_success_information_modal_button_id,
            children = SAVE_CASE_SUCCESS_INFORMATION_MODAL_CHILDREN,
        )
    
    def _build_save_case_failure_error_modal(self) -> dbc.Modal:
        return widget_utils.build_error_modal(
            modal_id = id.save_case_failure_error_modal_id,
            close_button_id = id.close_save_case_failure_error_modal_button_id,
            children = SAVE_CASE_FAILURE_ERROR_MODAL_CHILDREN,
        )

class MainPlot2DSectionPlugin:
    """Plugin that defines the layout of Main Plot 2D Section."""

    def _build_main_plot_2d_section(self) -> dbc.Card:
        return dbc.Card(
            children = (
                dbc.CardHeader(
                    children = dbc.Row(
                        children = (
                            dbc.Col(self._build_slice_selection_dropdown(), width=4),
                            dbc.Col(self._build_main_graph_mask_type_selection_dropdown(), width=4),
                            dbc.Col(self._build_main_graph_mask_format_selection_dropdown(), width=4),
                            dbc.Col(self._build_main_graph_main_figure_data_store()),
                            dbc.Col(self._build_main_graph_support_figure_data_store()),
                        ),
                    ),
                ),
                dbc.CardBody(
                    children = dbc.Row(
                        children = self._build_main_graph(),
                        justify = 'center',
                        align = 'center',
                        style = {'height':'100%'},
                    ),
                ),
            ),
        )
    
    def _build_slice_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id.slice_selection_dropdown_id)
    
    def _build_main_graph_mask_type_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id = id.main_graph_mask_type_selection_dropdown_id,
            option = MAIN_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_OPTION,
            value = MAIN_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_VALUE,
        )
    
    def _build_main_graph_mask_format_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id = id.main_graph_mask_format_selection_dropdown_id,
            option = MAIN_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_OPTION,
            value = MAIN_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_VALUE,
        )
    
    def _build_main_graph(self) -> dcc.Graph:
        return dcc.Graph(
            id = id.main_graph_id,
            config = {'displayModeBar':False},
            className = 'graph',
        )
    
    def _build_main_graph_main_figure_data_store(self) -> dcc.Store:
        return widget_utils.build_store(id.main_graph_main_figure_data_store_id)
    
    def _build_main_graph_support_figure_data_store(self) -> dcc.Store:
        return widget_utils.build_store(
            id.main_graph_support_figure_data_store_id)

class SupportPlot2DSectionPlugin:
    """Plugin that defines the layout of Support Plot 2D Section."""

    def _build_support_plot_2d_section(self) -> dbc.Card:
        return dbc.Card(
            children = (
                dbc.CardHeader(
                    children = dbc.Row(
                        children = (
                            dbc.Col(self._build_support_graph_image_type_selection_dropdown(), width=4),
                            dbc.Col(self._build_support_graph_mask_type_selection_dropdown(), width=4),
                            dbc.Col(self._build_support_graph_mask_format_selection_dropdown(), width=4),
                            dbc.Col(self._build_support_graph_main_figure_data_store()),
                            dbc.Col(self._build_support_graph_support_figure_data_store()),
                        ),
                    ),
                ),
                dbc.CardBody(
                    children = dbc.Row(
                        children = self._build_support_graph(),
                        justify = 'center',
                        align = 'center',
                        style = {'height':'100%'},
                    ),
                ),
            ),
        ),
    
    def _build_support_graph_image_type_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id = id.support_graph_image_type_selection_dropdown_id,
            option = SUPPORT_GRAPH_IMAGE_TYPE_SELECTION_DROPDOWN_OPTION,
            value = SUPPORT_GRAPH_IMAGE_TYPE_SELECTION_DROPDOWN_VALUE,
        )
    
    def _build_support_graph_mask_type_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id = id.support_graph_mask_type_selection_dropdown_id,
            option = SUPPORT_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_OPTION,
            value = SUPPORT_GRAPH_MASK_TYPE_SELECTION_DROPDOWN_VALUE,
        )
    
    def _build_support_graph_mask_format_selection_dropdown(self) -> dcc.Dropdown:
        return widget_utils.build_dropdown(
            id = id.support_graph_mask_format_selection_dropdown_id,
            option = SUPPORT_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_OPTION,
            value = SUPPORT_GRAPH_MASK_FORMAT_SELECTION_DROPDOWN_VALUE,
        )
    
    def _build_support_graph(self) -> dcc.Graph:
        return dcc.Graph(
            id = id.support_graph_id,
            config = {'displayModeBar':False},
            className = 'graph',
        )
    
    def _build_support_graph_main_figure_data_store(self) -> dcc.Store:
        return widget_utils.build_store(
            id.support_graph_main_figure_data_store_id)
    
    def _build_support_graph_support_figure_data_store(self) -> dcc.Store:
        return widget_utils.build_store(
            id.support_graph_support_figure_data_store_id)


class MainPagePlugin(
    MainMenuSectionPlugin,
    ModeSectionPlugin,
    EvaluationSectionPlugin,
    SupportMenuSectionPlugin,
    CameraSectionPlugin,
    Plot3DSectionPlugin,
    CaseSectionPlugin,
    MainPlot2DSectionPlugin,
    SupportPlot2DSectionPlugin,
):
    """Plugin that defines the layout of Main Page."""

    def _build_main_page(self) -> dbc.Card:
        return dbc.Card(
            id = id.main_page_id,
            children = dbc.CardBody(
                dbc.Row(
                    children = (
                        dbc.Col(
                            children = (
                                dbc.Row(
                                    children = self._build_main_menu_section(),
                                    style = {'height':'45%'},
                                ),
                                dbc.Row(
                                    children = self._build_mode_section(),
                                    style = {'height':'10%'},
                                ),
                                dbc.Row(
                                    children = self._build_evaluation_section(),
                                    style = {'height':'12%'},
                                ),
                                dbc.Row(
                                    children = self._build_support_menu_section(),
                                    style = {'height':'33%'},
                                )
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            children = (
                                dbc.Row(
                                    children = self._build_camera_section(),
                                    style = {'height':'12%'},
                                ),
                                dbc.Row(
                                    children = self._build_plot_3d_section(),
                                    style = {'height':'75%'},
                                ),
                                dbc.Row(
                                    children = self._build_case_section(),
                                    style = {'height':'13%'},
                                )
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            children = (
                                dbc.Row(
                                    children = self._build_main_plot_2d_section(),
                                    style = {'height':'50%'},
                                ),
                                dbc.Row(
                                    children = self._build_support_plot_2d_section(),
                                    style = {'height':'50%'},
                                )
                            ),
                            width = 4,
                        ),
                    ),
                    style = {'height':'100%'}, 
                ),
            ),
            class_name = 'page',
            style = {'display':'none'},
        )
