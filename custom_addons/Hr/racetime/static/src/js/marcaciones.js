/** @odoo-module **/
var ListController = require('web.ListController');
var ListView = require('web.ListView');
var viewRegistry = require('web.view_registry');

const rpc = require("web.rpc")

var TreeButton = ListController.extend({
    buttons_template: 'racetime.buttons_tree',
    events: _.extend({}, ListController.prototype.events, {
        'click .obtener_marcaciones': '_obtener_marcaciones',
        'click .obtener_marcaciones_al_dia': '_obtener_marcaciones_al_dia'
    }),
    _obtener_marcaciones: async function () {
        $(".obtener_marcaciones").prop("disabled", true)
        rpc.query({
            model: "racetime.detalle_marcacion",
            method: "obtener_marcaciones",
        }).then(() => {
            window.location.reload();
        })
    },
    _obtener_marcaciones_al_dia: async function () {
        $(".obtener_marcaciones_al_dia").prop("disabled", true)
        rpc.query({
            model: "racetime.detalle_marcacion",
            method: "obtener_marcaciones_diarias",
        }).then(() => {
            window.location.reload();
        })
    }
});

var TreeView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TreeButton,
    }),
});
viewRegistry.add('marcaciones_buttons_tree', TreeView);
