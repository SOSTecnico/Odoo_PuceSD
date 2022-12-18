/** @odoo-module **/

import AbstractField from 'web.AbstractField';
import fieldRegistry from 'web.field_registry';


const DiasWidget = AbstractField.extend({
    template: "reservaciones.DiasWidget",
    init: function () {
        this.dias = moment.weekdays();
        this._super.apply(this, arguments)
        this.selectedDays = eval(this.value) || [];
        console.log(this)

    },
    _renderReadonly: function () {
        const dias = this.$el.find('input').toArray();

        dias.forEach(dia => {
            $(dia).on("click", function (ev) {
                return false;
            });
            if (this.selectedDays.some(_dia => _dia == $(dia).val())) {
                $(dia).prop("checked", true);
            }
        })
    },
    _renderEdit: function () {
        const dias = this.$el.find('input').toArray();
        let self = this;
        dias.forEach(dia => {
            $(dia).on("click", function (ev) {
                self.setDay(ev)
            });
            if (this.selectedDays.some(_dia => _dia == $(dia).val())) {
                $(dia).prop("checked", true)
            }
        })
    },
    setDay: function (ev) {

        var $target = $(ev.currentTarget);
        if ($target.prop("checked")) {
            this.selectedDays.push($target.val())
        } else {
            this.selectedDays = this.selectedDays.filter(d => d != $target.val())
        }
        this._setValue([...new Set(this.selectedDays)])
    }
})

fieldRegistry.add('dias_widget', DiasWidget)
