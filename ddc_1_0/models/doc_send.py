from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_send(models.Model):

    _name= "doc.send"

    name = fields.Char(string='Transmittal Number', required=True)
    recepient = fields.Many2one('res.partner', string='Recepient', required=True, copy=False)
    recepient_rece_date = fields.Date(string='Recepient Receive Date')

    trans_date = fields.Date(string='Transmittal Date', required=True)
    trans_due_date = fields.Date(string='Due Date',)

    # line_ids = fields.One2many('master.deliver', 'send_id', 'MDR Line')
    line_ids = fields.Many2many('master.deliver', 'master_to_send', 'send_id', 'line_ids', string="Related MDR", copy=False)
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'trans_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.onchange('line_ids','name')
    def oc_name(self):
        for rec in self.line_ids:
            rec.write({'trans_number': self.name})

    @api.onchange('line_ids','trans_date')
    def oc_trans_date(self):
        for rec in self.line_ids:
            rec.write({'trans_date': self.trans_date})

    @api.onchange('line_ids','trans_due_date')
    def oc_trans_due_date(self):
        for rec in self.line_ids:
            rec.write({'trans_trans_due_date': self.trans_due_date})


    @api.onchange('line_ids','recepient_rece_date')
    def oc_recepient_rece_date(self):
        for rec in self.line_ids:
            rec.write({'recepient_rece_date': self.recepient_rece_date})
