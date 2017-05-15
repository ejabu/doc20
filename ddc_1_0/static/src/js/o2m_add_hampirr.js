openerp.ddc_1_0 = function(instance) {
    var _t = instance.web._t,
       _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    instance.web.ListView.List.include({

        render: function () {
            var self = this;
            this.$current.html(
                QWeb.render('ListView.rows', _.extend({}, this, {
                        render_cell: function () {
                            return self.render_cell.apply(self, arguments); }
                    })));
            this.new_pad_table_to(4);
        },
        new_pad_table_to: function(count) {
                console.log('Pad2', count);
                // your custom functionality;

                if (this.records.length >= count ||
                        _(this.columns).any(function(column) { return column.meta; })) {
                    return;
                }
                var cells = [];
                if (this.options.selectable) {
                    cells.push('<th class="oe_list_record_selector"></td>');
                }
                _(this.columns).each(function(column) {
                    if (column.invisible === '1') {
                        return;
                    }
                    cells.push('<td title="' + column.string + '">&nbsp;</td>');
                });
                if (this.options.deletable) {
                    cells.push('<td class="oe_list_record_delete"></td>');
                }
                cells.unshift('<tr>');
                cells.push('</tr>');

                var row = cells.join('');
                this.$current
                    .children('tr:not([data-id])').remove().end()
                    .append(new Array(count - this.records.length + 1).join(row));

                var columns = _(this.columns).filter(function (column) {
                    return column.invisible !== '1';
                }).length;
                if (this.options.selectable) { columns++; }
                if (this.options.deletable) { columns++; }

                var $cell = $('<td>', {
                    colspan: columns,
                    'class': 'oe_form_field_x2many_list_row_add'
                }).append(
                    $('<a>', {href: '#'}).text(_t("Add an item"))
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

                var $padding = this.$current.find('tr:not([data-id]):first');
                var $newrow = $('<tr>').append($cell);
                if ($padding.length) {
                    $padding.before($newrow);
                } else {
                    this.$current.append($newrow);
                }






            },

        })


}
