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
        template: "statRealTemplate",
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

            this.filtered_result;


            this.domain;
        },
        // willStart: function () {
        //         console.log('willStart');
        //     },
        start: function() {
            //START HANYA DIEKSEKUSI SEKALI SETELAH MENU ITEM DI KLIK
            this.$table_container = this.$('.stat-real-mainbox');
            // var babang = this.model.call('ejaboy', [], {context: this.dataset.get_context()})
            var load_fields = this.model.call('ejaboy', [], {context: this.dataset.get_context()})
                                .then(this.after_start.bind(this));
            return $.when(this._super(), load_fields).then(this.render_field_selection.bind(this));
        },
        after_start: function() {
            //START2 HANYA DIEKSEKUSI SEKALI SETELAH MENU ITEM DI KLIK

            var load_fields = this.model.call('fields_get', [], {context: this.dataset.get_context()})
                                .then(this.prepare_fields.bind(this));
            // tidak perlu declare return $.when lagi
            // hal ini dikarenakan sudah didefinisikan di start.
            // return $.when(this._super(), load_fields).then(this.render_field_selection.bind(this));
        },

        do_search: function (domain, context, group_by) {
            //Terpanggil secara otomastis setelah Rentetan Start
            //Sepertinya karena model.call('fields_get')

            this.data_loaded = this.load_data(true);
            console.log('Do Search');
            var self = this;
            this.domain = domain;
            var fields = [
                        'week_name',
                        'week_date',
                        'ifi',
                        'ifr',
                        'ifa',
                        'afc',
                        'def_ifr',
                        'def_ifa',
                        'def_afc',
                        'diff_ifi',
                        'diff_ifr',
                        'diff_ifa',
                        'diff_afc'
            ];

            return session.rpc('/web/dataset/search_read', {
                model: 'stat.real',
                fields: fields,
                sort: 'week_date',

            }, {}).then(function (results) {
                console.log(domain, context, group_by);
                // var string_res = JSON.stringify(results['records']);
                var filtered_result = filter_by_js(results['records'], domain)
                // console.log(filtered_array);
                self.filtered_result = filtered_result;
                self.do_show()

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


        do_show: function () {
            var self = this;
            console.log('do_show');

            // var context = {fields: _.chain(this.groupable_fields).pairs().sortBy(function(f){return f[1].string;}).value()};
            var context = {}
            console.log(this.$table_container);
            // this.$field_selection.html(QWeb.render('ejacoy', context));
            var $fragment = $(document.createDocumentFragment());
            // var $table = $('<table>')
            //     .addClass('table table-hover table-condensed')
            //     .appendTo($fragment);
            // console.log($table);
            // var $tbody = $('<tbody>').appendTo($table);
            // var $thead = $('<thead>').appendTo($table);
            // console.log($table);
            console.log('$fragment');
            console.log($fragment);

            var $cell = $('<div>')
                    .text('ejaaaaaaaaaaaaa')
            $fragment.append($cell);

            this.$table_container.empty().append($fragment);

            // core.bus.on('click', self, function () {
            //     self.$field_selection.find('ul').first().hide();
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
            var self = this;
            // var groupable_types = ['many2one', 'char', 'boolean',
            //                        'selection', 'date', 'datetime'];
           this.fields = fields;
        //    console.log('PREPAREFIELDS');
        //    console.log(this);
            _.each(fields, function (field, name) {
                if ((name !== 'id') && (field.store === true)) {
                    if (field.type === 'integer' || field.type === 'float' || field.type === 'monetary') {
                        self.measures[name] = field;
                    }
                    // if (_.contains(groupable_types, field.type)) {
                    //     self.groupable_fields[name] = field;
                    // }
                }
            });
            this.measures.__count__ = {string: _t("Count"), type: "integer"};

        },

    });

    core.view_registry.add('statReal', statReal);
    return statReal;
});
