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

odoo.define('hehe', function (require) {
'use strict';

    var core = require('web.core');
    var _t = core._t;

    // console.log("core.view_registry");
    // console.log(core.view_registry);
    // var eja = core.form_widget_registry.get('one2many')
    // console.log(eja);
    // console.log(eja);


    var ListView = require('web.ListView');
    // console.log(ListView);
    // console.log(ListView.List);
    //PASTI INCLUDE
    console.log(ListView.List.prototype.pad_table_to);

    delete ListView.List.prototype.pad_table_to
    console.log(ListView.List.prototype.pad_table_to);

    // var X2ManyList = ListView.List.include({
    ListView.List.prototype = {

        pad_table_to: function (count) {
    if (!this.view.is_action_enabled('create') || this.view.x2m.get('effective_readonly')) {
        this._super(count);
        return;
    }

    this._super(count > 0 ? count - 1 : 0);

    var self = this;
    var columns = _(this.columns).filter(function (column) {
        return column.invisible !== '1';
    }).length;
    if (this.options.selectable) { columns++; }
    if (this.options.deletable) { columns++; }
    console.log("this.$current");
    console.log(this.$current);
    console.log(this.$current.prev());
    var $cell = $('<td>', {
        colspan: columns,
        'class': 'oe_form_field_x2many_list_row_add'
    }).append(
        $('<a>', {href: '#'}).text(_t("WOI"))
            .click(function (e) {
                e.preventDefault();
                e.stopPropagation();
                // FIXME: there should also be an API for that one
                if (self.view.editor.form.__blur_timeout) {
                    clearTimeout(self.view.editor.form.__blur_timeout);
                    self.view.editor.form.__blur_timeout = false;
                }
                self.view.save_edition().done(function () {
                    self.view.do_add_record();
                });
            }));

    // var $old = this.$current.find('oe_form_field_x2many_list_row_add');
    // $old.remove()
    var $padding = this.$current.find('tr:not([data-id]):first');

    var $newrow = $('<tr>').append($cell);

        $padding.before($newrow);

    if ($padding.length) {
        $padding.before($newrow);
    } else {
        this.$current.append($newrow);
    }
},
            // pad_table_to : function() {
            //     this._super.apply(this, arguments);
            //     console.log('self');
            //     console.log(self);
            //     console.log('this');
            //     console.log(this);
            //     var wow = this.$current.find(".oe_form_field_x2many_list_row_add")
            //     console.log(wow);
            //     wow.text('as')
            //     // var self = this;
            //     // console.log('arguments');
            //     // console.log(arguments);
            //     // // this._super.apply(this, arguments);
            //     //
            //     // if (this.$current.length > 0){
            //     //     console.log('hore');
            //     //     // this.$current.find(".oe_form_field_x2many_list_row_add a")[0].text="haha"
            //     // }
            //     // var wow = this.$current.find(".oe_form_field_x2many_list_row_add a")
            //     // console.log(wow);
            //     // console.log(wow.text);
            //     // console.log(wow[0]);
            //     // if (wow){
            //     //     console.log('hore2');
            //     //     wow.text("haha")
            //     //     // wow[0].text("haha")
            //     //     // wow.innerHTML="haha"
            //     //     // this.$current.find(".oe_form_field_x2many_list_row_add a")[0].text="haha"
            //     //
            //     //     // if (wow[0]){
            //     //     //     console.log('hore3');
            //     //     //     wow.text="haha"
            //     //     // }
            //     // }
            //
            //
            // }
        }
        console.log('meh');






});
