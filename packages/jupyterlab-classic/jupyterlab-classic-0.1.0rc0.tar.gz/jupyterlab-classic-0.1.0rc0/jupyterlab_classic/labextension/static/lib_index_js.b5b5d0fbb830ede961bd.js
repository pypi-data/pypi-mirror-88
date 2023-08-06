(self["webpackChunk_jupyterlab_classic_lab_extension"] = self["webpackChunk_jupyterlab_classic_lab_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => __WEBPACK_DEFAULT_EXPORT__
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The command IDs used by the application plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    /**
     * Toggle Top Bar visibility
     */
    CommandIDs.openClassic = 'jupyterlab-classic:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * A notebook widget extension that adds a jupyterlab classic button to the toolbar.
 */
class ClassicButton {
    /**
     * Instantiate a new ClassicButton.
     * @param commands The command registry.
     */
    constructor(commands) {
        this._commands = commands;
    }
    /**
     * Create a new extension object.
     */
    createNew(panel) {
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            tooltip: 'Open with JupyterLab Classic',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.jupyterIcon,
            onClick: () => {
                this._commands.execute(CommandIDs.openClassic);
            }
        });
        panel.toolbar.insertAfter('cellType', 'jupyterlabClassic', button);
        return button;
    }
}
/**
 * A plugin for the checkpoint indicator
 */
const openClassic = {
    id: '@jupyterlab-classic/lab-extension:open-classic',
    autoStart: true,
    optional: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.INotebookTracker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, notebookTracker, palette, menu, labShell) => {
        // TODO: do not activate if already in a IClassicShell?
        if (!notebookTracker || !labShell) {
            // to prevent showing the toolbar button in JupyterLab Classic
            return;
        }
        const { commands, docRegistry, shell } = app;
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl();
        const isEnabled = () => {
            return (notebookTracker.currentWidget !== null &&
                notebookTracker.currentWidget === shell.currentWidget);
        };
        commands.addCommand(CommandIDs.openClassic, {
            label: 'Open in JupyterLab Classic',
            execute: () => {
                const current = notebookTracker.currentWidget;
                if (!current) {
                    return;
                }
                const { context } = current;
                window.open(`${baseUrl}classic/notebooks/${context.path}`);
            },
            isEnabled
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.openClassic, category: 'Other' });
        }
        if (menu) {
            menu.viewMenu.addGroup([{ command: CommandIDs.openClassic }], 1);
        }
        const classicButton = new ClassicButton(commands);
        docRegistry.addWidgetExtension('Notebook', classicButton);
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [openClassic];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b5b5d0fbb830ede961bd.js.map