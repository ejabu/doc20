odoo.define('web_x2many_selectable.form_widgets', function (require) {
"use strict";
    var core = require('web.core');
    var Model = require('web.Model');
    var ListView = require('web.ListView');
    var _t = core._t;
    var QWeb = core.qweb;
    var FieldOne2Many = core.form_widget_registry.get('one2many');
    console.log("EJA LOADED");
    console.log(this.x2many_views.list);

    var X2ManySelectable = FieldOne2Many.extend({
		init: function() {
	        this._super.apply(this, arguments);
            console.log("EJA LOADED2");
            console.log(this);

            console.log(this.x2many_views.list);
            // this.x2many_views = {
            //     list: One2ManyListView,
            // };

	    },
	    start: function()
	    {
	    	this._super.apply(this, arguments);
            console.log("EJA LOADED3");
	    	var self=this;
	        // this.$el.find(".ep_button_confirm").click(function(){
	        // 	self.action_selected_lines();
	        // });
	   },

	//    action_selected_lines: function()
	//    {
	// 	var self = this;
	// 	var selected_ids = self.get_selected_ids_one2many();
	// 	if (selected_ids.length === 0)
	// 	{
	// 	    this.do_warn(_t("You must choose at least one record."));
	// 	    return false;
	// 	}
	// 	var model_obj=new Model(this.dataset.model); //you can hardcode model name as: new Model("module.model_name");
	// 	//you can change the function name below
	// 	model_obj.call('bulk_verify',[selected_ids],{context:self.dataset.context})
	// 	.then(function(result){
	// 	});
       //
	//    },
	//    get_selected_ids_one2many: function ()
	//    {
	//        var ids =[];
	//        this.$el.find('th.oe_list_record_selector input:checked')
	//                .closest('tr').each(function () {
	//                	ids.push(parseInt($(this).context.dataset.id));
	//        });
	//        return ids;
	//    },
	});

    var hehe = FieldOne2Many.extend({
		init: function() {
	        this._super.apply(this, arguments);
            console.log("EJA LOADED82");
            console.log(this);

	    },
    });


    var eja = ListView.List.extend({
    pad_table_to: function (count) {
        console.log('eja999');
        if (!this.view.is_action_enabled('create')) {
            this._super(count);
        } else {
            this._super(count > 0 ? count - 1 : 0);
        }

        // magical invocation of wtf does that do
        if (this.view.o2m.get('effective_readonly')) {
            return;
        }

        var self = this;
        var columns = _(this.columns).filter(function (column) {
            return column.invisible !== '1';
        }).length;
        if (this.options.selectable) { columns++; }
        if (this.options.deletable) { columns++; }

        if (!this.view.is_action_enabled('create')) {
            return;
        }

        var $cell = $('<td>', {
            colspan: columns,
            'class': 'oe_form_field_one2many_list_row_add'
        }).append(
            $('<a>', {href: '#'}).text(_t("Add an item"))
                .mousedown(function () {
                    // FIXME: needs to be an official API somehow
                    if (self.view.editor.is_editing()) {
                        self.view.__ignore_blur = true;
                    }
                })
                .click(function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    // FIXME: there should also be an API for that one
                    if (self.view.editor.form.__blur_timeout) {
                        clearTimeout(self.view.editor.form.__blur_timeout);
                        self.view.editor.form.__blur_timeout = false;
                    }
                    self.view.ensure_saved().done(function () {
                        self.view.do_add_record();
                    });
                }));

        var $padding = this.$current.find('tr:not([data-id]):first');
        var $newrow = $('<tr>').append($cell);
        if ($padding.length) {
            $padding.before($newrow);
        } else {
            this.$current.append($newrow)
        }
    }
});

	core.form_widget_registry.add('one2many', X2ManySelectable);
	return X2ManySelectable;
});
