import json

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

from openerp.exceptions import Warning

class dash_delay_approve(models.Model):

    _name= "dash.delay.approve"

    name = fields.Char(string='Report Name', required=True)
    description = fields.Char(string='Description', required=True)
    discipline = fields.Many2one('conf.discipline', 'Discipline')
    external_status = fields.Many2one('conf.external.status', 'External Status')
    dash_json = fields.Text(compute='_kanban_json')
    date_field_start = fields.Selection(selection=[
                                            ('mdr.create_date', 'Date Creation'),
                                            ('mdr.recv_rece_date', 'Receiving Date'),
                                            ('mdr.due_date', 'Due Date'),
                                            ('mdr.send_date', 'IDC Sending Date'),
                                            ('mdr.rece_date', 'IDC Receiving Date'),
                                            ('now()', 'Now'),
                                            ])
    date_field_end = fields.Selection(selection=[
                                            ('mdr.create_date', 'Date Creation'),
                                            ('mdr.recv_rece_date', 'Receiving Date'),
                                            ('mdr.due_date', 'Due Date'),
                                            ('mdr.send_date', 'IDC Sending Date'),
                                            ('mdr.rece_date', 'IDC Receiving Date'),
                                            ('now()', 'Now'),
                                            ])

    def _generate_where(self):
        where_clause = ""
        if self.external_status.name:
            where_clause =  "WHERE ext.name = '%s'" % (self.external_status.name)
        return where_clause

    @api.one
    def _kanban_json(self):
        par_date_field_start = self.date_field_start if self.date_field_start else "mdr.create_date"
        par_date_field_end = self.date_field_end if self.date_field_end else "now()"
        query= '''
                    WITH ranges AS (
    select 1 minRange, 7 maxRange, 6 sortIndex, '1 W' "range"
         union all
         select 8, 14, 5, '2 W'
         union all
         select 15, 21, 4, '3 W'
         union all
         select 22, 28, 3, '4 W'
         union all
         select 29, 35, 2, '5 W'
         union all
         select 36, 1000, 1, '> 5 W'
     ),
mdr AS (

SELECT cast((EXTRACT(epoch FROM age(%s, %s ))/86400) as smallint) as haha
    FROM master_deliver mdr LEFT JOIN conf_external_status ext ON (mdr.external_status = ext.id)
    %s

)
SELECT r.range as label, r.sortIndex as "sortIndex", count(mdr.*) as value
  FROM ranges r
  LEFT JOIN mdr ON mdr.haha BETWEEN r.minRange AND r.maxRange

GROUP BY r.range, r.sortIndex
ORDER BY r.sortIndex

        ''' % (par_date_field_end,par_date_field_start, self._generate_where())
        self.env.cr.execute(query)
        query_fetch = self.env.cr.dictfetchall()
        for elem in query_fetch:
            elem.pop('sortIndex', None)
            elem['type'] = "past"
        query_res = [{'values': query_fetch}]
        self.dash_json = json.dumps(query_res)
