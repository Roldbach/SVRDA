"""Basic Plugin of App Factory.

This module contains the implementation of App Factory
Plugin. It defines the basic layout and structure of the
application.

Created by: Weixun Luo
Date: 15/04/2023
"""
from __future__ import annotations

from dash import dcc
import dash_bootstrap_components as dbc

from application import id
from utils import widget_utils


# Please update this if changes are maded to README.md in the repository.
HELP_MODAL_CONTENT = '''
### Transformation
- **Rigid transformations** with six degrees of freedom (three translation and
three rotation parameters) can be applied to adjust the poses of 2D slices.
- Transformations can be computed with respect to:
    - Patient Coordinate System: A static RAS+ coordinate system
    - Slice Coordinate System: A dynamic coordinate system based on the
    real-time pose of the currently selected slice
- Please control transformations using the following keyboard shortcuts:
    - Translations in the Patient Coordinate System:
        - x axis: **a**, **d**
        - y axis: **w**, **s**
        - z axis: **q**, **e**
    - Translations in the Slice Coordinate System:
        - x axis: **j**, **l**
        - y axis: **i**, **k**
        - z axis: **u**, **o**
    - Rotations in the Slice Coordinate System:
        - x axis: **Shift+W**, **Shift+S**
        - y axis: **Shift+A**, **Shift+D**
        - z axis: **Shift+Q**, **Shift+E**

### Mode
- Modes are introduced to adjust the granularity of transformation control:
    - Macro Mode:
        - **All 2D slices** are visible.
        - Transformations are applied to **all 2D slices** simultaneously.
    - Micro Mode:
        - Only **the selected 2D slice** is visible.
        - Transformations are exclusively applied to **the selected 2D slice**.

### Alignment Quantification
- The alignment between data is quantitatively monitored in real-time by
measuring the difference between the selected slice and its corresponding 2D
cross-section image resampled from the 3D volume.
- The following evaluation metrics have been implemented:
    - Normalised Mutual Information (NMI): A **similarity** metric that measure
    the ratio of the sum of the marginal entropy between the images.
    - Sum of Absolute Difference (SAD): A **difference** metric that measures
    the sum of the absolute difference between pixel values between the images.

### Case and Saving
- To shift to a new case, please:
    - use **Previous/Next** buttons to go through each case one-by-one.
    - select the new case ID in the dropdown showing the current case ID.
- The current case is **auto-saved** before shifting to a new case.
- **Please notice that directly closing the browser won't save the current case.
To save the last case, please manually press the Save button.**

### Note
- [Github Repository](https://github.com/Roldbach/SVRDA)
'''
HOME_PAGE_LINK_CHILDREN = 'Home'
HOME_PAGE_LINK_HREF = '/home'
MAIN_PAGE_LINK_CHILDREN = 'Main'
MAIN_PAGE_LINK_HREF = '/main'
HELP_MODAL_LINK_CHILDREN = 'Help'


class PageSelectionSectionPlugin:
    """Plugin that defines the layout of Page Selection Section."""

    def _build_page_selection_section(self) -> dbc.Row:
        return dbc.Row(
            id = id.page_selection_section_id,
            children = (
                dbc.Col(self._build_page_selector(), width=4),
                dbc.Col(self._build_location()),
                dbc.Col(self._build_help_modal()),
            ),
        )
    
    def _build_page_selector(self) -> dbc.Nav:
        return dbc.Nav((
            dbc.NavLink(
                id = id.home_page_link_id,
                children = HOME_PAGE_LINK_CHILDREN,
                href = HOME_PAGE_LINK_HREF,
            ),
            dbc.NavLink(
                id = id.main_page_link_id,
                children = MAIN_PAGE_LINK_CHILDREN,
                href = MAIN_PAGE_LINK_HREF,
            ),
            dbc.NavLink(
                id = id.help_modal_link_id,
                children = HELP_MODAL_LINK_CHILDREN,
                n_clicks = 0,
            ),
        ))
    
    def _build_location(self) -> dcc.Location:
        return widget_utils.build_location(id.location_id)

    def _build_help_modal(self) -> dbc.Modal:
        return widget_utils.build_help_modal(
            modal_id = id.help_modal_id,
            close_button_id = id.close_help_modal_button_id,
            children = widget_utils.build_markdown(HELP_MODAL_CONTENT),
        )
