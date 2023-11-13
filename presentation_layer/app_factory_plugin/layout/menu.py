"""Menu Plugins of App Factory.

This module contains the implementation of App Factory
Plugins. They define the layout and structure of all menus
used in the application.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations

from dash import dcc
import dash_bootstrap_components as dbc

from application import id
from utils import widget_utils


# ----- Transformation Menu -----
TRANSLATION_INDICATOR_LABEL_CHILDREN = 'Translation:'
TRANSLATION_X_INDICATOR_LABEL_CHILDREN = 'x:'
TRANSLATION_Y_INDICATOR_LABEL_CHILDREN = 'y:'
TRANSLATION_Z_INDICATOR_LABEL_CHILDREN = 'z:'
TRANSLATION_STEP_SIZE_INDICATOR_LABEL_CHILDREN = 'Translation Step Size (mm):'
TRANSLATION_STEP_SIZE_SLIDER_VALUE = 1.0
TRANSLATION_STEP_SIZE_SLIDER_RANGE = (0.1, 5.0)
TRANSLATION_STEP_SIZE_SLIDER_STEP = 0.1
ROTATION_INDICATOR_LABEL_CHILDREN = 'Rotation:'
ROTATION_X_INDICATOR_LABEL_CHILDREN = 'x:'
ROTATION_Y_INDICATOR_LABEL_CHILDREN = 'y:'
ROTATION_Z_INDICATOR_LABEL_CHILDREN = 'z:'
ROTATION_STEP_SIZE_INDICATOR_LABEL_CHILDREN = 'Rotation Step Size (degree):'
ROTATION_STEP_SIZE_SLIDER_VALUE = 1.0
ROTATION_STEP_SIZE_SLIDER_RANGE = (0.1, 5.0)
ROTATION_STEP_SIZE_SLIDER_STEP = 0.1
UNDO_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN = 'Undo'
REDO_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN = 'Redo'
OPTIMISE_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN = 'Optimise'
RESET_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN = 'Reset'

# ----- Body Menu -----
BODY_RESAMPLED_WINDOW_LEVEL_INDICATOR_LABEL_CHILDREN = 'Window Level:'
BODY_RESAMPLED_WINDOW_WIDTH_INDICATOR_LABEL_CHILDREN = 'Window Width:'
RESET_BODY_MENU_BUTTON_CHILDREN = 'Reset'
BODY_VISIBILITY_SWITCH_CHILDREN = 'Show'

# ----- Organ Menu -----
ORGAN_RESAMPLED_THRESHOLD_INDICATOR_LABEL_CHILDREN = 'Threshold:'
ORGAN_RESAMPLED_OPACITY_INDICATOR_LABEL_CHILDREN = 'Opacity:'
RESET_ORGAN_MENU_BUTTON_CHILDREN = 'Reset'
ORGAN_VISIBILITY_SWITCH_CHILDREN = 'Show'

# ----- Slice Menu -----
SLICE_WINDOW_LEVEL_INDICATOR_LABEL_CHILDREN = 'Window Level:'
SLICE_WINDOW_WIDTH_INDICATOR_LABEL_CHILDREN = 'Window Width:'
SLICE_OPACITY_INDICATOR_LABEL_CHILDREN = 'Opacity:'
RESET_SLICE_MENU_BUTTON_CHILDREN = 'Reset'

# ----- Contour Menu -----
CONTOUR_MENU_OPTION_TAG = 'Contour'  # Content displayed in the selection dropdown in Support Menu
CONTOUR_LINE_WIDTH_INDICATOR_LABEL_CHILDREN = 'Line Width:'
CONTOUR_LINE_WIDTH_SLIDER_RANGE = (0, 5)
CONTOUR_LINE_WIDTH_SLIDER_STEP = 1

# ----- Checkerboard Menu -----
CHECKERBOARD_MENU_OPTION_TAG = 'Checkerboard'  # Content displayed in the selection dropdown in Support Menu
CHECKERBOARD_BOARD_WIDTH_INDICATOR_LABEL_CHILDREN = 'Board Width:'
CHECKERBOARD_BOARD_WIDTH_SLIDER_RANGE = (1, 100)
CHECKERBOARD_BOARD_WIDTH_SLIDER_STEP = 1


class TransformationMenuPlugin:
    """Plugin that defines the layout of Transformation Menu."""

    def _build_transformation_menu(self) -> dbc.Stack:
        return dbc.Stack(
            id = id.transformation_menu_id,
            children = (
                dbc.Row(
                    children = (
                        dbc.Col(self._build_translation_indicator_label(), width=3),
                        dbc.Col(self._build_translation_x_indicator_label(), width=1),
                        dbc.Col(self._build_translation_x_label(), width=2),
                        dbc.Col(self._build_translation_y_indicator_label(), width=1),
                        dbc.Col(self._build_translation_y_label(), width=2),
                        dbc.Col(self._build_translation_z_indicator_label(), width=1),
                        dbc.Col(self._build_translation_z_label(), width=2),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_translation_step_size_indicator_label(), width=7),
                        dbc.Col(self._build_translation_step_size_slider(), width=5),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_rotation_indicator_label(), width=3),
                        dbc.Col(self._build_rotation_x_indicator_label(), width=1),
                        dbc.Col(self._build_rotation_x_label(), width=2),
                        dbc.Col(self._build_rotation_y_indicator_label(), width=1),
                        dbc.Col(self._build_rotation_y_label(), width=2),
                        dbc.Col(self._build_rotation_z_indicator_label(), width=1),
                        dbc.Col(self._build_rotation_z_label(), width=2),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_rotation_step_size_indicator_label(), width=7),
                        dbc.Col(self._build_rotation_step_size_slider(), width=5),
                    )
                ),
                dbc.Row(self._build_transformation_control_button_group(), justify = 'center'),
            ),
            gap = 1,
            style = {'display':'none'},
        )
    
    def _build_translation_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(TRANSLATION_INDICATOR_LABEL_CHILDREN)
    
    def _build_translation_x_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(TRANSLATION_X_INDICATOR_LABEL_CHILDREN)

    def _build_translation_x_label(self) -> dbc.Label:
        return widget_utils.build_label(id=id.translation_x_label_id)
    
    def _build_translation_y_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(TRANSLATION_Y_INDICATOR_LABEL_CHILDREN)

    def _build_translation_y_label(self) -> dbc.Label:
        return widget_utils.build_label(id=id.translation_y_label_id)
    
    def _build_translation_z_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(TRANSLATION_Z_INDICATOR_LABEL_CHILDREN)

    def _build_translation_z_label(self) -> dbc.Label:
        return widget_utils.build_label(id=id.translation_z_label_id)
    
    def _build_translation_step_size_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(TRANSLATION_STEP_SIZE_INDICATOR_LABEL_CHILDREN)
    
    def _build_translation_step_size_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id = id.translation_step_size_slider_id,
            value = TRANSLATION_STEP_SIZE_SLIDER_VALUE,
            range = TRANSLATION_STEP_SIZE_SLIDER_RANGE,
            step = TRANSLATION_STEP_SIZE_SLIDER_STEP,
        )
    
    def _build_rotation_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(ROTATION_INDICATOR_LABEL_CHILDREN)

    def _build_rotation_x_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(ROTATION_X_INDICATOR_LABEL_CHILDREN)

    def _build_rotation_x_label(self) -> dbc.Label:
        return widget_utils.build_label(id=id.rotation_x_label_id)
    
    def _build_rotation_y_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(ROTATION_Y_INDICATOR_LABEL_CHILDREN)
    
    def _build_rotation_y_label(self) -> dbc.Label:
        return widget_utils.build_label(id=id.rotation_y_label_id)
    
    def _build_rotation_z_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(ROTATION_Z_INDICATOR_LABEL_CHILDREN)

    def _build_rotation_z_label(self) -> dbc.Label:
        return widget_utils.build_label(id=id.rotation_z_label_id)
    
    def _build_rotation_step_size_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(ROTATION_STEP_SIZE_INDICATOR_LABEL_CHILDREN)
    
    def _build_rotation_step_size_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id = id.rotation_step_size_slider_id,
            value = ROTATION_STEP_SIZE_SLIDER_VALUE,
            range = ROTATION_STEP_SIZE_SLIDER_RANGE,
            step = ROTATION_STEP_SIZE_SLIDER_STEP,
        )
    
    def _build_transformation_control_button_group(self) -> dbc.ButtonGroup:
        return dbc.ButtonGroup(
            children = (
                self._build_undo_transformation_outline_button(),
                self._build_redo_transformation_outline_button(),
                self._build_optimise_transformation_button(),
                self._build_reset_transformation_outline_button(),
            ),
        )

    def _build_undo_transformation_outline_button(self) -> dbc.Button:
        return widget_utils.build_outline_button(
            id = id.undo_transformation_outline_button_id,
            children = UNDO_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN,
        )
    
    def _build_redo_transformation_outline_button(self) -> dbc.Button:
        return widget_utils.build_outline_button(
            id = id.redo_transformation_outline_button_id,
            children = REDO_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN,
        )
    
    def _build_optimise_transformation_button(self) -> dbc.Button:
        return widget_utils.build_outline_button(
            id = id.optimise_transformation_outline_button_id,
            children = OPTIMISE_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN,
        )
        
    def _build_reset_transformation_outline_button(self) -> dbc.Button:
        return widget_utils.build_outline_button(
            id = id.reset_transformation_outline_button_id,
            children = RESET_TRANSFORMATION_OUTLINE_BUTTON_CHILDREN,
        )

class BodyMenuPlugin:
    """Plugin that defines the layout of Body Menu."""

    def _build_body_menu(self) -> dbc.Stack:
        return dbc.Stack(
            id = id.body_menu_id,
            children = (
                dbc.Row(
                    children = (
                        dbc.Col(self._build_body_resampled_window_level_indicator_label(), width=4),
                        dbc.Col(self._build_body_resampled_window_level_slider(), width=8),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_body_resampled_window_width_indicator_label(), width=4),
                        dbc.Col(self._build_body_resampled_window_width_slider(), width=8),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_reset_body_menu_button(), width=4),
                        dbc.Col(self._build_body_visibility_switch(), width=4),
                    ),
                    justify = 'center',
                ),
            ),
            gap = 3,
            style = {'display':'none'},
        )
    
    def _build_body_resampled_window_level_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(BODY_RESAMPLED_WINDOW_LEVEL_INDICATOR_LABEL_CHILDREN)
    
    def _build_body_resampled_window_level_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id.body_resampled_window_level_slider_id)
    
    def _build_body_resampled_window_width_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(BODY_RESAMPLED_WINDOW_WIDTH_INDICATOR_LABEL_CHILDREN)

    def _build_body_resampled_window_width_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id.body_resampled_window_width_slider_id)
    
    def _build_reset_body_menu_button(self) -> dbc.Button:
        return widget_utils.build_button(
            id = id.reset_body_menu_button_id,
            children = RESET_BODY_MENU_BUTTON_CHILDREN,
        )
    
    def _build_body_visibility_switch(self) -> dbc.Switch:
        return widget_utils.build_switch(
            id = id.body_visibility_switch_id,
            children = BODY_VISIBILITY_SWITCH_CHILDREN,
        )

class OrganMenuPlugin:
    """Plugin that defines the layout of Organ Menu."""
    
    def _build_organ_menu(self) -> dbc.Stack:
        return dbc.Stack(
            id = id.organ_menu_id,
            children = (
                dbc.Row(
                    children = (
                        dbc.Col(widget_utils.build_label('Threshold:'), width=4),
                        dbc.Col(self._build_organ_resampled_threshold_slider(), width=8),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(widget_utils.build_label('Opacity:'), width=4),
                        dbc.Col(self._build_organ_resampled_opacity_slider(), width=8),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_reset_organ_menu_button(), width=4),
                        dbc.Col(self._build_organ_visibility_switch(), width=4),
                    ),
                    justify = 'center',
                ),
            ),
            gap = 3,
            style = {'display':'none'},
        )
    
    def _build_organ_resampled_threshold_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(ORGAN_RESAMPLED_THRESHOLD_INDICATOR_LABEL_CHILDREN)
    
    def _build_organ_resampled_threshold_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id.organ_resampled_threshold_slider_id)
    
    def _build_organ_resampled_opacity_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(ORGAN_RESAMPLED_OPACITY_INDICATOR_LABEL_CHILDREN)
    
    def _build_organ_resampled_opacity_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id.organ_resampled_opacity_slider_id)
    
    def _build_reset_organ_menu_button(self) -> dbc.Button:
        return widget_utils.build_button(
            id = id.reset_organ_menu_button_id,
            children = RESET_ORGAN_MENU_BUTTON_CHILDREN,
        )
        
    def _build_organ_visibility_switch(self) -> dbc.Switch:
        return widget_utils.build_switch(
            id = id.organ_visibility_switch_id,
            children = ORGAN_VISIBILITY_SWITCH_CHILDREN,
        )

class SliceMenuPlugin:
    """Plugin that defines the layout of Slice Menu."""

    def _build_slice_menu(self) -> dbc.Stack:
        return dbc.Stack(
            id = id.slice_menu_id,
            children = (
                dbc.Row(
                    children = (
                        dbc.Col(self._build_slice_window_level_indicator_label(), width=4),
                        dbc.Col(self._build_slice_window_level_slider(), width=8),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_slice_window_width_indicator_label(), width=4),
                        dbc.Col(self._build_slice_window_width_slider(), width=8),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(self._build_slice_opacity_indicator_label(), width=4),
                        dbc.Col(self._build_slice_opacity_slider(), width=8),
                    ),
                ),
                dbc.Row(
                    children = (
                        dbc.Col(width = 5),
                        dbc.Col(self._build_reset_slice_menu_button(), width=2),
                        dbc.Col(width = 5),
                    ),
                ),
            ),
            gap = 3,
            style = {'display':'none'},
        )
    
    def _build_slice_window_level_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(SLICE_WINDOW_LEVEL_INDICATOR_LABEL_CHILDREN)
    
    def _build_slice_window_level_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id.slice_window_level_slider_id)
        
    def _build_slice_window_width_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(SLICE_WINDOW_WIDTH_INDICATOR_LABEL_CHILDREN)

    def _build_slice_window_width_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id.slice_window_width_slider_id)
    
    def _build_slice_opacity_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(SLICE_OPACITY_INDICATOR_LABEL_CHILDREN)

    def _build_slice_opacity_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id.slice_opacity_slider_id)
    
    def _build_reset_slice_menu_button(self) -> dbc.Button:
        return widget_utils.build_button(
            id = id.reset_slice_menu_button_id,
            children = RESET_SLICE_MENU_BUTTON_CHILDREN,
        )

class ContourMenuPlugin:
    """Plugin that defines the layout of Contour Menu."""

    def _build_contour_menu(self) -> dbc.Stack:
        return dbc.Stack(
            id = id.contour_menu_id,
            children = dbc.Row(
                children = (
                    dbc.Col(self._build_contour_line_width_indicator_label(), width=4),
                    dbc.Col(self._build_contour_line_width_slider(), width=8),
                ),
            ),
            style = {'display':'none'},
        )
    
    def _build_contour_line_width_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(CONTOUR_LINE_WIDTH_INDICATOR_LABEL_CHILDREN)
    
    def _build_contour_line_width_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id = id.contour_line_width_slider_id,
            range = CONTOUR_LINE_WIDTH_SLIDER_RANGE,
            step = CONTOUR_LINE_WIDTH_SLIDER_STEP,
        )

class CheckerboardMenuPlugin:
    """Plugin that defines the layout of Checkerboard Menu."""

    def _build_checkerboard_menu(self) -> dbc.Stack:
        return dbc.Stack(
            id = id.checkerboard_menu_id,
            children = dbc.Row(
                children = (
                    dbc.Col(self._build_checkerboard_board_width_indicator_label(), width=4),
                    dbc.Col(self._build_checkerboard_board_width_slider(), width=8),
                ),
            ),
            style = {'display':'none'},
        )
    
    def _build_checkerboard_board_width_indicator_label(self) -> dbc.Label:
        return widget_utils.build_label(CHECKERBOARD_BOARD_WIDTH_INDICATOR_LABEL_CHILDREN)
    
    def _build_checkerboard_board_width_slider(self) -> dcc.Slider:
        return widget_utils.build_slider(
            id = id.checkerboard_board_width_slider_id,
            range = CHECKERBOARD_BOARD_WIDTH_SLIDER_RANGE,
            step = CHECKERBOARD_BOARD_WIDTH_SLIDER_STEP,
        )