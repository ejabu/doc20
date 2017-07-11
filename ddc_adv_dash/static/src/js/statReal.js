odoo.define('ddc_adv_dash.statReal', function(require) {
    "use strict";

    var core = require('web.core');
    var form_common = require('web.form_common');
    var Model = require('web.DataModel');
    var time = require('web.time');
    var View = require('web.View');
    var widgets = require('web_calendar.widgets');
    var session = require('web.session');

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
            this._super(parent, dataset, view_id, options);
            this.view_id = view_id;
            this.view_type = 'statReal';
            this.model = new Model(dataset.model, {group_by_no_leaf: true});
            // this.model = dataset.model;
            this.dataset = dataset;
            this.data_loaded = $.Deferred();

            this.fields_view = {};
            this.view_id = view_id;
            this.measures = {};
            this.groupable_fields = {};


            this.domain;
            console.log('EJA3');
            console.log(this);
        },
        // willStart: function () {
        //         console.log('willStart');
        //     },
        start: function() {
            this.$table_container = this.$('.o-pivot-table');
            // var babang = this.model.call('ejaboy', [], {context: this.dataset.get_context()})
            var load_fields = this.model.call('ejaboy', [], {context: this.dataset.get_context()})
                                .then(this.start2.bind(this));
            console.log('load_fields');
            console.log(load_fields);
            console.log(this);
            return $.when(this._super(), load_fields).then(this.render_field_selection.bind(this));
        },
        start2: function() {
            this.$table_container = this.$('.o-pivot-table');
            var load_fields = this.model.call('fields_get', [], {context: this.dataset.get_context()})
                                .then(this.prepare_fields.bind(this));
            console.log('load_fields');
            console.log(load_fields);
            console.log(this);
            // return $.when(this._super(), load_fields).then(this.render_field_selection.bind(this));
        },

        do_search: function (domain, context, group_by) {
            //KEPANGGIL SETELAH RENTETAN start
            var self = this;
            console.log('self awal');
            console.log(this);
            this.domain = domain;
            console.log('self a22');
            console.log(this);
            var fields = ['external_status','weekly', 'count'];
            var groupbys = ['external_status', 'weekly'];

            console.log('do_search');
            console.log(domain, context, group_by);



            return session.rpc('/web/dataset/search_read', {
                model: 'stat.real',
                fields: ['external_status','weekly','count'],
                sort: 'id',

            }, {}).then(function (results) {
                console.log('resultsbaru');
                console.log(results);
                console.log('domain, context, group_by');
                console.log(domain, context, group_by);
                console.log('this');
                console.log(this);
                console.log('self');
                console.log(self);
                var tesresult = JSON.stringify(results['records']);
                console.log(tesresult);
                // return results.records;
            }, null);


            // return $.when.apply(null, groupbys.map(function (groupby) {
            //     console.log('load_data', fields, groupby, self.domain, self.context);
            //     return self.model.query(fields)
            //         .filter(self.domain)
            //         .context(self.context)
            //         .lazy(false)
            //         // .order_by(['probable_revenue'])
            //         .group_by(['id']);
            // })).then(function () {
            //     var data = Array.prototype.slice.call(arguments);
            //     console.log('data');
            //     console.log(data);
            //     self.prepare_data(data);
            // });
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
