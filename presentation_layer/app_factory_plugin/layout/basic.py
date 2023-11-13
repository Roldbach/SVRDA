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
### Transformation ###
- Currently, **rigid transformations** can be applied to 2D quantitative
parametric maps to adjust their positions. These include translation and
rotation in X, Y, Z axis for a total of **6** degrees of freedom.
- Scanner Coordinate System (static) used in the App coincides with standard
**NiFTI** coordinate system , which has directional code **LAS**.
- Slice Coordinate System (dynamic) used in the App depends on the
**real-time** orientation of **the selected 2D quantitative parametric map**.

### Transformation Control ###
- Transformations can be controlled using the following keyboard shortcuts:
    - Translations in Scanner Coordinate System:
        - x axis: **a**, **d**
        - y axis: **w**, **s**
        - z axis: **q**, **e**
    - Translations in Slice Coordinate System:
        - x axis: **j**, **l**
        - y axis: **i**, **k**
        - z axis: **u**, **o**
    - Rotations in Slice Coordinate System:
        - x axis: **Shift + W**, **Shift + S**
        - y axis: **Shift + A**, **Shift + D**
        - z axis: **Shift + Q**, **Shift + E**

### Mode ###
- We introduce different modes to allow flexible control of transformations.
    - Macro Mode
        - **All 2D quantitative parametric maps** are visible within the 3D plot.
        - Transformations can be applied to **all 2D quantitative parametric
        maps** as group effects.
        - Rotations are done in **Scanner Coordinate System** only and **the
        mean centroid of all 2D quantitative parametric maps** is chosen as the
        rotation centre.
    - Micro Mode
        - Only **the selected 2D quantitative parametric map** is visible within
        the 3D plot.
        - Transformations can only be applied to **the selected 2D quantitative
        parametric map**.
        - Rotations are done in **Slice Coordinate System** depending on the
        selected 2D quantitative parametric map and its **centroid** is chosen as
        the rotation centre.

### Evaluation ###
- Evaluation are served as a support to help users determine whether 2D
quantitative parametric maps are well aligned with the 3D volume at the current
position or not.
- Evaluation is done by measuring the similarity/difference between **the
selected 2D quantitative map** and **the corresponding 2D resampled image from
the 3D volume**.
- For manual registration, we encourage users to mainly rely on exptertise and
knowledge during decision making and only use this as a supplementary reference.
- The following evaluation metrics are available in the GUI:
    - Normalised Mutual Information (NMI): A **similarity** measurement that
    measures the mutual dependence between 2 images. This is recommended for
    **multi-modal data**.
    - Sum of Absolute Difference (SAD): A **difference** measurement that
    measures the pixel-wise difference between 2 images.

### Case Control ###
- To shift to a new case, you could:
    - use **Previous** and **Next** buttons to go through each case one-by-one.
    - click the dropdown showing the current case id and select the new case id.
- The current case is **auto-saved** before shifting to a new case.
- **Please notice that directly closing the browser won't save the current case.
To save the last case, please manually press the Save button.**

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