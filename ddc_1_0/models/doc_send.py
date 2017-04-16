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

    line_ids = fields.One2many('master.deliver', 'send_id', 'MDR Line', ondelete='restrict')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'trans_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.multi
    def send_doc(self):
        for line_id in self.line_ids:

            line_id.doc_status = line_id.doc_status_update
            line_id.rev_num = line_id.rev_num_update
            line_id.state = 'done'
            new_doc = line_id.copy()

            line_id.trans_number = self.name
            line_id.trans_date = self.trans_date
            line_id.due_date = self.due_date
            line_id.need_to_response = self.need_to_response
            line_id.antam_date = self.antam_date
        self.state='done'
