from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_rece(models.Model):

    _name= "doc.rece"

    name = fields.Char(string='Transmittal Number', required=True)

    recv_rece_date = fields.Date(string='Receiving Date', required=True)


    line_ids = fields.One2many('master.deliver', 'rece_id', 'MDR Line')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'recv_rece_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.multi
    def send_doc(self):
        self.state='done'
