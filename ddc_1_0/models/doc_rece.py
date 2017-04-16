from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_rece(models.Model):

    _name= "doc.rece"

    name = fields.Char(string='Transmittal Number', required=True)

    recv_rece_date = fields.Date(string='Receiving Date', required=True)


    line_ids = fields.One2many('master.deliver', 'rece_id', 'MDR Line', ondelete='restrict')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'recv_rece_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.multi
    def send_doc(self):
        for line_id in self.line_ids:

            line_id.doc_status = line_id.doc_status_update
            line_id.rev_num = line_id.rev_num_update
            line_id.recv_comment = line_id.recv_comment_update
            line_id.state = 'done'
            new_doc = line_id.copy()

            line_id.recv_trans_number = self.name
            line_id.recv_rece_date = self.recv_rece_date
        self.state='done'
