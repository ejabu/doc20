from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class master_deliver(models.Model):

    _name= "master.deliver"
    _order = "create_date"

    discipline = fields.Many2one('conf.discipline', 'Discipline', required=True, ondelete='restrict', copy=True)
    doc_categ = fields.Many2one('conf.doc.categ', 'Category', ondelete='restrict', copy=True)
    doc_sub = fields.Many2one('conf.doc.sub', 'Subsystem', ondelete='restrict', copy=True)
    name = fields.Char(string='Document Number', required=True, copy=True)
    doc_title = fields.Char(string='Title', copy=True)
    doc_type = fields.Many2one('conf.doc.type', 'Document Type', required=True, ondelete='restrict', copy=True)
    doc_type_desc = fields.Char(string='Type Description', copy=True)

    sched_date = fields.Date(string='Schedule Date', copy=True)
    originator = fields.Many2one('res.partner', string='Originator', copy=True)

    doc_status = fields.Many2one('conf.doc.status', 'Status', ondelete='restrict', copy=True)
    doc_status_update = fields.Many2one('conf.doc.status', 'Status', ondelete='restrict', copy=True)

    # internal_status = fields.Many2one('conf.internal.status', 'Internal Status')

    doc_pred = fields.Char(string='Document Predecessor', copy=True)
    alt_doc = fields.Char(string='Alternative Document #', copy=True)


    notes = fields.Text(string='Notes', copy=True)
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    idc_id = fields.Many2one('doc.idc', 'Related IDC', ondelete='restrict', copy=False)
    rev_num = fields.Many2one('conf.rev.num', 'Revision Number', ondelete='restrict', copy=True)
    rev_num_update = fields.Many2one('conf.rev.num', 'Revision Number', ondelete='restrict', copy=True)

    idc_number = fields.Char(string='IDC Number', copy=False)
    send_date = fields.Date(string='IDC Sending Date', copy=False)
    rece_date = fields.Date(string='IDC Receiving Date', copy=False)

    send_id = fields.Many2one('doc.send', 'Related Send', ondelete='restrict', copy=False)
    trans_number = fields.Char(string='Trans Number', copy=False)
    trans_date = fields.Date(string='Transmittal Date', required=True, copy=False)
    due_date = fields.Date(string='Due Date', copy=False)
    need_to_response = fields.Date(string='Need to Response', copy=False)
    antam_date = fields.Date(string='Antam Receive Date', copy=False)

    rece_id = fields.Many2one('doc.rece', 'Related Receiving', ondelete='restrict', copy=False)
    recv_trans_number = fields.Char(string='Transmittal Number', copy=False)
    recv_rece_date = fields.Date(string='Receiving Date', required=True, copy=False)
    recv_comment = fields.Many2one('conf.rec.comment', 'Status Comment', ondelete='restrict', copy=False)
    recv_comment_update = fields.Many2one('conf.rec.comment', 'Status Comment', ondelete='restrict', copy=False)
    # file_name = fields.Char(string='File Name')

    # external_status = fields.Many2one('conf.external.status', 'External Status')
    # old_rev = fields.Char(string='Old Revision')


    # history_seq = fields.Char(string='History')
    # history_seq = fields.Char(string='History', required=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('master.deliver'))

    # send_eng_id = fields.Many2many('send.eng.doc', 'master_to_send_eng', 'master_deliver_id', 'send_eng_id', string="Master Deliver", copy=False)
    # rec_eng_id = fields.Many2many('rec.eng.doc', 'master_to_rec_eng', 'master_deliver_id', 'rec_eng_id', string="Master Deliver", copy=False)

    _defaults = {
        'state': 'new',
    }
    #
    _sql_constraints = [
        ('name', 'Check(1=1)', "The system record Can't be duplicate value for this field!")
        # ('name', 'unique(name)', "The system record Can't be duplicate value for this field!")
    ]
    @api.onchange('doc_type')
    def change_doc_type(self):
        self.doc_type_desc = self.doc_type.desc
