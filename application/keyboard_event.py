"""Keyboard Event.

This module contains all keyboard events that can trigger
callbacks in the application.

Created by: Weixun Luo
Date: 15/04/2023
"""
from utils import widget_utils


# ----- Scanner Coordinate Translation -----
scanner_coordinate_translate_positive_x_keyboard_event = widget_utils.build_keyboard_event('a')
scanner_coordinate_translate_negative_x_keyboard_event = widget_utils.build_keyboard_event('d')
scanner_coordinate_translate_positive_y_keyboard_event = widget_utils.build_keyboard_event('w')
scanner_coordinate_translate_negative_y_keyboard_event = widget_utils.build_keyboard_event('s')
scanner_coordinate_translate_positive_z_keyboard_event = widget_utils.build_keyboard_event('q')
scanner_coordinate_translate_negative_z_keyboard_event = widget_utils.build_keyboard_event('e')


# ----- Slice Coordinate Translation -----
slice_coordinate_translate_positive_x_keyboard_event = widget_utils.build_keyboard_event('j')
slice_coordinate_translate_negative_x_keyboard_event = widget_utils.build_keyboard_event('l')
slice_coordinate_translate_positive_y_keyboard_event = widget_utils.build_keyboard_event('i')
slice_coordinate_translate_negative_y_keyboard_event = widget_utils.build_keyboard_event('k')
slice_coordinate_translate_positive_z_keyboard_event = widget_utils.build_keyboard_event('u')
slice_coordinate_translate_negative_z_keyboard_event = widget_utils.build_keyboard_event('o')


# ----- Slice Coordinate Rotation -----
slice_coordinate_rotate_clockwise_x_keyboard_event = widget_utils.build_keyboard_event('W', shift_pressed=True)
slice_coordinate_rotate_anti_clockwise_x_keyboard_event = widget_utils.build_keyboard_event('S', shift_pressed=True)
slice_coordinate_rotate_clockwise_y_keyboard_event = widget_utils.build_keyboard_event('A', shift_pressed=True)
slice_coordinate_rotate_anti_clockwise_y_keyboard_event = widget_utils.build_keyboard_event('D', shift_pressed=True)
slice_coordinate_rotate_clockwise_z_keyboard_event = widget_utils.build_keyboard_event('E', shift_pressed=True)
slice_coordinate_rotate_anti_clockwise_z_keyboard_event = widget_utils.build_keyboard_event('Q', shift_pressed=True)


# ----- Other -----
update_backend_keyboard_event = widget_utils.build_keyboard_event('r')