"""Main Page Callback Plugin of App Factory.

This module contains the implementation of App Factory
Plugins. They adds callbacks triggered in Main Page.

Created by: Weixun Luo
Date: 25/04/2023
"""
from __future__ import annotations

import dash
from dash import exceptions
import dash_vtk
import numpy as np

from application import id
from application import keyboard_event
from object import record
from presentation_layer.app_factory_plugin.layout import menu
from utils import format_utils
from utils import image_processing_utils
from utils import widget_utils


class MainMenuSectionCallbackPlugin:
    """Plugin that adds callbacks triggered in Main Menu Section."""

    def _add_main_menu_section_callback(self) -> None:
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'main_menu_section',
                function_name = 'select_main_menu',
            ),
            dash.Output(id.transformation_menu_id, 'style'),
            dash.Output(id.body_menu_id, 'style'),
            dash.Output(id.organ_menu_id, 'style'),
            dash.Output(id.slice_menu_id, 'style'),
            dash.Input(id.main_menu_selection_dropdown_id, 'value'),
            prevent_initial_call = True,
        )

class EvaluationSectionCallbackPlugin:
    """Plugin that adds callbacks triggered in Evaluation Section."""

    def _add_evaluation_section_callback(self) -> None:
        @dash.callback(
            dash.Output(id.evaluation_result_label_id, 'children'),
            dash.State(id.slice_selection_dropdown_id, 'value'),
            dash.Input(id.evaluation_metric_selection_dropdown_id, 'value'),
            prevent_initial_call = True,
        )
        def evaluate(slice_id: str, evaluation_metric_name: str) -> str:
            try:
                evaluation_output, is_evaluation_output_optimal = self._evaluate(
                    slice_id, evaluation_metric_name)
                self._assign_optimal_transformation(
                    slice_id, is_evaluation_output_optimal)
                evaluation_output = format_utils.format_number(
                    evaluation_output)
                return evaluation_output
            except:
                raise exceptions.PreventUpdate

        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'evaluation_section',
                function_name = 'control_evaluation_result_visibility',
            ),
            dash.Output(id.evaluation_result_label_id, 'style'),
            dash.Input(id.evaluation_result_visibility_switch_id, 'value'),
            prevent_initial_call = True,
        )

    def _evaluate(
        self, slice_id: str, evaluation_metric_name: str) -> tuple[float, bool]:
        return self._evaluation_processing_unit.evaluate(
            slice_id = slice_id,
            evaluation_metric_name = evaluation_metric_name,
            **self._get_evaluate_kwargs(slice_id),
        )
    
    def _get_evaluate_kwargs(self, slice_id: str) -> dict[str, np.ndarray]:
        evaluation_mask = self._masking_processing_unit.build_evaluation_mask(
            **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id))
        evaluate_kwargs = self._data_accessor.get_evaluate_kwargs(slice_id)
        evaluate_kwargs = {
            argument: image_processing_utils.mask(pixel_data, evaluation_mask)
            for argument, pixel_data in evaluate_kwargs.items()
        }
        return evaluate_kwargs
    
    def _assign_optimal_transformation(
        self, slice_id: str, is_evaluation_output_optimal: bool) -> None:
        if is_evaluation_output_optimal:
            self._transformation_processing_unit.assign_optimal_transformation(
                slice_id)

class SupportMenuSectionCallbackPlugin:
    """Plugin that adds callbacks triggered in Support Menu Section."""

    def _add_support_menu_section_callback(self) -> None:
        @dash.callback(
            {
                'option':
                    dash.Output(id.support_menu_selection_dropdown_id, 'options'),
                'value':
                    dash.Output(id.support_menu_selection_dropdown_id, 'value'),
                'visibility':
                    dash.Output(id.support_menu_section_id, 'style'),
            },
            {
                'mask_format_sequence': (
                    dash.Input(id.main_graph_mask_format_selection_dropdown_id, 'value'),
                    dash.Input(id.support_graph_mask_format_selection_dropdown_id, 'value'),
                ),
                'image_type':
                    dash.Input(id.support_graph_image_type_selection_dropdown_id, 'value'),
            },
        )
        def refresh_support_menu_selection_dropdown(
            mask_format_sequence: tuple[str, str], image_type: str) -> dict:
            try:
                support_menu_selection_dropdown_option = self._build_support_menu_selection_dropdown_option(
                    mask_format_sequence, image_type)
                return {
                    'option': support_menu_selection_dropdown_option,
                    'value': next(iter(support_menu_selection_dropdown_option.keys())),
                    'visibility': None,
                }
            except:
                return {
                    'option': dash.no_update,
                    'value': dash.no_update,
                    'visibility': {'display':'none'},
                }

        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'support_menu_section',
                function_name = 'select_support_menu',
            ),
            dash.Output(id.contour_menu_id, 'style'),
            dash.Output(id.checkerboard_menu_id, 'style'),
            dash.Input(id.support_menu_selection_dropdown_id, 'value'),
            prevent_initial_call = True,
        )

    def _build_support_menu_selection_dropdown_option(
        self,
        mask_format_sequence: tuple[str, str], 
        image_type: str,
    ) -> dict[str, str]:
        support_menu_selection_dropdown_option = {}
        if id.contour_id in mask_format_sequence:
            support_menu_selection_dropdown_option[
                id.contour_menu_id] = menu.CONTOUR_MENU_OPTION_TAG,
        if id.checkerboard_id == image_type:
            support_menu_selection_dropdown_option[
                id.checkerboard_menu_id] = menu.CHECKERBOARD_MENU_OPTION_TAG
        return support_menu_selection_dropdown_option

class CameraSectionCallbackPlugin:
    """Plugin that adds callbacks triggered in Camera Section."""

    def _add_camera_section_callback(self) -> None:
        @dash.callback(
            {
                'camera_property': {
                    'position':
                        dash.Output(id.plot_3d_view_id, 'cameraPosition'),
                    'view_up':
                        dash.Output(id.plot_3d_view_id, 'cameraViewUp'),
                },
            },
            dash.Input(id.camera_view_positive_x_outline_button_id, 'n_clicks'),
            dash.Input(id.camera_view_negative_x_outline_button_id, 'n_clicks'),
            dash.Input(id.camera_view_positive_y_outline_button_id, 'n_clicks'),
            dash.Input(id.camera_view_negative_y_outline_button_id, 'n_clicks'),
            dash.Input(id.camera_view_positive_z_outline_button_id, 'n_clicks'),
            dash.Input(id.camera_view_negative_z_outline_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )
        def control_camera_property(*_: tuple[int, ...]) -> dict:
            return {'camera_property':self._control_camera_property()}

    def _control_camera_property(self) -> record.CameraProperty:
        camera_property = self._visualisation_processing_unit.camera_property_map[
            self._select_camera_view()]
        camera_property['position'] = self._format_camera_position(
            camera_property['position'])
        return camera_property

    def _select_camera_view(self) -> str:
        match dash.callback_context.triggered_id:
            case id.camera_view_positive_x_outline_button_id:
                return '+x'
            case id.camera_view_negative_x_outline_button_id:
                return '-x'
            case id.camera_view_positive_y_outline_button_id:
                return '+y'
            case id.camera_view_negative_y_outline_button_id:
                return '-y'
            case id.camera_view_positive_z_outline_button_id:
                return '+z'
            case id.camera_view_negative_z_outline_button_id:
                return '-z'
    
    def _format_camera_position(
        self, camera_position: tuple[int, int, int]) -> tuple[float, int, int]:
        noise = np.random.uniform(-1e-9, 1e-9)  # This can ensure the same view can be selected repeatedly
        return (camera_position[0]+noise, camera_position[1], camera_position[2])

class CaseSectionCallbackPlugin:
    """Plugin that adds callbacks triggered in Case Section."""
    
    def _add_case_section_callback(self) -> None:
        @dash.callback(
            {
                'case_id_previous': 
                    dash.Output(id.case_selection_dropdown_id, 'value', allow_duplicate=True),
                'open_shift_previous_case_failure_error_modal':
                    dash.Output(id.shift_previous_case_failure_error_modal_id, 'is_open'),
            },
            dash.Input(id.shift_previous_case_outline_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )
        def shift_previous_case(_: int) -> dict:
            try:
                return {
                    'case_id_previous': self._shift_previous_case(),
                    'open_shift_previous_case_failure_error_modal': False,
                }
            except IndexError:
                return {
                    'case_id_previous': dash.no_update,
                    'open_shift_previous_case_failure_error_modal': True,
                }

        # Close Shift Previous Case Failure Error Modal
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'close_modal',
            ),
            dash.Output(id.shift_previous_case_failure_error_modal_id, 'is_open', allow_duplicate=True),
            dash.Input(id.close_shift_previous_case_failure_error_modal_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )

        @dash.callback(
            {
                'case_id_next':
                    dash.Output(id.case_selection_dropdown_id, 'value', allow_duplicate=True),
                'open_shift_next_case_failure_error_modal':
                    dash.Output(id.shift_next_case_failure_error_modal_id, 'is_open'),
            },
            dash.Input(id.shift_next_case_outline_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )
        def shift_next_case(_: int) -> tuple[str, bool]:
            try:
                return {
                    'case_id_next': self._shift_next_case(),
                    'open_shift_next_case_failure_error_modal': False,
                }
            except IndexError:
                return {
                    'case_id_next': dash.no_update,
                    'open_shift_next_case_failure_error_modal': True,
                }

        # Close Shift Next Case Failure Error Modal
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'close_modal',
            ),
            dash.Output(id.shift_next_case_failure_error_modal_id, 'is_open', allow_duplicate=True),
            dash.Input(id.close_shift_next_case_failure_error_modal_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )

        @dash.callback(
            {
                'main_menu_selection_dropdown_value':
                    dash.Output(id.main_menu_selection_dropdown_id, 'value'),
                'body_resampled_window_level_slider_kwargs': {
                    'value': dash.Output(id.body_resampled_window_level_slider_id, 'value'),
                    'min': dash.Output(id.body_resampled_window_level_slider_id, 'min'),
                    'max': dash.Output(id.body_resampled_window_level_slider_id, 'max'),
                },
                'body_resampled_window_width_slider_kwargs': {
                    'value': dash.Output(id.body_resampled_window_width_slider_id, 'value'),
                    'min': dash.Output(id.body_resampled_window_width_slider_id, 'min'),
                    'max': dash.Output(id.body_resampled_window_width_slider_id, 'max'),
                },
                'organ_resampled_threshold_slider_value':
                    dash.Output(id.organ_resampled_threshold_slider_id, 'value'),
                'organ_resampled_opacity_slider_value':
                    dash.Output(id.organ_resampled_opacity_slider_id, 'value'),
                'slice_window_level_slider_kwargs': {
                    'value': dash.Output(id.slice_window_level_slider_id, 'value'),
                    'min': dash.Output(id.slice_window_level_slider_id, 'min'),
                    'max': dash.Output(id.slice_window_level_slider_id, 'max'),
                },
                'slice_window_width_slider_kwargs': {
                    'value': dash.Output(id.slice_window_width_slider_id, 'value'),
                    'min': dash.Output(id.slice_window_width_slider_id, 'min'),
                    'max': dash.Output(id.slice_window_width_slider_id, 'max'),
                },
                'slice_opacity_slider_value':
                    dash.Output(id.slice_opacity_slider_id, 'value'),
                'evaluation_metric_selection_dropdown_kwargs': {
                    'option': dash.Output(id.evaluation_metric_selection_dropdown_id, 'options'),
                    'value': dash.Output(id.evaluation_metric_selection_dropdown_id, 'value'),
                },
                'contour_line_width_slider_value':
                    dash.Output(id.contour_line_width_slider_id, 'value'),
                'checkerboard_board_width_slider_value':
                    dash.Output(id.checkerboard_board_width_slider_id, 'value'),
                'plot_3d_view_children':
                    dash.Output(id.plot_3d_view_id, 'children'),
                'camera_view_positive_z_outline_button_n_clicks':
                    dash.Output(id.camera_view_positive_z_outline_button_id, 'n_clicks'),
                'slice_selection_dropdown_kwargs': {
                    'option': dash.Output(id.slice_selection_dropdown_id, 'options'),
                    'value': dash.Output(id.slice_selection_dropdown_id, 'value'),
                },
                'keyboard_event':
                    dash.Output(id.keyboard_id, 'event'),
            },
            dash.Input(id.case_selection_dropdown_id, 'value'),
            prevent_initial_call = True,
        )
        def shift_case(case_id: str) -> dict:
            try:
                self._save_case()
            except:
                pass
            finally:
                self._shift_case(case_id)
                self._set_up()
                return {
                    'main_menu_selection_dropdown_value':
                        id.transformation_menu_id,
                    'body_resampled_window_level_slider_kwargs':
                        self._build_body_resampled_window_level_slider_kwargs(),
                    'body_resampled_window_width_slider_kwargs':
                        self._build_body_resampled_window_width_slider_kwargs(),
                    'organ_resampled_threshold_slider_value':
                        self._build_organ_resampled_threshold_slider_value(),
                    'organ_resampled_opacity_slider_value':
                        self._build_organ_resampled_opacity_slider_value(),
                    'slice_window_level_slider_kwargs':
                        self._build_slice_window_level_slider_kwargs(),
                    'slice_window_width_slider_kwargs':
                        self._build_slice_window_width_slider_kwargs(),
                    'slice_opacity_slider_value':
                        self._build_slice_opacity_slider_value(),
                    'evaluation_metric_selection_dropdown_kwargs':
                        self._build_evaluation_metric_selection_dropdown_kwargs(),
                    'contour_line_width_slider_value':
                        self._build_contour_line_width_slider_value(),
                    'checkerboard_board_width_slider_value':
                        self._build_checkerboard_board_width_slider_value(),
                    'plot_3d_view_children':
                        self._build_plot_3d_view_children(),
                    'camera_view_positive_z_outline_button_n_clicks': 0,
                    'slice_selection_dropdown_kwargs':
                        self._build_slice_selection_dropdown_kwargs(),
                    'keyboard_event':
                        keyboard_event.update_backend_keyboard_event,
                }

        @dash.callback(
            {
                'open_save_case_success_information_modal':
                    dash.Output(id.save_case_success_information_modal_id, 'is_open'),
                'open_save_case_failure_error_modal':
                    dash.Output(id.save_case_failure_error_modal_id, 'is_open'),
            },
            dash.Input(id.save_case_outline_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )
        def save_case(_: int) -> tuple[bool, bool]:
            try:
                self._save_case()
                return {
                    'open_save_case_success_information_modal': True,
                    'open_save_case_failure_error_modal': False,
                }
            except:
                return {
                    'open_save_case_success_information_modal': False,
                    'open_save_case_failure_error_modal': True,
                }

        # Close Save Case Success Information Modal
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'close_modal',
            ),
            dash.Output(id.save_case_success_information_modal_id, 'is_open', allow_duplicate=True),
            dash.Input(id.close_save_case_success_information_modal_button_id, 'n_clicks'),
            prevent_initial_call = True
        )

        # Close Save Case Failure Error Modal
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'close_modal',
            ),
            dash.Output(id.save_case_failure_error_modal_id, 'is_open', allow_duplicate=True),
            dash.Input(id.close_save_case_failure_error_modal_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )

    def _shift_previous_case(self) -> str:
        try:
            return self._dataset.shift_previous_case()
        except Exception as exception:
            raise exception

    def _shift_next_case(self) -> str:
        try:
            return self._dataset.shift_next_case()
        except Exception as exception:
            raise exception

    def _save_case(self) -> None:
        self._io_processing_unit.write_transformation_spreadsheet(
            **self._data_accessor.get_write_transformation_spreadsheet_kwargs(),
        )
        self._io_processing_unit.write_organ_resampled_map(
            **self._data_accessor.get_write_organ_resampled_map_kwargs(),
        )

    def _shift_case(self, case_id: str) -> None:
        self._dataset.shift_case(case_id)

    def _set_up(self) -> None:
        self._data_accessor.set_up(
            self._dataset.build_data_accessor_initialiser())
        self._transformation_processing_unit.set_up(
            self._data_accessor.build_transformation_processing_unit_initialiser())
        self._visualisation_processing_unit.set_up(
            self._data_accessor.build_visualisation_processing_unit_initialiser())
        self._resampling_processing_unit.set_up(
            self._data_accessor.build_resampling_processing_unit_initialiser())
        self._evaluation_processing_unit.set_up(
            self._data_accessor.build_evaluation_processing_unit_initialiser())

    def _build_body_resampled_window_level_slider_kwargs(self) -> dict[str, int]:
        body_resampled_property = self._visualisation_processing_unit.body_resampled_property
        return {
            'value': body_resampled_property['window_level'],
            'min': 0,
            'max': 2 * body_resampled_property['window_level'],
        }

    def _build_body_resampled_window_width_slider_kwargs(self) -> dict[str, int]:
        body_resampled_property = self._visualisation_processing_unit.body_resampled_property
        return {
            'value': body_resampled_property['window_width'],
            'min': 0,
            'max': 2 * body_resampled_property['window_width'],
        }

    def _build_organ_resampled_threshold_slider_value(self) -> float:
        return self._visualisation_processing_unit.organ_resampled_property['threshold']

    def _build_organ_resampled_opacity_slider_value(self) -> float:
        return self._visualisation_processing_unit.organ_resampled_property['opacity']

    def _build_slice_window_level_slider_kwargs(self) -> dict[str, int]:
        slice_property = self._visualisation_processing_unit.slice_property
        return {
            'value': slice_property['window_level'],
            'min': 0,
            'max': 2 * slice_property['window_level'],
        }
    
    def _build_slice_window_width_slider_kwargs(self) -> dict[str, int]:
        slice_property = self._visualisation_processing_unit.slice_property
        return {
            'value': slice_property['window_width'],
            'min': 0,
            'max': 2 * slice_property['window_width'],
        }
    
    def _build_slice_opacity_slider_value(self) -> float:
        return self._visualisation_processing_unit.slice_property['opacity']
    
    def _build_evaluation_metric_selection_dropdown_kwargs(self) -> dict:
        evaluation_metric_name_sequence = self._data_accessor.build_evaluation_metric_name_sequence()
        return {
            'option': evaluation_metric_name_sequence,
            'value': evaluation_metric_name_sequence[0],
        }
    
    def _build_contour_line_width_slider_value(self) -> int:
        return self._visualisation_processing_unit.contour_property['line_width']
    
    def _build_checkerboard_board_width_slider_value(self) -> int:
        return self._visualisation_processing_unit.checkerboard_property['board_width']
    
    def _build_plot_3d_view_children(self) -> tuple:
        body_representation = self._build_body_representation(
            property = self._visualisation_processing_unit.body_property,
            **self._data_accessor.get_build_body_representation_kwargs(),
        )
        organ_representation = self._build_organ_representation(
            property = self._visualisation_processing_unit.organ_property,
            **self._data_accessor.get_build_organ_representation_kwargs(),
        )
        slice_representation_sequence = self._build_slice_representation_sequence(
            property = self._visualisation_processing_unit.slice_property,
            **self._data_accessor.get_build_slice_representation_sequence_kwargs(),
        )
        return (
            body_representation,
            organ_representation,
            *slice_representation_sequence,
        )
    
    def _build_body_representation(
        self,
        state: record.State,
        property: record.Body3DProperty,
    ) -> dash_vtk.VolumeRepresentation:
        return widget_utils.build_body_representation(
            id.body_representation_id, id.body_volume_id, state, property)
    
    def _build_organ_representation(
        self,
        state: record.State,
        property: record.Organ3DProperty,
    ) -> dash_vtk.VolumeRepresentation:
        return widget_utils.build_organ_representation(
            id.organ_representation_id, id.organ_volume_id, state, property)
    
    def _build_slice_representation_sequence(
        self,
        state_map: dict[str, record.State],
        property: record.Slice2DProperty,
    ) -> tuple[dash_vtk.SliceRepresentation, ...]:
        return tuple(
            widget_utils.build_slice_representation(
                widget_utils.build_matchable_id(slice_id, id.slice_representation_type),
                widget_utils.build_matchable_id(slice_id, id.slice_volume_type),
                state,
                property,
            )
            for slice_id, state in state_map.items()
        )
    
    def _build_slice_selection_dropdown_kwargs(self) -> dict:
        return self._data_accessor.get_slice_selection_dropdown_kwargs()

class MainPlot2DSectionCallbackPlugin:
    """Plugin that adds callbacks triggered in Main Plot 2D Section."""

    def _add_main_plot_2d_section_callback(self) -> None:
        @dash.callback(
            dash.Output(id.main_graph_main_figure_data_store_id, 'data'),
            {
                'slice_id':
                    dash.State(id.slice_selection_dropdown_id, 'value'),
                'window': (
                    dash.Input(id.slice_window_level_slider_id, 'value'),
                    dash.Input(id.slice_window_width_slider_id, 'value'),
                ),
                'modified_timestamp':
                    dash.Input(id.main_graph_main_figure_data_store_id, 'modified_timestamp'),
            },
            prevent_initial_call = True,
        )
        def refresh_main_graph_main_figure_data(
            slice_id: str,
            window: tuple[int, int],
            modified_timestamp: int,
        ) -> str:
            return self._plotting_processing_unit.build_slice_image(
                **self._get_build_slice_image_kwargs(slice_id, window),
            )

        @dash.callback(
            dash.Output(id.main_graph_support_figure_data_store_id, 'data'),
            {
                'slice_id':
                    dash.State(id.slice_selection_dropdown_id, 'value'),
                'mask_type':
                    dash.Input(id.main_graph_mask_type_selection_dropdown_id, 'value'),
                'mask_format':
                    dash.Input(id.main_graph_mask_format_selection_dropdown_id, 'value'),
                'threshold':
                    dash.Input(id.organ_resampled_threshold_slider_id, 'value'),
                'opacity':
                    dash.Input(id.organ_resampled_opacity_slider_id, 'value'),
                'modified_timestamp':
                    dash.Input(id.main_graph_support_figure_data_store_id, 'modified_timestamp')
            },
            prevent_initial_call = True,
        )
        def refresh_main_graph_support_figure_data(
            slice_id: str,
            mask_type: str,
            mask_format: str,
            threshold: float,
            opacity: float,
            modified_timestamp: int,
        ) -> str:
            match mask_type, mask_format:
                case id.organ_resampled_mask_id, id.contour_id:
                    return self._plotting_processing_unit.build_organ_resampled_contour(
                        **self._get_build_organ_resampled_contour_kwargs(slice_id, threshold),
                    )
                case id.organ_resampled_mask_id, id.mask_id:
                    return self._plotting_processing_unit.build_organ_resampled_mask(
                        **self._get_build_organ_resampled_mask_kwargs(slice_id, threshold, opacity),
                    )
                case id.evaluation_mask_id, id.contour_id:
                    return self._plotting_processing_unit.build_evaluation_mask_contour(
                        **self._get_build_evaluation_mask_contour_kwargs(slice_id),
                    )
                case id.evaluation_mask_id, id.mask_id:
                    return self._plotting_processing_unit.build_evaluation_mask(
                        **self._get_build_evaluation_mask_kwargs(slice_id, opacity),
                    )
                case id.none_mask_id, _:
                    return ''

        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'main_plot_2d_section',
                function_name = 'refresh_main_graph',
            ),
            dash.Output(id.main_graph_id, 'figure'),
            dash.Input(id.main_graph_main_figure_data_store_id, 'data'),
            dash.Input(id.main_graph_support_figure_data_store_id, 'data'),
            dash.Input(id.contour_line_width_slider_id, 'value'),
            dash.State(id.main_graph_mask_type_selection_dropdown_id, 'value'),
            dash.State(id.main_graph_mask_format_selection_dropdown_id, 'value'),
        )

    def _get_build_slice_image_kwargs(
        self, slice_id: str, window: tuple[int, int]) -> dict:
        evaluation_mask = self._masking_processing_unit.build_evaluation_mask(
            **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id))
        slice_image_kwargs = self._data_accessor.get_build_slice_image_kwargs(
            slice_id)
        slice_image_kwargs['pixel_data'] = image_processing_utils.mask(
            slice_image_kwargs['pixel_data'], evaluation_mask)
        slice_image_kwargs['window'] = window
        return slice_image_kwargs

    def _get_build_organ_resampled_contour_kwargs(
        self, slice_id: str, threshold: float) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_organ_resampled_mask(
                threshold = threshold,
                **self._data_accessor.get_build_organ_resampled_mask_kwargs(slice_id),
            ),
        }

    def _get_build_organ_resampled_mask_kwargs(
        self, slice_id: str, threshold: float, opacity: float) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_organ_resampled_mask(
                threshold = threshold,
                **self._data_accessor.get_build_organ_resampled_mask_kwargs(slice_id),
            ),
            'opacity': opacity,
        }
    
    def _get_build_evaluation_mask_contour_kwargs(self, slice_id: str) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_evaluation_mask(
                **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id)
            ),
        }
    
    def _get_build_evaluation_mask_kwargs(
        self, slice_id: str, opacity: float) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_evaluation_mask(
                **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id)
            ),
            'opacity': opacity,
        }

class SupportPlot2DSectionCallbackPlugin:
    """Plugin that adds callbacks triggered in Support Plot 2D Section."""

    def _add_support_plot_2d_section_callback(self) -> None:
        @dash.callback(
            dash.Output(id.support_graph_main_figure_data_store_id, 'data'),
            {
                'slice_id':
                    dash.State(id.slice_selection_dropdown_id, 'value'),
                'image_type':
                    dash.Input(id.support_graph_image_type_selection_dropdown_id, 'value'),
                'slice_window': (
                    dash.Input(id.slice_window_level_slider_id, 'value'),
                    dash.Input(id.slice_window_width_slider_id, 'value'),
                ),
                'body_resampled_window': (
                    dash.Input(id.body_resampled_window_level_slider_id, 'value'),
                    dash.Input(id.body_resampled_window_width_slider_id, 'value'),
                ),
                'checkerboard_board_width': 
                    dash.Input(id.checkerboard_board_width_slider_id, 'value'),
                'modified_timestamp':
                    dash.Input(id.support_graph_main_figure_data_store_id, 'modified_timestamp'),
            },
            prevent_initial_call = True,
        )
        def refresh_support_graph_main_figure_data(
            slice_id: str,
            image_type: str,
            slice_window: tuple[int, int],
            body_resampled_window: tuple[int, int],
            checkerboard_board_width: int,
            modified_timestamp: int,
        ) -> str:
            match image_type:
                case id.body_resampled_image_id:
                    return self._plotting_processing_unit.build_body_resampled_image(
                        **self._get_build_body_resampled_image_kwargs(slice_id, body_resampled_window),
                    )
                case id.checkerboard_id:
                    return self._plotting_processing_unit.build_slice_body_resampled_checkerboard(
                        **self._get_build_slice_body_resampled_checkerboard_kwargs(
                            slice_id,
                            slice_window,
                            body_resampled_window,
                            checkerboard_board_width,
                        ),
                    )

        @dash.callback(
            dash.Output(id.support_graph_support_figure_data_store_id, 'data'),
            {
                'slice_id':
                    dash.State(id.slice_selection_dropdown_id, 'value'),
                'mask_type':
                    dash.Input(id.support_graph_mask_type_selection_dropdown_id, 'value'),
                'mask_format':
                    dash.Input(id.support_graph_mask_format_selection_dropdown_id, 'value'),
                'threshold':
                    dash.Input(id.organ_resampled_threshold_slider_id, 'value'),
                'opacity':
                    dash.Input(id.organ_resampled_opacity_slider_id, 'value'),
                'modified_timestamp':
                    dash.Input(id.support_graph_support_figure_data_store_id, 'modified_timestamp')
            },
            prevent_initial_call = True,
        )
        def refresh_support_graph_support_figure_data(
            slice_id: str,
            mask_type: str,
            mask_format: str,
            threshold: float,
            opacity: float,
            modified_timestamp: int,
        ) -> str:
            match mask_type, mask_format:
                case id.organ_resampled_mask_id, id.contour_id:
                    return self._plotting_processing_unit.build_organ_resampled_contour(
                        **self._get_build_organ_resampled_contour_kwargs(slice_id, threshold),
                    )
                case id.organ_resampled_mask_id, id.mask_id:
                    return self._plotting_processing_unit.build_organ_resampled_mask(
                        **self._get_build_organ_resampled_mask_kwargs(slice_id, threshold, opacity),
                    )
                case id.evaluation_mask_id, id.contour_id:
                    return self._plotting_processing_unit.build_evaluation_mask_contour(
                        **self._get_build_evaluation_mask_contour_kwargs(slice_id),
                    )
                case id.evaluation_mask_id, id.mask_id:
                    return self._plotting_processing_unit.build_evaluation_mask(
                        **self._get_build_evaluation_mask_kwargs(slice_id, opacity),
                    )
                case id.none_mask_id, _:
                    return ''

        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'support_plot_2d_section',
                function_name = 'refresh_support_graph',
            ),
            dash.Output(id.support_graph_id, 'figure'),
            dash.Input(id.support_graph_main_figure_data_store_id, 'data'),
            dash.Input(id.support_graph_support_figure_data_store_id, 'data'),
            dash.Input(id.contour_line_width_slider_id, 'value'),
            dash.State(id.support_graph_mask_type_selection_dropdown_id, 'value'),
            dash.State(id.support_graph_mask_format_selection_dropdown_id, 'value'),
        )

    def _get_build_body_resampled_image_kwargs(
        self, slice_id: str, window: tuple[int, int]) -> dict:
        evaluation_mask = self._masking_processing_unit.build_evaluation_mask(
            **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id))
        body_resampled_image_kwargs = self._data_accessor.get_build_body_resampled_image_kwargs(slice_id)
        body_resampled_image_kwargs['pixel_data'] = image_processing_utils.mask(
            body_resampled_image_kwargs['pixel_data'], evaluation_mask)
        body_resampled_image_kwargs['window'] = window
        return body_resampled_image_kwargs
    
    def _get_build_slice_body_resampled_checkerboard_kwargs(
        self,
        slice_id: str,
        slice_window: tuple[int, int],
        body_resampled_window: tuple[int, int],
        checkerboard_board_width: int,
    ) -> dict:
        evaluation_mask = self._masking_processing_unit.build_evaluation_mask(
            **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id))
        slice_body_resampled_checkerboard_kwargs = self._data_accessor.get_build_slice_body_resampled_checkerboard_kwargs(slice_id)
        slice_body_resampled_checkerboard_kwargs['pixel_data_pair'] = tuple(
            image_processing_utils.mask(pixel_data, evaluation_mask)
            for pixel_data
            in slice_body_resampled_checkerboard_kwargs['pixel_data_pair']
        )
        slice_body_resampled_checkerboard_kwargs['window_pair'] = (
            slice_window, body_resampled_window)
        slice_body_resampled_checkerboard_kwargs['board_width'] = checkerboard_board_width
        return slice_body_resampled_checkerboard_kwargs

    # The following functions are repeated to ensure each plugin is independent.
    def _get_build_organ_resampled_contour_kwargs(
        self, slice_id: str, threshold: float) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_organ_resampled_mask(
                threshold = threshold,
                **self._data_accessor.get_build_organ_resampled_mask_kwargs(slice_id),
            ),
        }

    def _get_build_organ_resampled_mask_kwargs(
        self, slice_id: str, threshold: float, opacity: float) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_organ_resampled_mask(
                threshold = threshold,
                **self._data_accessor.get_build_organ_resampled_mask_kwargs(slice_id),
            ),
            'opacity': opacity,
        }
    
    def _get_build_evaluation_mask_contour_kwargs(self, slice_id: str) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_evaluation_mask(
                **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id)
            ),
        }
    
    def _get_build_evaluation_mask_kwargs(
        self, slice_id: str, opacity: float) -> dict:
        return {
            'pixel_data': self._masking_processing_unit.build_evaluation_mask(
                **self._data_accessor.get_build_evaluation_mask_kwargs(slice_id)
            ),
            'opacity': opacity,
        }


class MainPageCallbackPlugin(
    MainMenuSectionCallbackPlugin,
    EvaluationSectionCallbackPlugin,
    SupportMenuSectionCallbackPlugin,
    CameraSectionCallbackPlugin,
    CaseSectionCallbackPlugin,
    MainPlot2DSectionCallbackPlugin,
    SupportPlot2DSectionCallbackPlugin,
):
    """Plugin that adds callbacks triggered in Main Page."""

    def _add_main_page_callback(self) -> None:
        self._add_main_menu_section_callback()
        self._add_evaluation_section_callback()
        self._add_support_menu_section_callback()
        self._add_camera_section_callback()
        self._add_case_section_callback()
        self._add_main_plot_2d_section_callback()
        self._add_support_plot_2d_section_callback()