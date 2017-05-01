import json

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

from openerp.exceptions import Warning

class dash_delay_approve(models.Model):

    _name= "dash.delay.approve"

    name = fields.Char(string='Report Name', required=True)
    discipline = fields.Many2one('conf.discipline', 'Discipline')
    external_status = fields.Many2one('conf.external.status', 'External Status')
    query_result= fields.Text(string='Query Result',)
    dash_json = fields.Text(compute='_kanban_json')

    @api.one
    def _kanban_json(self):
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
         select 36, 42, 1, '> 5 W'
     ),
mdr AS (

SELECT cast((EXTRACT(epoch FROM age(mdr.recv_rece_date, mdr.%s ))/86400) as smallint) as haha
    FROM master_deliver mdr INNER JOIN conf_external_status ext ON (mdr.external_status = ext.id) WHERE ext.name = 'IFA'

)
SELECT r.range as label, r.sortIndex as "sortIndex", count(mdr.*) as value
  FROM ranges r
  LEFT JOIN mdr ON mdr.haha BETWEEN r.minRange AND r.maxRange

GROUP BY r.range, r.sortIndex
ORDER BY r.sortIndex

        ''' % ("create_date")
        import ipdb; ipdb.set_trace()
        self.env.cr.execute(query)
        query_fetch = self.env.cr.dictfetchall()
        for elem in query_fetch:
            elem.pop('sortIndex', None)
            elem['type'] = "past"
        query_res = [{'values': query_fetch}]
        self.dash_json = json.dumps(query_res)
