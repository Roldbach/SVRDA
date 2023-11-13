/*Basic Clientside Callbacks.

This module adds basic clientside callbacks to the
application.

Changes to the following components must also be updated:
(1) HOME_PAGE_LINK_HREF (./presentation_layer/app_factory_plugin/layout/basic.py)
(2) MAIN_PAGE_LINK_HREF (./presentation_layer/app_factory_plugin/layout/basic.py)

Created by: Weixun Luo
Date: 05/05/2023
*/
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    basic: {
        select_page: function (path_name) {
            return [
                path_name == '/home' ? null : {'display':'none'},
                path_name == '/main' ? null : {'display':'none'},
            ];
        },
        open_modal: function (_) {return true;},
        close_modal: function (_) {return false;},
    },
});