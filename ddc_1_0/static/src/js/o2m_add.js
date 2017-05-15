
odoo.define('web_x2many_list_add_label.Mixin', function (require) {
    "use strict";
    var core = require('web.core');

    var X2manyListAddLabel = {
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
            if (this.dataset.x2m.options && this.dataset.x2m.options.addLabel) {
                this.$('.oe_form_field_x2many_list_row_add a').text(this.dataset.x2m.options.addLabel)
            }
        },

    }

    core.form_widget_registry.get('many2many').include(X2manyListAddLabel);
    core.form_widget_registry.get('one2many').include(X2manyListAddLabel);

    return X2manyListAddLabel;
});
