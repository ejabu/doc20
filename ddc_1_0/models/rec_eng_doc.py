from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class rec_eng_doc(models.Model):

    _name= "rec.eng.doc"

    name = fields.Char(string='Transmittal Number', required=True)

    from_company = fields.Many2one('res.partner', 'From Company', required=True)
    # from_company = fields.Char(string='From Company' , required=True)
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    province = fields.Char(string='State')
    country = fields.Char(string='Country')


    ref_num = fields.Char(string='Reference Number')

    receiving_date = fields.Date(string='Receiving Date', required=True)
    # status_comment = fields.Char(string='Status Comment')
    status_comment = fields.Many2one('conf.rec.comment', 'Status Comment')

    sender = fields.Char(string='Sender')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    # master_deliver_id = fields.Many2one('master.deliver', 'Related Master Deliverables')
    master_deliver_id = fields.Many2many('master.deliver', 'master_to_send_eng', 'rec_eng_id', 'master_deliver_id', string="Master Deliver")

    _defaults={
        'state': 'new',
        'receiving_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
        # 'date_end': lambda *a:(datetime.now() + timedelta(days=(6))).strftime('%Y-%m-%d'),
    }

    @api.onchange('from_company')
    def company_details(self):
        if self.from_company.id:
            if self.from_company.parent_id.id:
                if self.from_company.parent_id.street:
                    self.address = self.from_company.parent_id.street
                    if self.from_company.parent_id.street2:
                        self.address = self.address +" " + self.from_company.parent_id.street2
                self.city = self.from_company.parent_id.city or ""
                self.province = self.from_company.parent_id.state_id.name or ""
                self.country = self.from_company.parent_id.country_id.name or ""
            else :
                if self.from_company.street:
                    self.address = self.from_company.street
                    if self.from_company.street2:
                        self.address = self.address +" " + self.from_company.street2
                self.city = self.from_company.city or ""
                self.province = self.from_company.state_id.name or ""
                self.country = self.from_company.country_id.name or ""
