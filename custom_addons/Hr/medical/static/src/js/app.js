/** @odoo-module **/

var calendarEl = document.getElementById('calendar');


var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridWeek",
    locale: "es",
    headerToolbar: {
        left: "dayGridMonth,dayGridWeek",
        center: "title",
        right: "today prev next"
    },
    editable: true,
    selectable: true,
    weekends: false,
    allDaySlot: false,
    slotMinTime: "08:00",
    slotMaxTime: "18:00",
    unselectAuto: true,
    businessHours: [
        {
            daysOfWeek: [1, 2, 3, 4, 5],
            startTime: "08:00",
            endTime: "13:00"
        },
        {
            daysOfWeek: [1, 2, 3, 4, 5],
            startTime: "15:00",
            endTime: "18:00"
        },
    ],
    // dateClick: (arg) => {
    //
    //     console.log(calendar)
    //
    //     if (calendar.view.type == 'timeGrid')
    //         return
    //     calendar.changeView("timeGrid")
    //     calendar.unselect();
    // },
    select: (arg) => {

        calendar.changeView("timeGrid") ;
        calendar.unselect();

    },
});
calendar.render();
