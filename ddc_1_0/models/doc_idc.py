from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_idc(models.Model):

    _name= "doc.idc"

    name = fields.Char(string='IDC Number', required=True)

    send_date = fields.Date(string='Sending Date', required=True)
    sched_date = fields.Date(string='Schedule Date',)

    # line_ids = fields.One2many('master.deliver', 'idc_id', 'MDR Line')
    line_ids = fields.Many2many('master.deliver', 'master_to_idc', 'idc_id', 'line_ids', string="Related MDR", copy=False)

    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'send_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.multi
    def send_doc(self):
        self.state='done'

    @api.onchange('sched_date')
    def oc_sched_date(self):
        for rec in self.line_ids:
            rec.write({'sched_date': self.sched_date})

    @api.onchange('send_date')
    def oc_send_date(self):
        for rec in self.line_ids:
            rec.write({'send_date': self.send_date})
