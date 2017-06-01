from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_rece(models.Model):

    _name= "doc.rece"
    _inherit = ['mail.thread']

    recipient = fields.Many2one('res.partner', string='Recipient', required=True, copy=False)
    name = fields.Char(string='Incoming Transmittal Number', required=True)

    recv_rece_date = fields.Date(string='Transmittal Date', required=True)


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


    @api.multi
    def rewrite_relation(self):

        all_counter = 0
        counter = 0
        message = "Check berapa banyak MDR yang terhubung, namun sebenarnya belum pernah Update Revisi / Update Status \n \n"
        for doc in self.search([]):
            doc_send_name = doc.name
            for line in doc.line_ids:
                all_counter += 1
                if len(line.history_ids) <> 1 :
                    counter += 1
                    server_log = "%s : Outgoing Trans : %s - MDR Name : %s \n" % (counter, doc_send_name, line.name)
                    message += server_log

        message += '\n Total Doc yang ada Relasi : %s \n' % all_counter
        message += 'Total Doc yang ada Bermasalah : %s \n' % counter

        raise UserError(message)
