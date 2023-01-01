/** @odoo-module **/
var ListController = require('web.ListController');
var ListView = require('web.ListView');
var viewRegistry = require('web.view_registry');

const TreeButton = ListController.extend({
    buttons_template: "wifi.docentes_buttons_template",
})

const DocentesTreeView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TreeButton
    })
})

viewRegistry.add("docentes_tree_buttons", DocentesTreeView)