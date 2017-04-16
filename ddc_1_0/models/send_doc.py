from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_idc(models.Model):

    _name= "doc.idc"

    name = fields.Char(string='IDC Number', required=True)

    send_date = fields.Date(string='Sending Date', required=True)
    rece_date = fields.Date(string='Receiving Date',)

    line_ids = fields.One2many('master.deliver', 'idc_id', 'MDR Line')

    _defaults={
        'state': 'new',
        'send_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }
