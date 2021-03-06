from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class master_deliver(models.Model):

    _name= "master.deliver"

    discipline = fields.Many2one('conf.discipline', 'Discipline', required=True)
    doc_categ = fields.Many2one('conf.doc.categ', 'Document Category')
    doc_sub = fields.Many2one('conf.doc.sub', 'Document Subsystem')
    name = fields.Char(string='Document Number', required=True)
    doc_title = fields.Char(string='Document Title')
    originator = fields.Many2one('res.partner', string='Originator', required=True)

    doc_pred = fields.Char(string='Document Predecessor')
    file_name = fields.Char(string='File Name')
    alt_doc = fields.Char(string='Alternative Document #')
    sched_date = fields.Date(string='Schedule Date')
    doc_type = fields.Many2one('conf.doc.type', 'Document Type')
    doc_status = fields.Many2one('conf.doc.status', 'Status')
    doc_status_update = fields.Many2one('conf.doc.status', 'Status')
    # rev_num = fields.Many2one('conf.rev.num', 'Revision Number')
    rev_num = fields.Integer('Revision Number')
    rev_num_update = fields.Integer('Revision Number')
    internal_status = fields.Many2one('conf.internal.status', 'Internal Status', required=True)
    external_status = fields.Many2one('conf.external.status', 'External Status')
    old_rev = fields.Char(string='Old Revision')
    notes = fields.Text(string='Notes')

    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    # history_seq = fields.Char(string='History')
    history_seq = fields.Char(string='History', required=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('master.deliver'))

    send_eng_id = fields.Many2many('send.eng.doc', 'master_to_send_eng', 'master_deliver_id', 'send_eng_id', string="Master Deliver", copy=False)
    rec_eng_id = fields.Many2many('rec.eng.doc', 'master_to_rec_eng', 'master_deliver_id', 'rec_eng_id', string="Master Deliver", copy=False)

    _defaults={
        'state': 'new',
        'rev_num': 0,
        'rev_num_update': 1,
    }

    @api.onchange('doc_status')
    def change_doc_status_update(self):
        self.doc_status_update = self.doc_status

    @api.multi
    def change_doc_status(self):
        pass


    @api.multi
    def action_view_invoice(self):
        pass
        # invoice_ids = self.mapped('invoice_ids')
        # imd = self.env['ir.model.data']
        # action = imd.xmlid_to_object('account.action_invoice_tree1')
        # list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        # form_view_id = imd.xmlid_to_res_id('account.invoice_form')
        #
        # result = {
        #     'name': action.name,
        #     'help': action.help,
        #     'type': action.type,
        #     'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
        #     'target': action.target,
        #     'context': action.context,
        #     'res_model': action.res_model,
        # }
        # if len(invoice_ids) > 1:
        #     result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
        # elif len(invoice_ids) == 1:
        #     result['views'] = [(form_view_id, 'form')]
        #     result['res_id'] = invoice_ids.ids[0]
        # else:
        #     result = {'type': 'ir.actions.act_window_close'}
        # return result


    # def change_doc_status(self, cr, uid, ids, context=None):
    #     dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'ddc', 'popup_quiz_form')
    #     return {
    #         'name':"Quiz",
    #         'view_mode': 'form',
    #         'view_id': view_id,
    #         'view_type': 'form',
    #         'res_model': 'popup.quiz',
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #     }


        # self.state='sent'
