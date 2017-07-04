odoo.define('ddc_adv_dash.statReal', function(require) {
    "use strict";

    var core = require('web.core');
    var form_common = require('web.form_common');
    var Model = require('web.DataModel');
    var time = require('web.time');
    var View = require('web.View');
    var widgets = require('web_calendar.widgets');
    var _ = require('_');
    var $ = require('$');

    var _t = core._t;
    var _lt = core._lt;
    var QWeb = core.qweb;

    function isNullOrUndef(value) {
        return _.isUndefined(value) || _.isNull(value);
    }

    var statReal = View.extend({
        template: "statReal",
        display_name: _lt('statReal'),
        icon: 'fa-clock-o',

        init: function(parent, dataset, view_id, options) {
            this._super(parent);
            this.view_id = view_id;
            this.view_type = 'statReal';
            this.model = new Model(dataset.model, {group_by_no_leaf: true});
            // this.model = dataset.model;
            this.dataset = dataset;
            this.fields_view = {};
            this.view_id = view_id;
            this.measures = {};
            this.groupable_fields = {};
            console.log('EJA3');
            console.log(this);
        },

        start: function() {
            this.$table_container = this.$('.o-pivot-table');

            var load_fields = this.model.call('fields_get', [], {context: this.dataset.get_context()})
                                .then(this.prepare_fields.bind(this));
            console.log('load_fields');
            console.log(load_fields);
            console.log(this);
            return $.when(this._super(), load_fields).then(this.render_field_selection.bind(this));
        },

        render_field_selection: function () {
            var self = this;
            console.log('render_field_selection');

            // var context = {fields: _.chain(this.groupable_fields).pairs().sortBy(function(f){return f[1].string;}).value()};
            var context = {}
            this.$field_selection = this.$('.ejao-field-selection');
            console.log(this.$field_selection);
            this.$field_selection.html(QWeb.render('ejacoy', context));
            // core.bus.on('click', self, function () {
            //     self.$field_selection.find('ul').first().hide();
            // });
        },

        prepare_fields: function (fields) {
            var self = this,
                groupable_types = ['many2one', 'char', 'boolean',
                                   'selection', 'date', 'datetime'];
           this.fields = fields;
           console.log('PREPAREFIELDS');
           console.log(this);
            _.each(fields, function (field, name) {
                if ((name !== 'id') && (field.store === true)) {
                    if (field.type === 'integer' || field.type === 'float' || field.type === 'monetary') {
                        self.measures[name] = field;
                    }
                    if (_.contains(groupable_types, field.type)) {
                        self.groupable_fields[name] = field;
                    }
                }
            });
            this.measures.__count__ = {string: _t("Count"), type: "integer"};

        },

    });

    core.view_registry.add('statReal', statReal);
    return statReal;
});
