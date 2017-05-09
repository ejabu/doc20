from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_rece(models.Model):

    _name= "doc.rece"

    name = fields.Char(string='Incoming Transmittal Number', required=True)

    recv_rece_date = fields.Date(string='Receiving Date', required=True)


    # line_ids = fields.One2many('master.deliver', 'rece_id', 'MDR Line')
    line_ids = fields.Many2many('master.deliver', 'master_to_rece', 'rece_id', 'line_ids', string="Related MDR", copy=False)
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'recv_rece_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.onchange('line_ids','name')
    def oc_name(self):
        for rec in self.line_ids:
            rec.write({'recv_trans_number': self.name})

    @api.onchange('recv_rece_date', 'line_ids')
    def oc_recv_rece_date(self):
        for rec in self.line_ids:
            rec.write({'recv_rece_date': self.recv_rece_date})
