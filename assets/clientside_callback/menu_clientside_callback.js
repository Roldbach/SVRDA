/*Clientside Callbacks Triggered in All Menus.

This module adds clientside callbacks triggered in all menus
to the application.

Changes to the following components must also be updated:
(1) macro_mode_id (./application/id.py)
(2) micro_mode_id (./application/id.py)

Created by: Weixun Luo
Date: 05/05/2023
*/
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    body_menu: {
        control_body_representation_visibility: function (is_body_visible) {
            return {'visibility':is_body_visible == true ? 1 : 0};
        },
    },
    organ_menu: {
        control_organ_representation_visibility: function (is_organ_visible, trigger) {
            return [
                {'visibility':is_organ_visible == true ? 1 : 0},
                trigger + 1,
            ];
        },
    },
    slice_menu: {
        control_slice_representation_property: function (
            slice_window_level,
            slice_window_width,
            slice_opacity,
            slice_id_sequence,
        ) {
            var output = [];
            for (var i = 0; i < slice_id_sequence.length; i++) {
                output.push({
                    'colorLevel': slice_window_level,
                    'colorWindow': slice_window_width,
                    'opacity': slice_opacity,
                });
            }
            return output;
        },
        control_slice_representation_visibility: function (
            slice_id, mode, slice_id_sequence,
        ) {
            var output = []
            for (var i = 0; i < slice_id_sequence.length; i++) {
                if (mode == 'main_page_macro_mode') {
                    output.push({'visibility':1});
                }
                else if (mode == 'main_page_micro_mode') {
                    output.push({
                        'visibility': slice_id_sequence[i] == slice_id ? 1 : 0
                    });
                }
            }
            return output;
        },
    },
});