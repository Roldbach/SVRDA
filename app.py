"""App.

This module is used to start the application.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations
import argparse
import sys

import dash
import dash_bootstrap_components as dbc

from presentation_layer import app_factory


APP = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
FACTORY = app_factory.AppFactory()
HOST_LOCAL = '127.0.0.1'
HOST_REMOTE = ''
IS_LOCAL = True


def main() -> int:
    _start_up_application()
    _run_application()
    return 0

def _start_up_application() -> None:
    APP.layout = FACTORY.build_app_layout(_get_configuration_file_path())
    FACTORY.add_callback()

def _get_configuration_file_path() -> str | None:
    argument = _parse_argument()
    return argument.configuration

def _parse_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=globals()['__doc__'])
    parser.add_argument('-c', '--configuration', type=str)
    return parser.parse_args()

def _run_application() -> None:
    APP.run(host=_select_host(), debug=False)

def _select_host() -> str:
    return HOST_LOCAL if IS_LOCAL else HOST_REMOTE


if __name__ == '__main__':
    sys.exit(main())
