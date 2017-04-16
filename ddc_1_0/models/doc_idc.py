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
        # 'date_end': lambda *a:(datetime.now() + timedelta(days=(6))).strftime('%Y-%m-%d'),
    }

    # @api.onchange('to_company')
    # def company_details(self):
    #     if self.to_company.id:
    #         if self.to_company.parent_id.id:
    #             if self.to_company.parent_id.street:
    #                 self.address = self.to_company.parent_id.street
    #                 if self.to_company.parent_id.street2:
    #                     self.address = self.address +" " + self.to_company.parent_id.street2
    #             self.city = self.to_company.parent_id.city or ""
    #             self.province = self.to_company.parent_id.state_id.name or ""
    #             self.country = self.to_company.parent_id.country_id.name or ""
    #         else :
    #             if self.to_company.street:
    #                 self.address = self.to_company.street
    #                 if self.to_company.street2:
    #                     self.address = self.address +" " + self.to_company.street2
    #             self.city = self.to_company.city or ""
    #             self.province = self.to_company.state_id.name or ""
    #             self.country = self.to_company.country_id.name or ""
    #
    # @api.multi
    # def send_doc(self):
    #     for master_deliver_id in self.master_deliver_id:
    #         master_deliver_id.doc_status = master_deliver_id.doc_status_update
    #         master_deliver_id.state = 'done'
    #         new_doc = master_deliver_id.copy()
    #         new_doc.history_seq = master_deliver_id.history_seq
    #         new_doc.rev_num = master_deliver_id.rev_num + 1
    #         new_doc.rev_num_update = master_deliver_id.rev_num_update + 1
    #     self.state='sent'
