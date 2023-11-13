"""Utils for building widgets.

This module contains utility functions that facilitate
building widgets at runtime.

Created by: Weixun Luo
Date: 21/03/2023
"""
from __future__ import annotations
import typing

from dash import dcc
import dash_bootstrap_components as dbc
import dash_extensions
import dash_vtk

from object import record


BODY_REPRESENTATION_CONTROLLER_SIZE = (200, 75)
DROPDOWN_OPTION_HEIGHT = 45
DROPDOWN_MAX_HEIGHT = 200
ORGAN_REPRESENTATION_COLOR_MAP = 'ITK Snap'  # This is hard-coded into the
                                             # dash_vtk package
ORGAN_REPRESENTATION_COLOR_RANGE = (0, 6)

ID: typing.TypeAlias = str | dict[str, str]
NumericChildren: typing.TypeAlias = int | float | None
Children: typing.TypeAlias = NumericChildren | str
Option: typing.TypeAlias = tuple[Children, ...] | dict[str, Children]


# ----- Button -----
def build_button(
    id: ID, children: Children, class_name: str | None = None) -> dbc.Button:
    return dbc.Button(children, id, class_name, n_clicks=0)

def build_outline_button(
    id: ID,
    children: Children,
    color: str = 'primary',
    class_name: str | None = None,
) -> dbc.Button:
    return dbc.Button(
        children, id, class_name, color=color, outline=True, n_clicks=0)


# ----- Dropdown -----
def build_dropdown(
    id: ID,
    option: Option = (),
    value: Children = None,
    display_number: int | None = None,
    class_name: str | None = None,
) -> dcc.Dropdown:
    return dcc.Dropdown(
        option,
        value,
        searchable = False,
        clearable = False,
        optionHeight = DROPDOWN_OPTION_HEIGHT,
        maxHeight = DROPDOWN_OPTION_HEIGHT * display_number
                    if display_number is not None
                    else DROPDOWN_MAX_HEIGHT,
        id = id,
        className = class_name,
    )


# ----- ID -----
def build_matchable_id(slice_id: str, widget_type: str) -> dict[str, str]:
    return {'slice_id':slice_id, 'widget_type':widget_type}


# ----- Keyboard -----
def build_keyboard_event(
    key: str,
    ctrl_pressed: bool = False,
    shift_pressed: bool = False,
    alt_pressed: bool = False,
    meta_pressed: bool = False,
    repeat: bool = False,
) -> record.KeyboardEvent:
    return record.KeyboardEvent(
        key = key,
        ctrlKey = ctrl_pressed,
        shiftKey = shift_pressed,
        altKey = alt_pressed,
        metaKey = meta_pressed,
        repeat = repeat,
    )

def build_keyboard_listener(id: ID) -> dash_extensions.EventListener:
    return dash_extensions.EventListener(id=id, logging=False, n_events=0)


# ----- Label -----
def build_label(
    children: Children = '',
    id: ID = '',
    class_name: str | None = None,
) -> dbc.Label:
    return dbc.Label(children, id, class_name=class_name)


# ----- Location -----
def build_location(id: ID) -> dcc.Location:
    return dcc.Location(id, refresh='callback-nav')


# ----- Markdown -----
def build_markdown(children: str, id: ID = '') -> dcc.Markdown:
    return dcc.Markdown(children, id, link_target='_blank')


# ----- Modal -----
def build_error_modal(
    modal_id: ID, close_button_id: ID, children: Children) -> dbc.Modal:
    return _build_central_modal(modal_id, close_button_id, 'Error', children)

def build_help_modal(
    modal_id: ID, close_button_id: ID, children: dcc.Markdown) -> dbc.Modal:
    return dbc.Modal(
        id = modal_id,
        children = (
            dbc.ModalHeader(dbc.ModalTitle('Help')),
            dbc.ModalBody(children),
            dbc.ModalFooter(build_button(close_button_id, 'Close')),
        ),
        size = 'xl',
        scrollable = True,
        is_open = False,
    )

def build_information_modal(
    modal_id: ID, close_button_id: ID, children: Children) -> dbc.Modal:
    return _build_central_modal(
        modal_id, close_button_id, 'Information', children)

def _build_central_modal(
    modal_id: ID, close_button_id: ID, header: str, body: str) -> dbc.Modal:
    return dbc.Modal(
        id = modal_id,
        children = (
            dbc.ModalHeader(dbc.ModalTitle(header)),
            dbc.ModalBody(body),
            dbc.ModalFooter(build_button(close_button_id, 'Close')),
        ),
        is_open = False,
        centered = True,
    )


# ----- Radio Items -----
def build_inline_radio_items(
    id: ID,
    option: Option,
    value: Children,
    class_name: str | None = None,
) -> dbc.RadioItems:
    return dbc.RadioItems(
        option,
        value,
        inline = True,
        id = id,
        className = class_name,
    )


# ----- Representation -----
def build_body_representation(
    representation_id: ID,
    volume_id: ID,
    state: record.State,
    property: record.Body3DProperty,
) -> dash_vtk.VolumeRepresentation:
    return dash_vtk.VolumeRepresentation(
        id = representation_id,
        children = (
            dash_vtk.VolumeController(size=BODY_REPRESENTATION_CONTROLLER_SIZE),
            dash_vtk.Volume(volume_id, state=state),
        ),
        volume = {'visibility':property['visibility']},
    )

def build_organ_representation(
    representation_id: ID,
    volume_id: ID,
    state: record.State,
    property: record.Organ3DProperty,
) -> dash_vtk.VolumeRepresentation:
    return dash_vtk.VolumeRepresentation(
        id = representation_id,
        children = dash_vtk.Volume(volume_id, state=state),
        colorMapPreset = ORGAN_REPRESENTATION_COLOR_MAP,
        colorDataRange = ORGAN_REPRESENTATION_COLOR_RANGE,
        volume = {'visibility':property['visibility']}
    )

def build_slice_representation(
    representation_id: ID,
    volume_id: ID,
    state: record.Slice2DProperty,
    property: record.Slice2DProperty,
) -> dash_vtk.SliceRepresentation:
    return dash_vtk.SliceRepresentation(
        id = representation_id,
        children = dash_vtk.Volume(volume_id, state=state),
        property = {
            'colorLevel': property['window_level'],
            'colorWindow': property['window_width'],
            'opacity': property['opacity'],
        },
        actor = {'visibility':property['visibility']},
    )


# ----- Slider -----
def build_slider(
    id: ID,
    value: NumericChildren = 0.0,
    range: tuple[NumericChildren, NumericChildren] = (0.0, 1.0),
    step: NumericChildren = 0.1,
    class_name: str | None = None,
) -> dcc.Slider:
    return dcc.Slider(
        value = value,
        min = range[0],
        max = range[1],
        step = step,
        marks = None,
        tooltip = {'placement':'bottom', 'always_visible':True},
        id = id,
        className = class_name,
    )


# ----- Store -----
def build_store(id: ID, data: str | dict | None = None) -> dcc.Store:
    return dcc.Store(id, 'memory', data, modified_timestamp=-1)


# ----- Switch -----
def build_switch(
    id: ID,
    children: Children,
    is_activate: bool = True,
    class_name: str | None = None,
) -> dbc.Switch:
    return dbc.Switch(
        label = children,
        value = is_activate,
        id = id,
        class_name = class_name,
    )