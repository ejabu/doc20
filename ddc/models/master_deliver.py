from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class master_deliver(models.Model):

    _name= "master.deliver"

    # cost_header_number = fields.Integer(string='Cost Header Number', required=True)
    discipline = fields.Char(string='Discipline', required=True)
    doc_categ = fields.Char(string='Document Category')
    doc_sub = fields.Char(string='Document Subsystem')
    name = fields.Char(string='Document Number', required=True)
    doc_title = fields.Char(string='Document Title')
    originator = fields.Char(string='Originator', required=True)
    doc_pred = fields.Char(string='Document Predecessor')
    file_name = fields.Char(string='File Name')
    alt_doc = fields.Char(string='Alternative Document #')
    sched_date = fields.Date(string='Schedule Date')
    doc_type = fields.Char(string='Document Type', required=True)
    rev_num = fields.Char(string='Revision Number')
    internal_status = fields.Char(string='Internal Status', required=True)
    external_status = fields.Char(string='External Status')
    old_rev = fields.Char(string='Old Revision')
    notes = fields.Text(string='Notes')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])


    send_eng_id = fields.Many2many('send.eng.doc', 'master_to_send_eng', 'master_deliver_id', 'send_eng_id', string="Master Deliver")
    rec_eng_id = fields.Many2many('rec.eng.doc', 'master_to_rec_eng', 'master_deliver_id', 'rec_eng_id', string="Master Deliver")
