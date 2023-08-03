/** @odoo-module **/

let problemas_tecnologicos = $("input[name='problemas']")
let txt_detalle_problemas = $("#txt_detalle_problemas")
let actividades = $("input[name='actividades']");
let txt_actividades_detalle = $("#actividades_detalle")


problemas_tecnologicos.on("change", (ev) => {
    if (problemas_tecnologicos.prop("checked")) {
        txt_detalle_problemas.show()
        txt_detalle_problemas.prop("required", true)
    } else {
        txt_detalle_problemas.hide();
        txt_detalle_problemas.prop("required", false)
        txt_detalle_problemas.val("")
    }
})


actividades.on("change", (ev) => {
    if (actividades.prop("checked")) {
        txt_actividades_detalle.show()
        txt_actividades_detalle.prop("required", true)
    } else {
        txt_actividades_detalle.hide();
        txt_actividades_detalle.prop("required", false)
        txt_actividades_detalle.val("")
    }
})

$("#select_nivel").select2()
$("#select_carrera").select2()