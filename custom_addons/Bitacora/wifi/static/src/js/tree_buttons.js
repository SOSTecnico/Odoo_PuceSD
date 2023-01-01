/** @odoo-module **/
var ListController = require('web.ListController');
var ListView = require('web.ListView');
var viewRegistry = require('web.view_registry');

const rpc = require("web.rpc")

var TreeButton = ListController.extend({
    buttons_template: 'wifi.buttons_tree',
    events: _.extend({}, ListController.prototype.events, {
        'click .recuperar_usuarios_radius': '_recuperar_usuarios_radius',
    }),
    _recuperar_usuarios_radius: async function () {
        $(".recuperar_usuarios_radius").prop("disabled",true)
        rpc.query({
            model:"wifi.estudiantes",
            method:"recuperar_usuarios_desde_radius",
        }).then(()=>{
            window.location.reload();
        })
    }
});

var TreeView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TreeButton,
    }),
});
viewRegistry.add('button_in_tree', TreeView);
