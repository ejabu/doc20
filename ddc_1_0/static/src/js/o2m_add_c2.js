// (function () {
//     "use strict";
//     var form_relational = require('web.form_relational');
//     console.log(form_relational);
//     form_relational.X2ManyList.include({
//         pad_table_to : function() {
//             var self = this;
//             this._super.apply(this, arguments);
//             console.log('eja');
//             console.log(this, arguments);
//             self.$current.find('.oe_form_field_x2many_list_row_add a').text('Your Text');
//         }
//     });
// }) ();

// _____________________ done
// odoo.define('hehe', function (require) {
// 'use strict';
//
//     var core = require('web.core');
//     console.log("core.view_registry");
//     console.log(core.view_registry);
//     var eja = core.view_registry.get('one2many')
//     console.log(eja);
//     var form_relational = require('web.form_relational');
//     console.log(form_relational);
// });
var EJA = "haha"
    var core = require('web.core');

odoo.define('hehe', function(require) {
    'use strict';

    var core = require('web.core');
    var _t = core._t;

    var ListView = require('web.ListView');

    var Ninja = X2ManyList.extend({
        init: function() {
            this._super(false);
        },
        pad_table_to: function() {
            // Call the inherited version of dance()
            this._super();
            console.log('called');
            return
        },

    });
    // var X2ManyList = ListView.List.extend({
    //     pad_table_to: function(count) {
    //
    //         if (!this.view.is_action_enabled('create') || this.view.x2m.get('effective_readonly')) {
    //             this._super(count);
    //             return;
    //         }
    //
    //         this._super(count > 0
    //             ? count - 1
    //             : 0);
    //
    //         var self = this;
    //         var columns = _(this.columns).filter(function(column) {
    //             return column.invisible !== '1';
    //         }).length;
    //         if (this.options.selectable) {
    //             columns++;
    //         }
    //         if (this.options.deletable) {
    //             columns++;
    //         }
    //         console.log("this.$current");
    //         console.log(this.$current);
    //         console.log(this.$current.prev());
    //         console.log(columns);
    //         var $cell = $('<td>', {
    //             colspan: columns,
    //             'class': 'oe_form_field_x2many_list_row_add'
    //         }).append($('<a>', {href: '#'}).text(_t("WOI")).click(function(e) {
    //             e.preventDefault();
    //             e.stopPropagation();
    //             // FIXME: there should also be an API for that one
    //             if (self.view.editor.form.__blur_timeout) {
    //                 clearTimeout(self.view.editor.form.__blur_timeout);
    //                 self.view.editor.form.__blur_timeout = false;
    //             }
    //             self.view.save_edition().done(function() {
    //                 self.view.do_add_record();
    //             });
    //         }));
    //
    //         var $padding = this.$current.find('tr:not([data-id])');
    //         // $(".oe_form_field_x2many_list_row_add").parent()[0].remove()
    //
    //         var $newrow = $('<tr>').append($cell);
    //
    //         $padding.eq(-1).remove();
    //         if ($padding.length) {
    //             $padding.before($newrow);
    //         } else {
    //             this.$current.append($newrow);
    //         }
    //     },
    //
    // });
    console.log('meh');
});
