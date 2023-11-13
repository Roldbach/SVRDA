"""Basic Callback Plugin of App Factory.

This module contains the implementation of App Factory
Plugin. It adds basic callbacks to the application.

Created by: Weixun Luo
Date: 24/04/2023
"""
from __future__ import annotations

import dash

from application import id


class BasicCallbackPlugin:
    """Plugin that adds basic callbacks."""

    def _add_basic_callback(self) -> None:
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'select_page',
            ),
            dash.Output(id.home_page_id, 'style'),
            dash.Output(id.main_page_id, 'style'),
            dash.Input(id.location_id, 'pathname'),
            prevent_initial_call = True,
        )

        # Open Help Modal
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'open_modal',
            ),
            dash.Output(id.help_modal_id, 'is_open'),
            dash.Input(id.help_modal_link_id, 'n_clicks'),
            prevent_initial_call = True,
        )

        # Close Help Modal
        dash.clientside_callback(
            dash.ClientsideFunction(
                namespace = 'basic',
                function_name = 'close_modal',
            ),
            dash.Output(id.help_modal_id, 'is_open', allow_duplicate=True),
            dash.Input(id.close_help_modal_button_id, 'n_clicks'),
            prevent_initial_call = True,
        )