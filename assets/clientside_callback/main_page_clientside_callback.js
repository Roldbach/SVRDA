/*Clientside Callbacks Triggered in Main Page.

This module adds clientside callbacks triggered in Main Page
to the application.

Changes to the following components must also be updated:
(1) transformation_menu_id (./application/id.py)
(2) body_menu_id (./application/id.py)
(3) organ_menu_id (./application/id.py)
(4) slice_menu_id (./application/id.py)
(5) contour_menu_id (./application/id.py)
(6) checkerboard_menu_id (./application/id.py)
(7) none_mask_id (./application/id.py)
(8) contour_id (./application/id.py)
(8) mask_id (./application/id.py)

Created by: Weixun Luo
Date: 05/05/2023
*/
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    main_menu_section: {
        select_main_menu: function (main_menu_id) {
            return [
                main_menu_id == 'main_page_transformation_menu' ? null : {'display':'none'},
                main_menu_id == 'main_page_body_menu' ? null : {'display':'none'},
                main_menu_id == 'main_page_organ_menu' ? null : {'display':'none'},
                main_menu_id == 'main_page_slice_menu' ? null : {'display':'none'},
            ];
        },
    },
    evaluation_section: {
        control_evaluation_result_visibility: function (is_evaluation_result_visible) {
            return is_evaluation_result_visible == true ? null : {'display':'none'};
        },
    },
    support_menu_section: {
        select_support_menu: function (support_menu_id) {
            return [
                support_menu_id == 'main_page_contour_menu' ? null : {'display':'none'},
                support_menu_id == 'main_page_checkerboard_menu' ? null : {'display':'none'},
            ];
        },
    },
    main_plot_2d_section: {
        refresh_main_graph: function (
            figure_data_main,
            figure_data_support,
            contour_line_width,
            mask_type,
            mask_format,
        ) {
            if (figure_data_main === undefined || figure_data_support === undefined) {
                return {};
            }
            else {
                return {
                    'data': [
                        build_main_graph_main_plot(figure_data_main),
                        build_main_graph_support_plot(
                            figure_data_support,
                            mask_type,
                            mask_format,
                            contour_line_width,
                        ),
                    ],
                    'layout': build_figure_layout(),
                };
            }
        },
    },
    support_plot_2d_section: {
        refresh_support_graph: function (
            figure_data_main,
            figure_data_support,
            contour_line_width,
            mask_type,
            mask_format,
        ) {
            if (figure_data_main === undefined || figure_data_support === undefined) {
                return {};
            }
            else {
                return {
                    'data': [
                        build_support_graph_main_plot(figure_data_main),
                        build_support_graph_support_plot(
                            figure_data_support,
                            mask_type,
                            mask_format,
                            contour_line_width,
                        ),
                    ],
                    'layout': build_figure_layout(),
                };
            }
        },
    },
});

function build_main_graph_main_plot(figure_data_main) {
    return build_image(figure_data_main, 'rgb');
}

function build_main_graph_support_plot(
    figure_data_support,
    mask_type,
    mask_format,
    contour_line_width,
) {
    if (mask_type != 'main_page_none_mask') {
        if (mask_format == 'main_page_contour') {
            return build_contour(figure_data_support, contour_line_width);
        }
        else if (mask_format == 'main_page_mask') {
            return build_image(figure_data_support, 'rgba');
        }
    }
    else {
        return build_placeholder();
    }
}

function build_support_graph_main_plot(figure_data_main) {
    return build_image(figure_data_main, 'rgb');
}

function build_support_graph_support_plot(
    figure_data_support,
    mask_type,
    mask_format,
    contour_line_width,
) {
    if (mask_type != 'main_page_none_mask') {
        if (mask_format == 'main_page_contour') {
            return build_contour(figure_data_support, contour_line_width);
        }
        else if (mask_format == 'main_page_mask') {
            return build_image(figure_data_support, 'rgba');
        }
    }
    else {
        return build_placeholder();
    }
}

function build_image(source, color_model) {
    return {
        'type': 'image',
        'source': source,
        'colormodel': color_model,
        'hoverinfo': 'skip',
    };
}

function build_placeholder() {
    return {
        'type': 'image',
        'z': [],
        'colormodel': 'rgb',
        'hoverinfo': 'skip',
    };
}

function build_contour(z, contour_line_width) {
    return {
        'type': 'contour',
        'z': JSON.parse(z),
        'contours': {
            'coloring': 'lines',
            'start': 0,
            'end': 6,
            'size': 0.999,
        },
        'line': {'width': contour_line_width, 'smoothing':0},
        'showscale': false,
        'hoverinfo': 'skip',
        'colorscale': build_contour_color_scale(),
    };
}

function build_contour_color_scale() {
    /*This is hard-coded to the same look-up table used in ITK Snap.*/
    return [
        [0, 'rgba(0, 0, 0, 0)'],
        [0.167, 'rgba(255, 0, 0, 255)'],
        [0.333, 'rgba(0, 255, 0, 255)'],
        [0.5, 'rgba(0, 0, 255, 255)'],
        [0.667, 'rgba(255, 255, 0, 255)'],
        [0.833, 'rgba(0, 255, 255, 255)'],
        [1, 'rgba(255, 0, 255, 255)'],
    ];
}

function build_figure_layout() {
    return {
        'margin': {'b':1, 'l':1, 'r':1, 't':1},
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'template': '...',
        'xais': {'visible':false},
        'yaxis': {'visible':false},
    };
}