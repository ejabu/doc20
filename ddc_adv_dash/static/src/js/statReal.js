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

            this.dataset = dataset;
            this.data_loaded = $.Deferred();

            this.fields_view = {};
            this.measures = {};
            this.groupable_fields = {};
            this.filtered_result;
            this.domain;
        },

        start: function() {
            //START HANYA DIEKSEKUSI SEKALI SETELAH MENU ITEM DI KLIK
            this.$table_container = this.$('.o-pivot-table');
            // var babang = this.model.call('ejaboy', [], {context: this.dataset.get_context()})
            var load_fields = this.model.call('fetch_report_stat_real', [], {context: this.dataset.get_context()})
            return $.when(this._super(), load_fields)
        },

        load_data: function (update) {
            // console.log('Querying to Database');
            var self = this;
            self.domain = this.domain;

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
                // console.log('Query Succeed');
                // var string_res = JSON.stringify(results['records']);
                var filtered_result = filter_by_js(results['records'], self.domain)
                self.filtered_result = filtered_result;
                self.do_show()
                // return results.records;
            }, null);

        },
        do_search: function (domain, context, group_by) {
            //Terpanggil secara otomastis setelah Rentetan Start
            //Sepertinya karena model.call('fields_get')
            this.data_loaded = this.load_data(true);
            this.domain = domain;

        },


        display_table: function () {
            // console.log("RENDER");
            var context = {}
            // this.$field_selection.html(QWeb.render('ejacoy', context));
            var $fragment = $(document.createDocumentFragment());
            var $mainbox = $('<div>')
                .addClass('str-main-box')
                .appendTo($fragment);
            var $table = $('<table>')
                .addClass('table')
                // .addClass('table table-hover table-condensed')
                .appendTo($mainbox);
            var $thead = $('<thead>').appendTo($table);
            var $tbody = $('<tbody>').appendTo($table);
            this.draw_headers($thead);
            this.draw_content($tbody);
            this.$table_container.empty().append($fragment);
        },
        draw_headers: function($thead){
            var $row, $cell;
            var self = this
            $row = $('<tr>');
            $cell = $('<th>')
                .text("")
                .addClass('str-cell-blank')
                .attr('colspan', 2);
            $row.append($cell);
            self.filtered_result.map(function (rec) {
                $cell = $('<th>')
                    .text(rec.week_name)
                    .addClass('str-header')
                    .attr('colspan', 4);
                $row.append($cell);

            })
            $thead.append($row);

        },
        draw_content: function($tbody){
            var $row, $cell;
            var self = this
            //Kolom Pertama
            $row = $('<tr>');
            $cell = $('<td>')
                .text("")
                .addClass('str-cell-blank')
                .attr('colspan', 2);
            $row.append($cell);
            self.filtered_result.map(function (rec) {
                ["IFI", "IFR", "IFA", "AFC"].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .attr('colspan', 1);
                    $row.append($cell);
                })
            })
            $tbody.append($row);
            //Kolom Kedua
            $row = $('<tr>');
            $cell = $('<td>')
                .text("Jumlah Dokumen")
                .addClass('str-body-side')
                .attr('colspan', 2);
            $row.append($cell);
            self.filtered_result.map(function (rec) {
                [rec.ifi, rec.ifr, rec.ifa, rec.afc].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .attr('colspan', 1);
                    $row.append($cell);
                })
            })
            $tbody.append($row);
            //Kolom Ketiga
            $row = $('<tr>');
            $cell = $('<td>')
                .text("A")
                .addClass('str-body-side')
                .attr('colspan', 2);
            $row.append($cell);
            self.filtered_result.map(function (rec) {
                ["", rec.def_ifr, rec.def_ifa, rec.def_afc].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .attr('colspan', 1);
                    $row.append($cell);
                })
            })
            $tbody.append($row);
            //Kolom Keempat
            $row = $('<tr>');
            $cell = $('<td>')
                .text("B")
                .addClass('str-body-side')
                .attr('colspan', 2);
            $row.append($cell);
            self.filtered_result.map(function (rec) {
                [rec.diff_ifi, rec.diff_ifr, rec.diff_ifa, rec.diff_afc].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .attr('colspan', 1);
                    $row.append($cell);
                })
            })
            $tbody.append($row);

        },
        do_show: function () {
            var self = this;
            this.data_loaded.done(function () {
                self.display_table();

            });
            return this._super();
        },


    });

    core.view_registry.add('statReal', statReal);
    return statReal;
});
