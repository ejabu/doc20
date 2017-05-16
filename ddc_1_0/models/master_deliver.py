from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

from openerp.exceptions import Warning

class master_deliver(models.Model):

    _name= "master.deliver"
    _order = "create_date"


    def _get_default(self):
        import ipdb; ipdb.set_trace()
        return


    @api.model
    def default_get(self, fields):
        rec = super(master_deliver, self).default_get(fields)
        if self._context.get('is_updating_rev'):
            rec.update({
                'external_status': self._context.get('update_external_status'),
                'status_date': self._context.get('update_status_date'),
            })
        elif self._context.get('is_updating_status'):
            rec.update({
                'rev_num': self._context.get('update_rev_num'),
                'revision_date': self._context.get('update_revision_date'),
            })
        return rec
    # @api.one
    def _set_external(self):
        pass

    @api.one
    @api.depends('history_ids')
    def _get_external(self):
        for record in self:
            if record.is_history is False :
                #Mengecek Urutan Terakhir berdasarkan status_date, kemudian rev_num_seq
                tes = record.history_ids.sorted(key=lambda r: r.status_date, reverse=True).sorted(key=lambda r: r.rev_num_seq, reverse=True)
                if len(tes) > 0:
                    record.external_status = tes[0].external_status
                    record.status_date = tes[0].status_date
                    record.rev_num = tes[0].rev_num
                    record.revision_date = tes[0].revision_date
            elif self._context.get('external_status') is not None:
                record.external_status = self._context.get('external_status')
                record.status_date = self._context.get('status_date')
            elif self._context.get('rev_num') is not None:
                record.rev_num = self._context.get('rev_num')
                record.revision_date = self._context.get('revision_date')


    discipline = fields.Many2one('conf.discipline', 'Discipline', ondelete='restrict', copy=True)
    doc_categ = fields.Many2one('conf.doc.categ', 'Category', ondelete='restrict', copy=True)
    doc_sub = fields.Many2one('conf.doc.sub', 'Subsystem', ondelete='restrict', copy=True)
    name = fields.Char(string='Document Number', copy=True)
    doc_title = fields.Char(string='Document Title', copy=True)
    doc_type = fields.Many2one('conf.doc.type', 'Document Type', ondelete='restrict', copy=True)
    doc_type_desc = fields.Char(string='Type Description', related='doc_type.desc', store=True)

    originator = fields.Many2one('res.partner', string='Originator', copy=False)

    version_id = fields.Many2one('master.deliver', string='Versions', copy=False)
    history_ids = fields.One2many('master.deliver', 'version_id', 'History', copy=False)

    revision_date = fields.Date(string='Revision Date')
    status_date = fields.Date(string='Status Date')
    is_history = fields.Boolean(string='Is History')


    doc_status = fields.Many2one('conf.doc.status', 'Status', ondelete='restrict', copy=False)
    rev_num = fields.Many2one('conf.rev.num', 'Revision Number', ondelete='restrict', copy=False)
    rev_num_seq = fields.Integer(string='Sequence', related='rev_num.sequence', store=False)

    #IFA IFI RE-IDC
    external_status = fields.Many2one('conf.external.status', 'External Status', compute='_get_external', inverse='_set_external', store=True)

    doc_pred = fields.Char(string='Predecessor', copy=True)
    alt_doc = fields.Char(string='Alternative Document #', copy=True)


    notes = fields.Text(string='Notes', copy=True)
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    idc_id = fields.Many2one('doc.idc', 'IDC', ondelete='restrict', copy=False)
    # idc_id = fields.Many2many('doc.idc', 'master_to_idc', 'line_ids', 'idc_id', string="Related IDC", copy=False)
    idc_number = fields.Char(string='IDC Number', copy=False)
    created_date = fields.Date(string='Created Date', default=lambda self: self._context.get('date', fields.Date.context_today(self)))
    sched_plan = fields.Date(string='Schedule Plan')
    sched_date = fields.Date(string='Schedule Date')
    send_date = fields.Date(string='IDC Sending Date', copy=False)
    rece_date = fields.Date(string='IDC Receiving Date', copy=False)
    due_date = fields.Date(string='Due Date', copy=False)
    status_comment = fields.Many2one('conf.rec.comment', 'Status Comment')

    #SEND_ID dan RECE_ID selamanya harus selalu dipisah
    #KARENA Amplop dari Pihak Ketiga, selalu rapih dan juga dicatat.
    #BERBEDA dengan IDC yang ketika dokumennya diterima, amplop dari pihak ketiga diabaikan

    send_id = fields.Many2many('doc.rece', 'master_to_send', 'line_ids', 'send_id', string="Related Sending", copy=False)
    trans_number = fields.Char(string='Outgoing Transmittal Number', copy=False)
    trans_date = fields.Date(string='Transmittal Date', copy=False)
    trans_due_date = fields.Date(string='Transmittal Due Date', copy=False)

    recipient_rece_date = fields.Date(string='Recipient Receive Date', copy=False)

    rece_id = fields.Many2many('doc.rece', 'master_to_rece', 'line_ids', 'rece_id', string="Related Receiving", copy=False)
    recv_trans_number = fields.Char(string='Incoming Transmittal Number', copy=False)
    recv_rece_date = fields.Date(string='Receiving Date', store=True, copy=False)
    recv_comment = fields.Many2one('conf.rec.comment', 'Status Comment', ondelete='restrict', copy=False)


    _defaults = {
        # 'state': 'new',
    }

    _sql_constraints = [
        ('name', 'Check(1=1)', "The system record Can't be duplicate value for this field!")
        # ('name', 'unique(name)', "The system record Can't be duplicate value for this field!")
    ]


    @api.model
    def create(self, vals):
        if self._context.get("update") is not None:
            if vals['is_history']:
                if vals['version_id']:
                    parent_obj = self.browse(vals['version_id'])
                    vals['discipline'] = parent_obj.discipline.id
                    vals['doc_categ'] = parent_obj.doc_categ.id
                    vals['doc_sub'] = parent_obj.doc_sub.id
                    vals['name'] = parent_obj.name
                    vals['doc_title'] = parent_obj.doc_title
                    vals['doc_pred'] = parent_obj.doc_pred
                    vals['alt_doc'] = parent_obj.alt_doc
                    vals['doc_type'] = parent_obj.doc_type.id
                    vals['sched_plan'] = parent_obj.sched_plan
                    vals['notes'] = parent_obj.notes
                    vals['is_history'] = True
            if self._context.get("update") == "status":
                context_to_pass={
                    'external_status': vals['external_status'],
                    'status_date': vals['status_date'],
                    'parent_id': vals['version_id']
                }
            elif self._context.get("update") == "rev":
                context_to_pass={
                    'rev_num': vals['rev_num'],
                    'revision_date': vals['revision_date'],
                    'parent_id': vals['version_id']
                }
            res = super(master_deliver, self.with_context(context_to_pass)).create(vals)
            return res
        else:
            res = super(master_deliver, self).create(vals)
            return res

    @api.one
    def unlink(self):
        text = "Please unlink this document from IDC / Sending / Incoming Transmittal"
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
