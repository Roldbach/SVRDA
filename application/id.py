"""ID.

This module contains the static id of all widgets, sections
and pages used in the application.

Created by: Weixun Luo
Date: 15/04/2023
"""


# ----- Basic -----
keyboard_id = 'keyboard'
page_selection_section_id = 'page_selection_section'
home_page_link_id = 'home_page_link'
main_page_link_id = 'main_page_link'
help_modal_link_id = 'help_modal_link'
location_id = 'location'
help_modal_id = 'help_modal'
close_help_modal_button_id = 'close_help_modal_button'


# ----- Home Page -----
home_page_id = 'home_page'
title_id = 'home_page_title'
configuration_file_upload_id = 'home_page_configuration_file_upload'
configuration_store_id = 'home_page_configuration_store'
invalid_configuration_file_error_modal_id = 'home_page_invalid_configuration_file_error_modal'
close_invalid_configuration_file_error_modal_button_id = 'home_page_close_invalid_configuration_file_error_modal_button'


# ----- Main Page -----
main_page_id = 'main_page'
## ----- Main Menu Selection -----
main_menu_selection_dropdown_id = 'main_page_main_menu_selection_dropdown'
### ----- Transformation Menu -----
transformation_menu_id = 'main_page_transformation_menu'
translation_x_label_id = 'main_page_translation_x_label'
translation_y_label_id = 'main_page_translation_y_label'
translation_z_label_id = 'main_page_translation_z_label'
translation_step_size_slider_id = 'main_page_translation_step_size_slider'
rotation_x_label_id = 'main_page_rotation_x_label'
rotation_y_label_id = 'main_page_rotation_y_label'
rotation_z_label_id = 'main_page_rotation_z_label'
rotation_step_size_slider_id = 'main_page_rotation_step_size_slider'
undo_transformation_outline_button_id = 'main_page_undo_transformation_outline_button'
redo_transformation_outline_button_id = 'main_page_redo_transformation_outline_button'
optimise_transformation_outline_button_id = 'main_page_optimise_transformation_outline_button'
reset_transformation_outline_button_id = 'main_page_reset_transformation_outline_button'
### ----- Body Menu -----
body_menu_id = 'main_page_body_menu'
body_resampled_window_level_slider_id = 'main_page_body_resampled_window_level_slider'
body_resampled_window_width_slider_id = 'main_page_body_resampled_window_width_slider'
reset_body_menu_button_id = 'main_page_reset_body_menu_button'
body_visibility_switch_id = 'main_page_body_visibility_switch'
### ----- Organ Menu -----
organ_menu_id = 'main_page_organ_menu'
organ_resampled_threshold_slider_id = 'main_page_organ_resampled_threshold_slider'
organ_resampled_opacity_slider_id = 'main_page_organ_resampled_opacity_slider'
reset_organ_menu_button_id = 'main_page_reset_organ_menu_button'
organ_visibility_switch_id = 'main_page_organ_visibility_switch'
### ----- Slice Menu -----
slice_menu_id = 'main_page_slice_menu'
slice_window_level_slider_id = 'main_page_slice_window_level_slider'
slice_window_width_slider_id = 'main_page_slice_window_width_slider'
slice_opacity_slider_id = 'main_page_slice_opacity_slider'
reset_slice_menu_button_id = 'main_page_reset_slice_menu_button'

## ----- Mode Section -----
mode_selection_inline_radio_items_id = 'main_page_mode_selection_inline_radio_items'
macro_mode_id = 'main_page_macro_mode'
micro_mode_id = 'main_page_micro_mode'

## ----- Evaluation Section -----
evaluation_metric_selection_dropdown_id = 'main_page_evaluation_metric_selection_dropdown'
evaluation_result_label_id = 'main_page_evaluation_result_label'
evaluation_result_visibility_switch_id = 'main_page_evaluation_result_visibility_switch'

## ----- Support Menu Section -----
support_menu_section_id = 'main_page_support_menu_section'
support_menu_selection_dropdown_id = 'main_page_support_menu_selection_dropdown'
### ----- Contour Menu -----
contour_menu_id = 'main_page_contour_menu'
contour_line_width_slider_id = 'main_page_contour_line_width_slider'
### ----- Checkerboard Menu -----
checkerboard_menu_id = 'main_page_checkerboard_menu'
checkerboard_board_width_slider_id = 'main_page_checkerboard_board_width_slider'

## ----- Camera Section -----
camera_view_positive_x_outline_button_id = 'main_page_camera_view_positive_x_outline_button'
camera_view_negative_x_outline_button_id = 'main_page_camera_view_negative_x_outline_button'
camera_view_positive_y_outline_button_id = 'main_page_camera_view_positive_y_outline_button'
camera_view_negative_y_outline_button_id = 'main_page_camera_view_negative_y_outline_button'
camera_view_positive_z_outline_button_id = 'main_page_camera_view_positive_z_outline_button'
camera_view_negative_z_outline_button_id = 'main_page_camera_view_negative_z_outline_button'

## ----- Plot 3D Section -----
plot_3d_view_id = 'main_page_plot_3d_view'
body_representation_id = 'main_page_body_representation'
body_volume_id = 'main_page_body_volume'
organ_representation_id = 'main_page_organ_representation'
organ_volume_id = 'main_page_organ_volume'
slice_representation_type = 'main_page_slice_representation'
slice_volume_type = 'main_page_slice_volume'

## ----- Case Section -----
shift_previous_case_outline_button_id = 'main_page_shift_previous_case_outline_button'
shift_next_case_outline_button_id = 'main_page_shift_next_case_outline_button'
save_case_outline_button_id = 'main_page_save_case_outline_button'
case_selection_dropdown_id = 'main_page_case_selection_dropdown'
shift_previous_case_failure_error_modal_id = 'main_page_shift_previous_case_failure_error_modal'
shift_next_case_failure_error_modal_id = 'main_page_shift_next_case_failure_error_modal'
save_case_success_information_modal_id = 'main_page_save_case_success_information_modal'
save_case_failure_error_modal_id = 'main_page_save_case_failure_error_modal'
close_shift_previous_case_failure_error_modal_button_id = 'main_page_close_shift_previous_case_failure_error_modal_button'
close_shift_next_case_failure_error_modal_button_id = 'main_page_close_shift_next_case_failure_error_modal_button'
close_save_case_success_information_modal_button_id = 'main_page_close_save_case_success_information_modal_button'
close_save_case_failure_error_modal_button_id = 'main_page_close_save_case_failure_error_modal_button'

## ----- Main Plot 2D Section -----
slice_selection_dropdown_id = 'main_page_slice_selection_dropdown'
main_graph_mask_type_selection_dropdown_id = 'main_page_main_graph_mask_type_selection_dropdown'
main_graph_mask_format_selection_dropdown_id = 'main_page_main_grpah_mask_format_selection_dropdown'
main_graph_id = 'main_page_main_graph'
main_graph_main_figure_data_store_id = 'main_page_main_graph_main_figure_data_store'
main_graph_support_figure_data_store_id = 'main_page_main_graph_supportmain_figure_data_store'

## ----- Support Plot 2D Section -----
support_graph_image_type_selection_dropdown_id = 'main_page_support_image_type_selection_dropdown'
support_graph_mask_type_selection_dropdown_id = 'main_page_support_mask_type_selection_dropdown'
support_graph_mask_format_selection_dropdown_id = 'main_page_support_mask_format_selection_dropdown'
support_graph_id = 'main_page_support_graph'
support_graph_main_figure_data_store_id = 'main_page_support_graph_main_figure_data_store'
support_graph_support_figure_data_store_id = 'main_page_support_graph_support_figure_data_store'
### ----- Image Type -----
body_resampled_image_id = 'main_page_body_resampled_image'
checkerboard_id = 'main_page_checkerboard'
### ----- Mask Type -----
organ_resampled_mask_id = 'main_page_organ_resampled_mask'
evaluation_mask_id = 'main_page_evaluation_mask'
none_mask_id = 'main_page_none_mask'
### ----- Mask Format -----
contour_id = 'main_page_contour'
mask_id = 'main_page_mask'