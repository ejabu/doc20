from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class doc_idc(models.Model):

    _name= "doc.idc"

    name = fields.Char(string='IDC Number', required=True)

    send_date = fields.Date(string='Sending Date', required=True)
    rece_date = fields.Date(string='Receiving Date',)

    line_ids = fields.One2many('master.deliver', 'idc_id', 'MDR Line', ondelete='restrict')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'send_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    # @api.onchange('name')
    # def update_name(self):
    #     import ipdb; ipdb.set_trace()
    #     # print "welcome"


    @api.multi
    def send_doc(self):
        # import ipdb; ipdb.set_trace()
        for line_id in self.line_ids:

            line_id.idc_number = ""
            line_id.send_date = ""
            line_id.rece_date = ""

            line_id.doc_status = line_id.doc_status_update
            line_id.rev_num = line_id.rev_num_update
            line_id.state = 'done'
            new_doc = line_id.copy()

            line_id.idc_number = self.name
            line_id.send_date = self.send_date
            line_id.rece_date = self.rece_date
        self.state='done'
