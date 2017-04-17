from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_send(models.Model):

    _name= "doc.send"

    name = fields.Char(string='Transmittal Number', required=True)

    trans_date = fields.Date(string='Transmittal Date', required=True)
    due_date = fields.Date(string='Due Date',)
    need_to_response = fields.Date(string='Need to Response',)
    antam_date = fields.Date(string='Antam Receive Date',)

    line_ids = fields.One2many('master.deliver', 'send_id', 'MDR Line')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'trans_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.multi
    def send_doc(self):
        self.state='done'
