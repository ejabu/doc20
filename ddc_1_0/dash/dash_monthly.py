import json

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta

from openerp.exceptions import Warning

class dash_monthly(models.Model):

    _name= "dash.monthly"

    name = fields.Char(string='Report Name', required=True)
    description = fields.Char(string='Description', required=True)
    discipline = fields.Many2one('conf.discipline', 'Discipline')
    external_status = fields.Many2one('conf.external.status', 'External Status')
    dash_json = fields.Text(compute='_kanban_json')
    month_start =  fields.Selection('_get_months', 'Month Start', required=True)
    year_start =  fields.Selection([(str(num), str(num)) for num in range((datetime.now().year)-5, (datetime.now().year)+5 )], 'Year Start', required=True)
    month_end =  fields.Selection('_get_months', 'Month End', required=True)
    year_end =  fields.Selection([(str(num), str(num)) for num in range((datetime.now().year)-5, (datetime.now().year)+5)], 'Year End', required=True)
    date_field_start = fields.Selection(selection=[
                                            ('mdr.create_date', 'Date Creation'),
                                            ('mdr.sched_date', 'Schedule Date'),
                                            ('mdr.recv_rece_date', 'Receiving Date'),
                                            ('mdr.due_date', 'Due Date'),
                                            ('mdr.send_date', 'IDC Sending Date'),
                                            ('mdr.rece_date', 'IDC Receiving Date'),
                                            ('now()', 'Now'),
                                            ])

    def _get_months(self):
        months = [
            ('01', 'Jan'),
            ('02', 'Feb'),
            ('03', 'Mar'),
            ('04', 'Apr'),
            ('05', 'May'),
            ('06', 'Jun'),
            ('07', 'Jul'),
            ('08', 'Aug'),
            ('09', 'Sep'),
            ('10', 'Oct'),
            ('11', 'Nov'),
            ('12', 'Dec'),
        ]
        return months
    def _generate_where(self):
        where_clause = ""
        if self.external_status.name:
            where_clause =  "WHERE ext.name = '%s'" % (self.external_status.name)
        return where_clause

    @api.one
    def _kanban_json(self):
        par_date_field_start = self.date_field_start if self.date_field_start else "mdr.create_date"
        par_range_start = self.year_start + " "+ self.month_start
        par_range_end = self.year_end + " "+ self.month_end
        query= '''
                    SELECT date_trunc('month', %s)::date AS label, count(mdr.*) as value
                         FROM master_deliver mdr
                         WHERE %s is not null
                     GROUP BY label
                    ORDER BY label

        ''' % (par_date_field_start, par_date_field_start)
        self.env.cr.execute(query)
        query_fetch = self.env.cr.dictfetchall()
        for elem in query_fetch:
            elem.pop('sortIndex', None)
            elem['type'] = "past"
        query_res = [
            {'values': query_fetch,
            'range_start': par_range_start,
            'range_end': par_range_end,
            },

        ]
        self.dash_json = json.dumps(query_res)
