import json

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

from openerp.exceptions import Warning

class dash_delay_approve(models.Model):

    _name= "dash.delay.approve"

    name = fields.Char(string='Report Name', required=True)
    query_result= fields.Text(string='Query Result',)
    dash_json = fields.Text(compute='_kanban_json')

    @api.one
    def _kanban_json(self):
        query= '''
                    WITH ranges AS (
                        select 1 minRange, 7 maxRange, 3 sortIndex, '1 W' "range"
                             union all
                             select 8, 14, 2, '2 W'
                             union all
                             select 15, 21, 1, '3 W'
                             union all
                             select 22, 28, 1, '4 W'
                             union all
                             select 29, 35, 1, '5 W'
                             union all
                             select 36, 42, 1, '> 5 W'
                         ),
                    mdr AS (
                        SELECT cast((EXTRACT(epoch FROM age(now(), create_date))/86400) as integer) as haha FROM master_deliver

                    )
                    SELECT r.range as label, r.sortIndex as "sortIndex", count(mdr.*) as value
                      FROM ranges r
                      LEFT JOIN mdr ON mdr.haha BETWEEN r.minRange AND r.maxRange

                    GROUP BY r.range, r.sortIndex
                    ORDER BY r.sortIndex

        '''
        self.env.cr.execute(query)
        query_fetch = self.env.cr.dictfetchall()
        # import ipdb; ipdb.set_trace()


        query_res = [{'values': query_fetch}]
        # self.dash_json = json.dumps(query_res)

        asal = '''
            [{
    "values": [{
        "type" : "past",
        "value": 15749.99,
        "label": "Past"
    }, {
        "type" : "past",
        "value": 0.0,
        "label": "23-29 Apr"
    }, {
        "type" : "past",
        "value": 0.0,
        "label": "This Week"
    }, {
        "type" : "past",
        "value": 0.0,
        "label": "7-13 May"
    }, {
        "type" : "past",
        "value": 0.0,
        "label": "14-20 May"
    }, {
        "type" : "past",
        "value": 0.0,
        "label": "Future"
    }]
}]

        '''


        asal = '''
        [{
        "type": "past",
        "value": 15749.99,
        "label": "Past"
    }, {
        "type": "past",
        "value": 0.0,
        "label": "23-29 Apssssssssssr"
    }, {
        "type": "past",
        "value": 0.0,
        "label": "This Week"
    }, {
        "type": "past",
        "value": 0.0,
        "label": "7-13 May"
    }, {
        "type": "past",
        "value": 0.0,
        "label": "14-20 May"
    }, {
        "type": "past",
        "value": 0.0,
        "label": "Future"
    }]
'''

        hasil = json.loads(asal)
        mai = [{'values': hasil}]
        self.dash_json = json.dumps(mai)
        # if (self.type in ['sale', 'purchase']):
        #     self.kanban_dashboard_graph = json.dumps(self.get_bar_graph_datas())
        # elif (self.type in ['cash', 'bank']):
        #     self.kanban_dashboard_graph = json.dumps(self.get_line_graph_datas())
