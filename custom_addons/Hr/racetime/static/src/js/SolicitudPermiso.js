/** @odoo-module **/

$("#sw_todo_el_dia").on("change", (ev) => {
    $(".horas-container").prop("hidden", ev.target.checked);
    $(".horas-container input").prop("required", !ev.target.checked)
    $(".horas-container input").val("")
})

$("#fecha_inicio").on("change", () => {
    if ($("#fecha_fin").val() == "")
        $("#fecha_fin").val($("#fecha_inicio").val())
})
