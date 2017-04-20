from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

from openerp.exceptions import Warning

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
    rev_num = fields.Many2one('conf.rev.num', 'Revision Number', ondelete='restrict', copy=True)
    rev_num_update = fields.Many2one('conf.rev.num', 'Revision Number', ondelete='restrict', copy=True)

    # internal_status = fields.Many2one('conf.internal.status', 'Internal Status')
    #IFA IFI RE-IDC
    external_status = fields.Many2one('conf.external.status', 'External Status')

    doc_pred = fields.Char(string='Predecessor', copy=True)
    alt_doc = fields.Char(string='Alternative Document #', copy=True)


    notes = fields.Text(string='Notes', copy=True)
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])


    idc_id = fields.Many2one('doc.idc', 'Related IDC', ondelete='restrict', copy=False)
    idc_number = fields.Char(string='IDC Number', related='idc_id.name', store=True, copy=False)
    send_date = fields.Date(string='IDC Sending Date', related='idc_id.send_date', store=True, copy=False)
    rece_date = fields.Date(string='IDC Receiving Date', related='idc_id.rece_date', store=True, copy=False)

    send_id = fields.Many2one('doc.send', 'Related Send', ondelete='restrict', copy=False)
    trans_number = fields.Char(string='Sending Transmittal Number', related='send_id.name', store=True, copy=False)
    trans_date = fields.Date(string='Transmittal Date', related='send_id.trans_date', store=True, copy=False)
    due_date = fields.Date(string='Due Date', related='send_id.due_date', store=True, copy=False)
    need_to_response = fields.Date(string='Need to Response', related='send_id.need_to_response', store=True, copy=False)
    antam_date = fields.Date(string='Antam Receive Date', related='send_id.antam_date', store=True, copy=False)

    rece_id = fields.Many2one('doc.rece', 'Related Receiving', ondelete='restrict', copy=False)
    recv_trans_number = fields.Char(string='Receiving Transmittal Number', related='rece_id.name', store=True, copy=False)
    recv_rece_date = fields.Date(string='Receiving Date', related='rece_id.recv_rece_date', store=True, copy=False)
    recv_comment = fields.Many2one('conf.rec.comment', 'Status Comment', ondelete='restrict', copy=False)


    # idc_id = fields.Many2one('doc.idc', 'Related IDC', ondelete='restrict', copy=False)
    # idc_number = fields.Char(string='IDC Number',copy=False)
    # send_date = fields.Date(string='IDC Sending Date', copy=False)
    # rece_date = fields.Date(string='IDC Receiving Date', copy=False)
    #
    # send_id = fields.Many2one('doc.send', 'Related Send', ondelete='restrict', copy=False)
    # trans_number = fields.Char(string='Sending Transmittal Number',  copy=False)
    # trans_date = fields.Date(string='Transmittal Date',  copy=False)
    # due_date = fields.Date(string='Due Date',  copy=False)
    # need_to_response = fields.Date(string='Need to Response',  copy=False)
    # antam_date = fields.Date(string='Antam Receive Date',  copy=False)
    #
    # rece_id = fields.Many2one('doc.rece', 'Related Receiving', ondelete='restrict', copy=False)
    # recv_trans_number = fields.Char(string='Receiving Transmittal Number',  copy=False)
    # recv_rece_date = fields.Date(string='Receiving Date',  copy=False)
    # recv_comment = fields.Many2one('conf.rec.comment', 'Status Comment', ondelete='restrict', copy=False)


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

    @api.multi
    def done(self):
        self.state='done'

    @api.one
    def unlink(self):
        text = "Please unlink this document from IDC / Sending / Receiving Transmittal"
        if self.idc_id.id != False:
            raise Warning(text)
            return
        elif self.send_id.id != False:
            raise Warning(text)
            return
        elif self.rece_id.id != False:
            raise Warning(text)
            return
        else:
            return super(master_deliver, self).unlink()
