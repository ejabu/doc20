from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class master_deliver(models.Model):

    _name= "master.deliver"

    discipline = fields.Many2one('conf.discipline', 'Discipline', required=True)
    doc_categ = fields.Many2one('conf.doc.categ', 'Category')
    doc_sub = fields.Many2one('conf.doc.sub', 'Subsystem')
    name = fields.Char(string='Document Number', required=True)
    doc_title = fields.Char(string='Title')
    doc_type = fields.Many2one('conf.doc.type', 'Document Type', required=True)
    doc_type_des = fields.Char(string='Type Description')

    sched_date = fields.Date(string='Schedule Date')
    originator = fields.Many2one('res.partner', string='Originator')
    internal_status = fields.Many2one('conf.internal.status', 'Internal Status')

    doc_pred = fields.Char(string='Document Predecessor')
    alt_doc = fields.Char(string='Alternative Document #')


    notes = fields.Text(string='Notes')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    idc_id = fields.Many2one('doc.idc', 'Related IDC')
    rev_num = fields.Many2one('conf.rev.num', 'Revision Number')

    idc_number = fields.Char(string='IDC Number', related='idc_id.name', store=True)
    send_date = fields.Date(string='Sending Date', related='idc_id.send_date', store=True)
    rece_date = fields.Date(string='Receiving Date', related='idc_id.rece_date', store=True)

    # file_name = fields.Char(string='File Name')
    # doc_status = fields.Many2one('conf.doc.status', 'Status')
    # doc_status_update = fields.Many2one('conf.doc.status', 'Status')
    # rev_num = fields.Integer('Revision Number')
    # rev_num_update = fields.Integer('Revision Number')
    # external_status = fields.Many2one('conf.external.status', 'External Status')
    # old_rev = fields.Char(string='Old Revision')


    # history_seq = fields.Char(string='History')
    # history_seq = fields.Char(string='History', required=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('master.deliver'))

    # send_eng_id = fields.Many2many('send.eng.doc', 'master_to_send_eng', 'master_deliver_id', 'send_eng_id', string="Master Deliver", copy=False)
    # rec_eng_id = fields.Many2many('rec.eng.doc', 'master_to_rec_eng', 'master_deliver_id', 'rec_eng_id', string="Master Deliver", copy=False)

    _defaults={
        'state': 'new',
    }
