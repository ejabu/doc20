odoo.define('oepetstore.EjaView', function (require) {
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

    var EjaView = View.extend({
        template: "EjaView",
        display_name: _lt('EjaView'),
        icon: 'fa-clock-o',

        init: function (parent, dataset, view_id, options) {
            this._super(parent);
            this.view_id = view_id;
            this.view_type = 'ejaview';
            this.model = dataset.model;
            this.dataset = dataset;
                        this.model = dataset.model;
                        this.fields_view = {};
                        this.view_id = view_id;
            console.log('EJA3');
            console.log(this);
        },


    });

    core.view_registry.add('ejaview', EjaView);
    return EjaView;
});
