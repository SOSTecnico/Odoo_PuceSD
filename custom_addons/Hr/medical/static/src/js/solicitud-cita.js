odoo.define('medical.citas_medicas', function (require) {
    "use strict";

    const {Component} = owl;
    const {xml} = owl.tags;

    class MyComponent extends Component {
        static template = xml`
<div class="bg-info text-center p-2">
<b> Welcome to Odoo </b>
</div>`
    }

    owl.utils.whenReady().then(() => {
        const app = new MyComponent();
        app.mount(document.body);
            
    });

    console.log("ss")


});

// /** @odoo-module **/


// const rpc = require('web.rpc')
//
// const obtener_franja_horaria = rpc.query({
//     model: "medical.horario",
//     method: 'search_read',
//     args: []
// })
//
// const obtener_dias = rpc.query({
//     model: 'medical.dias',
//     method: 'search_read',
//     args: []
// })
//
// var dias = [];
// var horario = {};
// Promise
//     .all([obtener_dias, obtener_franja_horaria])
//     .then((result) => {
//
//         dias = result[0].map(d => ({id: d.id, dia: d.name}));
//         const h = result[1][0]
//
//         let temp_hora_inicio_1 = moment.duration(h.hora_inicio_1, 'h')
//         let temp_hora_inicio_2 = moment.duration(h.hora_inicio_2, 'h')
//
//         let hora_fin_1 = moment.duration(h.hora_fin_1, 'h')
//         let hora_fin_2 = moment.duration(h.hora_fin_2, 'h')
//         const primera_jornada = [];
//         const segunda_jornada = [];
//
//         while (temp_hora_inicio_1 < hora_fin_1) {
//
//             let h_inicio = temp_hora_inicio_1;
//             let h_fin = h_inicio.clone().add(30, 'm')
//
//             primera_jornada.push({h_inicio, h_fin})
//
//             temp_hora_inicio_1 = h_fin
//         }
//
//         while (temp_hora_inicio_2 < hora_fin_2) {
//             let h_inicio = temp_hora_inicio_2;
//             let h_fin = h_inicio.clone().add(30, 'm')
//             segunda_jornada.push({h_inicio, h_fin})
//
//             temp_hora_inicio_2 = h_fin
//         }
//
//         horario.primera_jornada = primera_jornada;
//         horario.segunda_jornada = segunda_jornada;
//         horario.dias = h.dias.map(d => dias.filter(dia => dia.id == d)[0]);
//
//     }).then(() => {
//     $("#fecha").on("change", function () {
//         $("#primera_jornada").empty();
//         $("#segunda_jornada").empty();
//         if (!horario.dias.some(d => d.dia == moment(this.value).format('dddd'))) {
//             $("#primera_jornada").append('No Hay horarios disponibles para la fecha seleccionada');
//             return;
//         }
//
//         const domain = [
//             ['date_start', '>=', moment.utc(this.value).format('Y-MM-DD 00:00:00')],
//             ['date_stop', '<=', moment.utc(this.value).format('Y-MM-DD 23:59:59')]
//         ]
//
//         rpc.query({
//             model: 'medical.citas',
//             method: 'search_read',
//             args: [domain]
//         })
//             .then((res) => {
//
//                 const reservas = res.map(c => moment.duration(moment.utc(c.date_start).tz('America/Guayaquil').format('HH:mm')))
//
//                 horario.primera_jornada.forEach((h) => {
//
//                     const exist = reservas.some(r => r.asMilliseconds() == h.h_inicio.asMilliseconds())
//
//                     const li = $('<li>')
//                         .addClass("list-group-item list-group-item-action selection-hour")
//                         .append(`
//                         ${moment.utc(h.h_inicio.asMilliseconds()).format("HH:mm")}
//                         -
//                         ${moment.utc(h.h_fin.asMilliseconds()).format("HH:mm")}
//                         `);
//                     if (exist) {
//                         li.addClass('list-group-item-danger')
//                         li.append(" - Reservado")
//                     }
//                     $("#primera_jornada").append(li)
//                 });
//
//                 horario.segunda_jornada.forEach((h) => {
//
//                     const exist = reservas.some(r => r.asMilliseconds() == h.h_inicio.asMilliseconds())
//
//                     const li = $('<li>')
//                         .addClass("list-group-item list-group-item-action selection-hour")
//                         .append(`
//                         ${moment.utc(h.h_inicio.asMilliseconds()).format("HH:mm")}
//                         -
//                         ${moment.utc(h.h_fin.asMilliseconds()).format("HH:mm")}
//                         `);
//                     if (exist) {
//                         li.addClass('list-group-item-danger')
//                         li.append(" - Reservado")
//                     }
//                     $("#segunda_jornada").append(li)
//
//                 })
//
//                 $(".selection-hour").on("click", function (e) {
//                         $(".selection-hour").removeClass("active");
//                         if ($(this).hasClass('list-group-item-danger')) {
//                             e.preventDefault();
//                             return;
//                         }
//                         $(this).addClass("active");
//                     }
//                 )
//
//
//             });
//
//     });
//
// })