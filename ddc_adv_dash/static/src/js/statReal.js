odoo.define('ddc_adv_dash.statReal', function(require) {
    "use strict";

    var core = require('web.core');
    var form_common = require('web.form_common');
    var Model = require('web.DataModel');
    var time = require('web.time');
    var View = require('web.View');
    var session = require('web.session');
    var Sidebar = require('web.Sidebar');


    var crash_manager = require('web.crash_manager');
    var framework = require('web.framework');


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

            this.draw_side_table($mainbox);
            this.draw_table($mainbox);
            this.$table_container.empty().append($fragment);
        },

        draw_side_table: function($mainbox){
            var $row, $cell, $table, $thead, $tbody;
            var self = this
            $table = $('<table>')
                .addClass('table table-hover table-condensed')
                .addClass('str-table')
                .appendTo($mainbox);
            $thead = $('<thead>').appendTo($table);
            $tbody = $('<tbody>').appendTo($table);
            //Baris Pertama
            $row = $('<tr>');
            $cell = $('<th>')
                .text("blank")
                .addClass('trans-cell')
                .attr('colspan', 2)
            $row.append($cell);
            $thead.append($row);
            //Baris Kedua
            $row = $('<tr>');
            $cell = $('<td>')
                .text("blank")
                .addClass('trans-cell')
                .attr('colspan', 2);
            $row.append($cell);

            $tbody.append($row);
            //Baris Ke3
            $row = $('<tr>');
            $cell = $('<td nowrap>')
                .text("Jumlah Dokumen")
                .addClass('table-side-cell bold')
                .attr('colspan', 2);
            $row.append($cell);

            $tbody.append($row);
            //Baris Ke4
            $row = $('<tr>');
            $cell = $('<td nowrap>')
                .text("A")
                .addClass('table-side-cell bold')
                .attr('colspan', 2);
            $row.append($cell);

            $tbody.append($row);
            //Baris Ke5
            $row = $('<tr>');
            $cell = $('<td nowrap>')
                .text("B")
                .addClass('table-side-cell bold')
                .attr('colspan', 2);
            $row.append($cell);

            $tbody.append($row);
        },
        draw_table: function($mainbox){
            var $row, $cell, $table, $thead, $tbody;
            var self = this



            self.filtered_result.map(function (rec) {
                $table = $('<table>')
                    .addClass('table table-hover table-condensed')
                    .addClass('str-table')
                    .appendTo($mainbox);
                $thead = $('<thead>').appendTo($table);
                $tbody = $('<tbody>').appendTo($table);
                //Baris Pertama
                $row = $('<tr>');
                $cell = $('<th>')
                    .text(rec.week_name)
                    .attr('colspan', 4)
                    .addClass('str-header');
                $row.append($cell);

                $thead.append($row);
                //Baris Kedua
                $row = $('<tr>');
                ["IFI", "IFR", "IFA", "AFC"].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .addClass('str-sub-header str-body-cell bold')
                        .attr('colspan', 1);
                    $row.append($cell);
                })

                $tbody.append($row);
                //Baris Ketiga
                $row = $('<tr>');
                [rec.ifi, rec.ifr, rec.ifa, rec.afc].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .addClass('str-body-cell')
                        .attr('colspan', 1);
                    if (value < 1 ) {
                        $cell.addClass('str-body-cell-neg');
                    }
                    $row.append($cell);
                })

                $tbody.append($row);
                //Baris Keempat
                $row = $('<tr>');

                ["", rec.def_ifr, rec.def_ifa, rec.def_afc].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .addClass('str-body-cell')
                        .attr('colspan', 1);
                    if (value < 0  && value !== "") {
                        $cell.addClass('str-body-cell-neg');
                    }

                    $row.append($cell);
                })

                $tbody.append($row);
                //Baris Kelima
                $row = $('<tr>');
                [rec.diff_ifi, rec.diff_ifr, rec.diff_ifa, rec.diff_afc].map(function (value) {
                    $cell = $('<td>')
                        .text(value)
                        .addClass('str-body-cell')
                        .attr('colspan', 1);
                    if (value < 1) {
                        $cell.addClass('str-body-cell-neg');
                    }
                    $row.append($cell);
                })

                $tbody.append($row);

            })
        },


        do_show: function () {
            var self = this;
            this.data_loaded.done(function () {
                self.display_table();

            });
            return this._super();
        },

        willStart: function () {
            var self = this;
            return session.rpc('/web/pivot/check_xlwt').then(function(result) {
                self.xlwt_installed = result;
            });
        },
        render_sidebar: function($node) {
            console.log("render_sidebar");
            console.log($node, this);
            if (this.xlwt_installed && $node && this.options.sidebar) {
                this.sidebar = new Sidebar(this, {editable: this.is_action_enabled('edit')});
                this.sidebar.add_items('other', [{
                    label: _t("Download xls"),
                    callback: this.download_table.bind(this),
                }]);

                this.sidebar.appendTo($node);
            }
        },
        download_table: function () {
            framework.blockUI();

            console.log('download_table');
            console.log('download_table');
            console.log(JSON.stringify(this.filtered_result));

            session.get_file({
                url: '/web/adv/stat_real',
                data: {data: JSON.stringify(this.filtered_result)},
                complete: framework.unblockUI,
                error: crash_manager.rpc_error.bind(crash_manager)
            });
        }


    });

    core.view_registry.add('statReal', statReal);
    return statReal;
});
