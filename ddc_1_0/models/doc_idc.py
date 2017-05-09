from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_idc(models.Model):

    _name= "doc.idc"

    name = fields.Char(string='IDC Number', required=True)

    send_date = fields.Date(string='Sending Date', required=True)
    sched_date = fields.Date(string='Schedule Date', required=True)
    due_date = fields.Date(string='Due Date',)

    line_count = fields.Integer(string='Line Count',compute='_line_count', store=True)

    line_ids = fields.One2many('master.deliver', 'idc_id', 'MDR Line')
    # line_ids = fields.Many2many('master.deliver', 'master_to_idc', 'idc_id', 'line_ids', string="Related MDR", copy=False)

    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'send_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.multi
    @api.depends('line_ids')
    def _line_count(self):
        # import ipdb; ipdb.set_trace()
        for rec in self:
            rec.line_count = len(rec.line_ids)



    @api.onchange('line_ids','name')
    def oc_name(self):
        self.line_ids.write({'idc_number': self.name})

    @api.onchange('line_ids','sched_date')
    def oc_sched_date(self):
        self.line_ids.write({'sched_date': self.sched_date})

    @api.onchange('line_ids','due_date')
    def oc_sched_date(self):
        self.line_ids.write({'due_date': self.due_date})
