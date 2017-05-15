/* Copyright 2016 Onestein
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('web_x2many_delete_all.Mixin', function (require) {
    "use strict";
    var core = require('web.core');

    var X2ManyListDeleteAllMixin = {
        events: {
            'click th.oe_list_record_delete': 'btn_delete_all_clicked'
        },
        reload_current_view: function() {
            var self = this;
            var res = this._super.apply(this, arguments);


            res.then(function() {
                self.clearAdd();

            });
            return res
        },
        clearAdd: function() {
            console.log('EEEEEEEEEEEEEE');
            console.log(this.dataset.x2m.options);
            if (this.dataset.x2m.options && this.dataset.x2m.options.addLabel) {
                this.$('.oe_form_field_x2many_list_row_add a').text(this.dataset.x2m.options.addLabel)
            }
            // console.log(this.$('.oe_form_field_x2many_list_row_add a'));
            // this.$('.oe_form_field_x2many_list_row_add a').text('hehe')
            // this.$('.oe_form_field_x2many_list_row_add').remove()
        },
        // btn_delete_all_clicked: function() {
        //     if (this.get('effective_readonly')) return;
        //     this.delete_all();
        // },
        // delete_all: function() {
        //     this.viewmanager.views.list.controller.do_delete(this.dataset.ids);
        // }
    }

    core.form_widget_registry.get('many2many').include(X2ManyListDeleteAllMixin);
    core.form_widget_registry.get('one2many').include(X2ManyListDeleteAllMixin);

    return X2ManyListDeleteAllMixin;
});
