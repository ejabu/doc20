from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_idc(models.Model):

    _name= "doc.idc"

    name = fields.Char(string='IDC Number', required=True)

    send_date = fields.Date(string='Sending Date', required=True)
    sched_date = fields.Date(string='Schedule Date',)

    line_ids = fields.One2many('master.deliver', 'idc_id', 'MDR Line')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'send_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.multi
    def send_doc(self):
        self.state='done'
