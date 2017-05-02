odoo.define('journal_dashboard', function (require) {
'use strict';

var kanban_widgets = require('web_kanban.widgets');

var JournalDashboardGraph = kanban_widgets.AbstractField.extend({
    start: function() {
        this.graph_type = this.$node.attr('graph_type');
        this.data = JSON.parse(this.field.raw_value);
        this.display_graph();
        return this._super();
    },

    display_graph : function() {
        var self = this;
        nv.addGraph(function () {
            self.$svg = self.$el.append('<svg>');

            switch(self.graph_type) {

                case "line":
                    self.$svg.addClass('o_graph_linechart');

                    self.chart = nv.models.lineChart();
                    self.chart.options({
                        x: function(d, u) { return u },
                        margin: {'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
                        showYAxis: false,
                        showLegend: false,
                    });
                    self.chart.xAxis
                        .tickFormat(function(d) {
                            var label = '';
                            _.each(self.data, function(v, k){
                                if (v.values[d] && v.values[d].x){
                                    label = v.values[d].x;
                                }
                            });
                            return label;
                        });
                    self.chart.yAxis
                        .tickFormat(d3.format(',.2f'));

                    break;

                case "bar":
                    self.$svg.addClass('o_graph_barchart');

                    self.chart = nv.models.discreteBarChart()
                        .x(function(d) { return d.label })
                        .y(function(d) { return d.value })
                        .showValues(false)
                        .showYAxis(false)
                        .margin({'left': 0, 'right': 0, 'top': 0, 'bottom': 40});


                        self.chart.xAxis
                                    .axisLabel('Month')
                                    // .tickFormat(function(d) {
                                    //
                                    //    return d3.time.format("%b-%y")(new Date(d)); })

                    // self.chart.xAxis.axisLabel(self.data[0].title);
                    self.chart.yAxis.tickFormat(d3.format(',.2f'));

                    var vis = d3.select("body").
            append("svg:svg")
                console.log('visadasd');
                console.log(vis);

                var mindate = new Date(2012,0,1),
                            maxdate = new Date(2012,0,31);

                            var xScale = d3.time.scale()
            	        .domain([mindate, maxdate])    // values between for month of january


                        // define the x axis
                        var xAxis = d3.svg.axis()
                            .orient("bottom")
                            .scale(xScale)
                            .tickFormat(function(d) {
                               return d3.time.format("%b-%y")(new Date(d)); })

                        self.chart.xAxis = xAxis
                        // draw x axis with labels and move to the bottom of the chart area
                        // vis.append("g")
                        //     .attr("class", "xaxis axis")  // two classes, one for css formatting, one for selection below
                        //     .call(xAxis);


                    break;
            }
            d3.select(self.$el.find('svg')[0])
                .datum(self.data)
                .transition().duration(1200)
                .call(self.chart);

            self.customize_chart();

            nv.utils.windowResize(self.on_resize);
        });
    },

    on_resize: function(){
        this.chart.update();
        this.customize_chart();
    },

    customize_chart: function(){
        if (this.graph_type === 'bar') {
            // Add classes related to time on each bar of the bar chart
            var bar_classes = _.map(this.data[0].values, function (v, k) {return v.type});

            _.each(this.$('.nv-bar'), function(v, k){
                // classList doesn't work with phantomJS & addClass doesn't work with a SVG element
                $(v).attr('class', $(v).attr('class') + ' ' + bar_classes[k]);
            });
        }
    },

    destroy: function(){
        nv.utils.offWindowResize(this.on_resize);
        this._super();
    },

});


kanban_widgets.registry.add('dashboard_graph', JournalDashboardGraph);

});
