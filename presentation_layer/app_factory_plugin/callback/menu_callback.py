"""Menu Callback Plugins of App Factory.

This module contains the implementation of App Factory
Plugins. They add callbacks triggered in all menus used in
the application.

Created by: Weixun Luo
Date: 25/04/2023
"""
from __future__ import annotations

import dash
from dash import exceptions
import numpy as np

from application import id
from application import keyboard_event
from object import record
from utils import format_utils
from utils import image_processing_utils
from utils import widget_utils


class TransformationMenuCallbackPlugin:
    """Plugin that adds callbacks triggered in Transformation Menu."""

    def _add_transformation_menu_callback(self) -> None:
        @dash.callback(
            dash.Output(id.slice_selection_dropdown_id, 'value', allow_duplicate=True),
            {
                'keyboard_kwargs': {
                    'event': dash.Input(id.keyboard_id, 'event'),
                    'n_events': dash.Input(id.keyboard_id, 'n_events'),
                },
                'slice_id':
                    dash.State(id.slice_selection_dropdown_id, 'value'),
                'slice_id_sequence':
                    dash.State(id.slice_selection_dropdown_id, 'options'),
                'mode':
                    dash.State(id.mode_selection_inline_radio_items_id, 'value'),
                'translation_step_size':
                    dash.State(id.translation_step_size_slider_id, 'value'),
                'rotation_step_size':
                    dash.State(id.rotation_step_size_slider_id, 'value'),
            },
            prevent_initial_call = True,
        )
        def control_transformation_by_keyboard(
            keyboard_kwargs: dict,
            slice_id: str,
            slice_id_sequence: tuple[str, ...],
            mode: str,
            translation_step_size: float,
            rotation_step_size: float,
        ) -> str:
            self._control_transformation_by_keyboard(
                keyboard_kwargs['event'],
                slice_id,
                slice_id_sequence,
                mode,
                translation_step_size,
                rotation_step_size,
            )
            self._update_backend(slice_id, slice_id_sequence, mode)
            return slice_id

        @dash.callback(
            dash.Output(id.slice_selection_dropdown_id, 'value', allow_duplicate=True),
            {
                'slice_id':
                    dash.State(id.slice_selection_dropdown_id, 'value'),
                'slice_id_sequence':
                    dash.State(id.slice_selection_dropdown_id, 'options'),
                'mode':
                    dash.State(id.mode_selection_inline_radio_items_id, 'value'),
                'button_n_clicks_sequence': (
                    dash.Input(id.undo_transformation_outline_button_id, 'n_clicks'),
                    dash.Input(id.redo_transformation_outline_button_id, 'n_clicks'),
                    dash.Input(id.optimise_transformation_outline_button_id, 'n_clicks'),
                    dash.Input(id.reset_transformation_outline_button_id, 'n_clicks'),
                ),
            },
            prevent_initial_call = True,
        )
        def control_transformation_by_button(
            slice_id: str,
            slice_id_sequence: tuple[str, ...],
            mode: str,
            button_n_clicks_sequence: tuple[int, ...],
        ) -> str:
            self._control_transformation_by_button(
                slice_id, slice_id_sequence, mode)
            self._update_backend(slice_id, slice_id_sequence, mode)
            return slice_id

        @dash.callback(
            {
                'transformation_parameter': (
                    dash.Output(id.translation_x_label_id, 'children'),
                    dash.Output(id.translation_y_label_id, 'children'),
                    dash.Output(id.translation_z_label_id, 'children'),
                    dash.Output(id.rotation_x_label_id, 'children'),
                    dash.Output(id.rotation_y_label_id, 'children'),
                    dash.Output(id.rotation_z_label_id, 'children'),
                ),
                'evaluation_metric_selection_dropdown_value':
                    dash.Output(id.evaluation_metric_selection_dropdown_id, 'value', allow_duplicate=True),
                'slice_state_sequence':
                    dash.Output(widget_utils.build_matchable_id(dash.ALL, id.slice_volume_type), 'state'),
                'figure_data_store_modified_timestamp_sequence': (
                    dash.Output(id.main_graph_main_figure_data_store_id, 'modified_timestamp'),
                    dash.Output(id.main_graph_support_figure_data_store_id, 'modified_timestamp'),
                    dash.Output(id.support_graph_main_figure_data_store_id, 'modified_timestamp'),
                    dash.Output(id.support_graph_support_figure_data_store_id, 'modified_timestamp'),
                ),
            },
            {
                'slice_id':
                    dash.Input(id.slice_selection_dropdown_id, 'value'),
                'slice_id_sequence':
                    dash.State(id.slice_selection_dropdown_id, 'options'),
                'mode':
                    dash.State(id.mode_selection_inline_radio_items_id, 'value'),
                'evaluation_metric_name':
                    dash.State(id.evaluation_metric_selection_dropdown_id, 'value'),
                'slice_state_sequence':
                    dash.State(widget_utils.build_matchable_id(dash.ALL, id.slice_volume_type), 'state'),
                'figure_data_store_modified_timestamp_sequence': (
                    dash.State(id.main_graph_main_figure_data_store_id, 'modified_timestamp'),
                    dash.State(id.main_graph_support_figure_data_store_id, 'modified_timestamp'),
                    dash.State(id.support_graph_main_figure_data_store_id, 'modified_timestamp'),
                    dash.State(id.support_graph_support_figure_data_store_id, 'modified_timestamp'),
                ),
            },
            prevent_initial_call = True,
        )
        def refresh(
            slice_id: str,
            slice_id_sequence: tuple[str, ...],
            mode: str,
            evaluation_metric_name: str,
            slice_state_sequence: tuple,
            figure_data_store_modified_timestamp_sequence: tuple,
        ) -> dict:
            return {
                'transformation_parameter':
                    self._refresh_transformation_parameter(slice_id),
                'evaluation_metric_selection_dropdown_value':
                    evaluation_metric_name,
                'slice_state_sequence':
                    self._patch_refresh_slice_state_sequence(
                        slice_id, slice_id_sequence, mode, slice_state_sequence),
                'figure_data_store_modified_timestamp_sequence':
                    self._refresh_figure_data_store_modified_timestamp_sequence(
                        figure_data_store_modified_timestamp_sequence),
            }

    def _control_transformation_by_keyboard(
        self,
        event: record.KeyboardEvent,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
        translation_step_size: float,
        rotation_step_size: float,
    ) -> None:
        match event:
            # ----- Scanner Coordinate Translation -----
            case keyboard_event.scanner_coordinate_translate_positive_x_keyboard_event:
                self._scanner_coordinate_translate(slice_id, slice_id_sequence, mode, -1.0*translation_step_size, 'x')
            case keyboard_event.scanner_coordinate_translate_negative_x_keyboard_event:
                self._scanner_coordinate_translate(slice_id, slice_id_sequence, mode, translation_step_size, 'x')
            case keyboard_event.scanner_coordinate_translate_positive_y_keyboard_event:
                self._scanner_coordinate_translate(slice_id, slice_id_sequence, mode, translation_step_size, 'y')
            case keyboard_event.scanner_coordinate_translate_negative_y_keyboard_event:
                self._scanner_coordinate_translate(slice_id, slice_id_sequence, mode, -1.0*translation_step_size, 'y')
            case keyboard_event.scanner_coordinate_translate_positive_z_keyboard_event:
                self._scanner_coordinate_translate(slice_id, slice_id_sequence, mode, translation_step_size, 'z')
            case keyboard_event.scanner_coordinate_translate_negative_z_keyboard_event:
                self._scanner_coordinate_translate(slice_id, slice_id_sequence, mode, -1.0*translation_step_size, 'z')
            
            # ----- Slice Coordinate Translation -----
            case keyboard_event.slice_coordinate_translate_positive_x_keyboard_event:
                self._slice_coordinate_translate(slice_id, slice_id_sequence, mode, -1.0*translation_step_size, 'x')
            case keyboard_event.slice_coordinate_translate_negative_x_keyboard_event:
                self._slice_coordinate_translate(slice_id, slice_id_sequence, mode, translation_step_size, 'x')
            case keyboard_event.slice_coordinate_translate_positive_y_keyboard_event:
                self._slice_coordinate_translate(slice_id, slice_id_sequence, mode, translation_step_size, 'y')
            case keyboard_event.slice_coordinate_translate_negative_y_keyboard_event:
                self._slice_coordinate_translate(slice_id, slice_id_sequence, mode, -1.0*translation_step_size, 'y')
            case keyboard_event.slice_coordinate_translate_positive_z_keyboard_event:
                self._slice_coordinate_translate(slice_id, slice_id_sequence, mode, translation_step_size, 'z')
            case keyboard_event.slice_coordinate_translate_negative_z_keyboard_event:
                self._slice_coordinate_translate(slice_id, slice_id_sequence, mode, -1.0*translation_step_size, 'z')
            
            # ----- Slice Coordinate Rotation -----
            case keyboard_event.slice_coordinate_rotate_clockwise_x_keyboard_event:
                self._slice_coordinate_rotate(slice_id, slice_id_sequence, mode, format_utils.convert_degree_to_radian(-1.0*rotation_step_size), 'x')
            case keyboard_event.slice_coordinate_rotate_anti_clockwise_x_keyboard_event:
                self._slice_coordinate_rotate(slice_id, slice_id_sequence, mode, format_utils.convert_degree_to_radian(rotation_step_size), 'x')
            case keyboard_event.slice_coordinate_rotate_clockwise_y_keyboard_event:
                self._slice_coordinate_rotate(slice_id, slice_id_sequence, mode, format_utils.convert_degree_to_radian(rotation_step_size), 'y')
            case keyboard_event.slice_coordinate_rotate_anti_clockwise_y_keyboard_event:
                self._slice_coordinate_rotate(slice_id, slice_id_sequence, mode, format_utils.convert_degree_to_radian(-1.0*rotation_step_size), 'y')
            case keyboard_event.slice_coordinate_rotate_clockwise_z_keyboard_event:
                self._slice_coordinate_rotate(slice_id, slice_id_sequence, mode, format_utils.convert_degree_to_radian(rotation_step_size), 'z')
            case keyboard_event.slice_coordinate_rotate_anti_clockwise_z_keyboard_event:
                self._slice_coordinate_rotate(slice_id, slice_id_sequence, mode, format_utils.convert_degree_to_radian(-1.0*rotation_step_size), 'z')
            
            case keyboard_event.update_backend_keyboard_event:
                pass
            case _:
                raise exceptions.PreventUpdate
    
    def _scanner_coordinate_translate(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
        step_size: float,
        axis_name: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._scanner_coordinate_translate_macro(
                    slice_id_sequence, step_size, axis_name)
            case id.micro_mode_id:
                self._scanner_coordinate_translate_micro(
                    slice_id, step_size, axis_name)
            case _:
                raise exceptions.PreventUpdate

    def _scanner_coordinate_translate_macro(
        self,
        slice_id_sequence: tuple[str, ...],
        step_size: float,
        axis_name: str,
    ) -> None:
        for slice_id in slice_id_sequence:
            self._scanner_coordinate_translate_micro(
                slice_id, step_size, axis_name)

    def _scanner_coordinate_translate_micro(
        self, slice_id: str, step_size: float, axis_name: str) -> None:
        self._transformation_processing_unit.insert_transformation(
            slice_id,
            self._transformation_processing_unit.translate(
                **self._get_scanner_coordinate_translate_kwargs(
                    slice_id, step_size, axis_name),
            ),
        )
    
    def _get_scanner_coordinate_translate_kwargs(
        self, slice_id: str, step_size: float, axis_name: str) -> dict:
        scanner_coordinate_translate_kwargs = self._data_accessor.get_scanner_coordinate_translate_kwargs(axis_name)
        scanner_coordinate_translate_kwargs['transformation_matrix'] = self._transformation_processing_unit.get_transformation(slice_id).matrix
        scanner_coordinate_translate_kwargs['step_size'] = step_size
        return scanner_coordinate_translate_kwargs
    
    def _slice_coordinate_translate(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
        step_size: float,
        axis_name: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._slice_coordinate_translate_macro(
                    slice_id, slice_id_sequence, step_size, axis_name)
            case id.micro_mode_id:
                self._slice_coordinate_translate_micro(
                    slice_id, slice_id, step_size, axis_name)

    def _slice_coordinate_translate_macro(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        step_size: float,
        axis_name: str,
    ) -> None:
        for candidate_slice_id in slice_id_sequence:
            self._slice_coordinate_translate_micro(
                candidate_slice_id, slice_id, step_size, axis_name)

    def _slice_coordinate_translate_micro(
        self,
        candidate_slice_id: str,
        reference_slice_id: str,
        step_size: float,
        axis_name: str,
    ) -> None:
        self._transformation_processing_unit.insert_transformation(
            candidate_slice_id,
            self._transformation_processing_unit.translate(
                **self._get_slice_coordinate_translate_kwargs(
                    candidate_slice_id, reference_slice_id, step_size, axis_name
                ),
            ),
        )

    def _get_slice_coordinate_translate_kwargs(
        self,
        candidate_slice_id: str,
        reference_slice_id: str,
        step_size: float,
        axis_name: str,
    ) -> dict:
        slice_coordinate_translate_kwargs = self._data_accessor.get_slice_coordinate_translate_kwargs(
            reference_slice_id, axis_name)
        slice_coordinate_translate_kwargs['transformation_matrix'] = self._transformation_processing_unit.get_transformation(candidate_slice_id).matrix
        slice_coordinate_translate_kwargs['step_size'] = step_size
        return slice_coordinate_translate_kwargs
    
    def _slice_coordinate_rotate(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
        step_size: float,
        axis_name: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._slice_coordinate_rotate_macro(
                    slice_id_sequence, step_size, axis_name)
            case id.micro_mode_id:
                self._slice_coordinate_rotate_micro(
                    slice_id, step_size, axis_name)
            case _:
                raise exceptions.PreventUpdate

    def _slice_coordinate_rotate_macro(
        self,
        slice_id_sequence: tuple[str, ...],
        step_size: float,
        axis_name: str,
    ) -> None:
        for slice_id in slice_id_sequence:
            self._transformation_processing_unit.insert_transformation(
                slice_id,
                self._transformation_processing_unit.rotate(
                    **self._get_slice_coordinate_rotate_macro_kwargs(
                        slice_id, step_size, axis_name),
                ),
            )

    def _get_slice_coordinate_rotate_macro_kwargs(
        self, slice_id: str, step_size: float, axis_name: str) -> dict:
        slice_coordinate_rotate_macro_kwargs = self._data_accessor.get_slice_coordinate_rotate_macro_kwargs(slice_id, axis_name)
        slice_coordinate_rotate_macro_kwargs['step_size'] = step_size
        return slice_coordinate_rotate_macro_kwargs

    def _slice_coordinate_rotate_micro(
        self, slice_id: str, step_size: float, axis_name: str) -> None:
        self._transformation_processing_unit.insert_transformation(
            slice_id,
            self._transformation_processing_unit.rotate(
                **self._get_slice_coordinate_rotate_micro_kwargs(
                    slice_id, step_size, axis_name),
            ),
        )
    
    def _get_slice_coordinate_rotate_micro_kwargs(
        self, slice_id: str, step_size: float, axis_name: str) -> dict:
        slice_coordinate_rotate_micro_kwargs = self._data_accessor.get_slice_coordinate_rotate_micro_kwargs(slice_id, axis_name)
        slice_coordinate_rotate_micro_kwargs['step_size'] = step_size
        return slice_coordinate_rotate_micro_kwargs

    def _update_backend(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._update_backend_macro(slice_id_sequence)
            case id.micro_mode_id:
                self._update_backend_micro(slice_id)
            case _:
                raise exceptions.PreventUpdate
    
    def _update_backend_macro(self, slice_id_sequence: tuple[str, ...]) -> None:
        for slice_id in slice_id_sequence:
            self._update_backend_micro(slice_id)
    
    def _update_backend_micro(self, slice_id: str) -> None:
        self._update_transformation(slice_id)
        self._resample(slice_id)
    
    def _update_transformation(self, slice_id: str) -> None:
        self._data_accessor.update_transformation(
            slice_id,
            self._transformation_processing_unit.get_transformation(slice_id),
        )
        self._data_accessor.transform_slice(slice_id)
    
    def _resample(self, slice_id: str) -> None:
        self._update_body_resampled(slice_id, self._resample_body(slice_id))
        self._update_organ_resampled(slice_id, self._resample_organ(slice_id))
    
    def _resample_body(self, slice_id: str) -> np.ndarray:
        return self._resampling_processing_unit.resample_body(
            **self._data_accessor.get_resample_body_kwargs(slice_id))
    
    def _update_body_resampled(
        self, slice_id: str, pixel_data: np.ndarray) -> None:
        pixel_data = image_processing_utils.discretise(pixel_data)
        self._data_accessor.update_body_resampled(slice_id, pixel_data)
    
    def _resample_organ(self, slice_id: str) -> np.ndarray:
        return self._resampling_processing_unit.resample_organ(
            **self._data_accessor.get_resample_organ_kwargs(slice_id))
    
    def _update_organ_resampled(
        self, slice_id: str, pixel_data: np.ndarray) -> None:
        self._data_accessor.update_organ_resampled(slice_id, pixel_data)

    def _control_transformation_by_button(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
    ) -> None:
        match dash.callback_context.triggered_id:
            case id.undo_transformation_outline_button_id:
                self._undo_transformation(slice_id, slice_id_sequence, mode)
            case id.redo_transformation_outline_button_id:
                self._redo_transformation(slice_id, slice_id_sequence, mode)
            case id.optimise_transformation_outline_button_id:
                self._optimise_transformation(slice_id, slice_id_sequence, mode)
            case id.reset_transformation_outline_button_id:
                self._reset_transformation(slice_id, slice_id_sequence, mode)
            case _:
                raise exceptions.PreventUpdate
    
    def _undo_transformation(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._undo_transformation_macro(slice_id_sequence)
            case id.micro_mode_id:
                self._undo_transformation_micro(slice_id)
            case _:
                raise exceptions.PreventUpdate
    
    def _undo_transformation_macro(
        self, slice_id_sequence: tuple[str, ...]) -> None:
        for slice_id in slice_id_sequence:
            self._undo_transformation_micro(slice_id)
    
    def _undo_transformation_micro(self, slice_id: str) -> None:
        try:
            self._transformation_processing_unit.undo_transformation(slice_id)
        except:
            pass
    
    def _redo_transformation(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._redo_transformation_macro(slice_id_sequence)
            case id.micro_mode_id:
                self._redo_transformation_micro(slice_id)
            case _:
                raise exceptions.PreventUpdate

    def _redo_transformation_macro(
        self, slice_id_sequence: tuple[str, ...]) -> None:
        for slice_id in slice_id_sequence:
            self._redo_transformation_micro(slice_id)
    
    def _redo_transformation_micro(self, slice_id: str) -> None:
        try:
            self._transformation_processing_unit.redo_transformation(slice_id)
        except:
            pass

    def _optimise_transformation(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._optimise_transformation_macro(slice_id_sequence)
            case id.micro_mode_id:
                self._optimise_transformation_micro(slice_id)
            case _:
                raise exceptions.PreventUpdate

    def _optimise_transformation_macro(
        self, slice_id_sequence: tuple[str, ...]) -> None:
        for slice_id in slice_id_sequence:
            self._optimise_transformation_micro(slice_id)
    
    def _optimise_transformation_micro(self, slice_id: str) -> None:
        self._transformation_processing_unit.optimise_transformation(slice_id)

    def _reset_transformation(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
    ) -> None:
        match mode:
            case id.macro_mode_id:
                self._reset_transformation_macro(slice_id_sequence)
            case id.micro_mode_id:
                self._reset_transformation_micro(slice_id)
            case _:
                raise exceptions.PreventUpdate

    def _reset_transformation_macro(
        self, slice_id_sequence: tuple[str, ...]) -> None:
        for slice_id in slice_id_sequence:
            self._reset_transformation_micro(slice_id)

    def _reset_transformation_micro(self, slice_id: str) -> None:
        self._transformation_processing_unit.reset_transformation(slice_id)

    def _refresh_transformation_parameter(
        self, slice_id: str) -> tuple[str, ...]:
        return self._format_transformation_parameter(
            self._transformation_processing_unit.get_transformation(slice_id).parameter,
        )
    
    def _format_transformation_parameter(
        self, transformation_parameter: tuple[float, ...]) -> tuple[str, ...]:
        return tuple(
            format_utils.format_transformation_parameter(number)
            for number in transformation_parameter
        )

    def _patch_refresh_slice_state_sequence(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        mode: str,
        slice_state_sequence: tuple,
    ) -> tuple:
        match mode:
            case id.macro_mode_id:
                return self._patch_refresh_slice_state_sequence_macro(
                    slice_id_sequence, slice_state_sequence)
            case id.micro_mode_id:
                return self._patch_refresh_slice_state_sequence_micro(
                    slice_id, slice_id_sequence, slice_state_sequence)
            case _:
                raise exceptions.PreventUpdate

    def _patch_refresh_slice_state_sequence_macro(
        self,
        slice_id_sequence: tuple[str, ...],
        slice_state_sequence: tuple,
    ) -> tuple:
        return tuple(
            self._patch_refresh_slice_state(
                slice_state = slice_state,
                **self._data_accessor.get_patch_refresh_slice_state_kwargs(
                    slice_id),
            )
            for slice_id, slice_state
            in zip(slice_id_sequence, slice_state_sequence)
        )
    
    def _patch_refresh_slice_state_sequence_micro(
        self,
        slice_id: str,
        slice_id_sequence: tuple[str, ...],
        slice_state_sequence: tuple,
    ) -> tuple:
        return tuple(
            self._patch_refresh_slice_state(
                slice_state = slice_state,
                **self._data_accessor.get_patch_refresh_slice_state_kwargs(candidate_slice_id),
            )
            if candidate_slice_id == slice_id else dash.no_update
            for candidate_slice_id, slice_state
            in zip(slice_id_sequence, slice_state_sequence)
        )

    def _patch_refresh_slice_state(
        self,
        slice_state: record.State,
        spacing: tuple[float, float, float],
        direction: tuple[float, ...],
        origin: tuple[float, ...],
    ) -> dash.Patch:
        slice_state = dash.Patch()
        slice_state['image']['spacing'] = spacing
        slice_state['image']['direction'] = direction
        slice_state['image']['origin'] = origin
        return slice_state
    
    def _refresh_figure_data_store_modified_timestamp_sequence(
        self, figure_data_store_modified_timestamp_sequence: tuple) -> tuple:
        return tuple(
            modified_timestamp + 1
            for modified_timestamp
            in figure_data_store_modified_timestamp_sequence
        )

class BodyMenuCallbackPlugin:
    """Plugin that adds callbacks triggered in Body Menu."""

    def _add_body_menu_callback(self) -> None:
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'body_menu',
                function_name = 'control_body_representation_visibility',
            ),
            dash.Output(id.body_representation_id, 'volume'),
            dash.Input(id.body_visibility_switch_id, 'value'),
            prevent_initial_call = True,
        )

        @dash.callback(
            {
                'body_resampled_window': (
                    dash.Output(id.body_resampled_window_level_slider_id, 'value', allow_duplicate=True),
                    dash.Output(id.body_resampled_window_width_slider_id, 'value', allow_duplicate=True),
                ),
                'body_visibility':
                    dash.Output(id.body_visibility_switch_id, 'value'),
            },
            dash.Input(id.reset_body_menu_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )
        def reset_body_menu(_: int) -> dict:
            return self._reset_body_menu()

    def _reset_body_menu(self) -> dict:
        body_property = self._visualisation_processing_unit.body_property
        body_resampled_property = self._visualisation_processing_unit.body_resampled_property
        return {
            'body_resampled_window': (
                body_resampled_property['window_level'],
                body_resampled_property['window_width'],
            ),
            'body_visibility': body_property['visibility'] == 1,
        }

class OrganMenuCallbackPlugin:
    """Plugin that adds callbacks triggered in Organ Menu."""

    def _add_organ_menu_callback(self) -> None:
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'organ_menu',
                function_name = 'control_organ_representation_visibility',
            ),
            dash.Output(id.organ_representation_id, 'volume'),
            dash.Output(id.plot_3d_view_id, 'triggerRender'),
            dash.Input(id.organ_visibility_switch_id, 'value'),
            dash.State(id.plot_3d_view_id, 'triggerRender'),
            prevent_initial_call = True,
        )

        @dash.callback(
            {
                'organ_resampled_threshold':
                    dash.Output(id.organ_resampled_threshold_slider_id, 'value', allow_duplicate=True),
                'organ_resampled_opacity':
                    dash.Output(id.organ_resampled_opacity_slider_id, 'value', allow_duplicate=True),
                'organ_visibility':
                    dash.Output(id.organ_visibility_switch_id, 'value'),
            },
            dash.Input(id.reset_organ_menu_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )
        def reset_organ_menu(_: int) -> dict:
            return self._reset_organ_menu()

    def _reset_organ_menu(self) -> dict:
        organ_property = self._visualisation_processing_unit.organ_property
        organ_resampled_property = self._visualisation_processing_unit.organ_resampled_property
        return {
            'organ_resampled_threshold': organ_resampled_property['threshold'],
            'organ_resampled_opacity': organ_resampled_property['opacity'],
            'organ_visibility': organ_property['visibility'] == 1,
        }

class SliceMenuCallbackPlugin:
    """Plugin that adds callbacks triggered in Slice Menu"""

    def _add_slice_menu_callback(self) -> None:
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'slice_menu',
                function_name = 'control_slice_representation_property',
            ),
            dash.Output(widget_utils.build_matchable_id(dash.ALL, id.slice_representation_type), 'property'),
            dash.Input(id.slice_window_level_slider_id, 'value'),
            dash.Input(id.slice_window_width_slider_id, 'value'),
            dash.Input(id.slice_opacity_slider_id, 'value'),
            dash.State(id.slice_selection_dropdown_id, 'options'),
            prevent_initial_call = True,
        )

        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'slice_menu',
                function_name = 'control_slice_representation_visibility',
            ),
            dash.Output(widget_utils.build_matchable_id(dash.ALL, id.slice_representation_type), 'actor'),
            dash.Input(id.slice_selection_dropdown_id, 'value'),
            dash.Input(id.mode_selection_inline_radio_items_id, 'value'),
            dash.State(id.slice_selection_dropdown_id, 'options'),
        )

        @dash.callback(
            {
                'slice_window': (
                    dash.Output(id.slice_window_level_slider_id, 'value', allow_duplicate=True),
                    dash.Output(id.slice_window_width_slider_id, 'value', allow_duplicate=True),
                ),
                'slice_opacity':
                    dash.Output(id.slice_opacity_slider_id, 'value', allow_duplicate=True),
            },
            dash.Input(id.reset_slice_menu_button_id, 'n_clicks'),
            prevent_initial_call = True,
        ) 
        def reset_slice_menu(_: int) -> dict:
            return self._reset_slice_menu()

    def _reset_slice_menu(self) -> dict:
        slice_property = self._visualisation_processing_unit.slice_property
        return {
            'slice_window': (
                slice_property['window_level'],
                slice_property['window_width'],
            ),
            'slice_opacity': slice_property['opacity'],
        }


class MenuCallbackPlugin(
    TransformationMenuCallbackPlugin,
    BodyMenuCallbackPlugin,
    OrganMenuCallbackPlugin,
    SliceMenuCallbackPlugin,
):
    """Plugin that adds callbacks triggered in all menus."""

    def _add_menu_callback(self) -> None:
        self._add_transformation_menu_callback()
        self._add_body_menu_callback()
        self._add_organ_menu_callback()
        self._add_slice_menu_callback()