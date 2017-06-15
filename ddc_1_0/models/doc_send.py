from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta

from openerp.exceptions import UserError

class doc_send(models.Model):

    _name= "doc.send"
    _inherit = ['mail.thread']

    name = fields.Char(string='Transmittal Number', required=True)
    recipient = fields.Many2one('res.partner', string='-', copy=False)
    recipient_ids = fields.Many2many('res.partner', 'send_rel_partner', 'send_ids', 'recipient_ids', string='Recipient', required=True, copy=False)
    recipient_rece_date = fields.Date(string='Recipient Receive Date')

    trans_date = fields.Date(string='Transmittal Date', required=True)
    trans_due_date = fields.Date(string='Due Date',)

    # line_ids = fields.One2many('master.deliver', 'send_id', 'MDR Line')
    line_ids = fields.Many2many('master.deliver', 'master_to_send', 'send_id', 'line_ids', string="Related MDR", copy=False)
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'trans_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.onchange('line_ids','name')
    def oc_name(self):
        self.line_ids.write({'trans_number': self.name})

    @api.onchange('line_ids','trans_date')
    def oc_trans_date(self):
        self.line_ids.write({'trans_date': self.trans_date})

    @api.onchange('line_ids','trans_due_date')
    def oc_trans_due_date(self):
        self.line_ids.write({'trans_trans_due_date': self.trans_due_date})


    @api.onchange('line_ids','recipient_rece_date')
    def oc_recipient_rece_date(self):
        self.line_ids.write({'recipient_rece_date': self.recipient_rece_date})


    @api.multi
    def rewrite_relation(self):

        all_counter = 0
        counter = 0
        message = "Check berapa banyak MDR yang terhubung, namun sebenarnya belum pernah Update Revisi / Update Status \n \n"
        for doc in self.search([]):
            doc_send_name = doc.name
            for line in doc.line_ids:
                all_counter += 1
                if len(line.history_ids) > 0 :
                # if len(line.history_ids) == 0 :
                    counter += 1
                    server_log = "%s : \n Outgoing Trans : %s \n MDR Name : %s  \n Jumlah history_ids : %s \n" % (counter, doc_send_name, line.name, len(line.history_ids))
                    message += server_log

        message += '\n Total Doc yang ada Relasi : %s \n' % all_counter
        message += 'Total Doc yang ada Bermasalah : %s \n' % counter

        raise UserError(message)

    @api.multi
    def _check_duplicate(self):
        counter = 0
        all_counter = 0
        message = "Check berapa banyak MDR yang punya anak lebih dari 1 \n \n"
        anak_to_kill=[]
        for mdr in self.env['master.deliver'].search([['is_history', '=', False]]):
            all_counter +=1
            if len(mdr.history_ids) > 1 :
                counter += 1
                history_ids = mdr.history_ids
                sorted_history_ids = history_ids.sorted(key=lambda r: r.status_date, reverse=True).sorted(key=lambda r: r.rev_num_seq, reverse=True).ids
                del sorted_history_ids[0]
                anak_to_kill.extend(sorted_history_ids)
                log = '''%s : \n
                         MDR Name : %s \n
                         Jumlah Anak : %s \n
                ''' % (counter, mdr.name, len(mdr.history_ids))
                message += log

        message += 'Total Doc yang ada: %s \n' % all_counter
        message += 'Total Doc yang ada Bermasalah : %s \n' % counter
        message += 'ID To Delete : %s \n' % anak_to_kill

        return anak_to_kill, message


    @api.multi
    def remove_duplicate(self):
        anak_to_kill, message = doc_send._check_duplicate(self)
        self.env['master.deliver'].search([['id', 'in', anak_to_kill]]).unlink()
        return

    @api.multi
    def check_duplicate(self):
        anak_to_kill, message = doc_send._check_duplicate(self)
        raise UserError(message)
        return

    @api.multi
    def _check_child_id(self):
        child_ids=[]
        parent_ids=[]
        all_counter = 0
        for amplop in self.search([]):
            amplop_name = amplop.name
            parent_ids.extend(amplop.line_ids.ids)
            for line in amplop.line_ids:
                # menghitung jumlah linked MDR
                all_counter += 1
                if len(line.history_ids) == 1 :
                    # mencari ID Child
                    child_ids.append(line.history_ids[0].id)

        return parent_ids, child_ids, all_counter

    @api.multi
    def check_child_id(self):
        parent_ids, child_ids, all_counter = doc_send._check_child_id(self)
        message = "Check berapa banyak MDR yang terhubung, namun sebenarnya Terhubung ke Parent bukan ke Child \n \n"
        message += 'Jumlah Linked MDR : %s \n' % all_counter
        message += 'Parent ID : %s \n' % parent_ids
        message += '\n\n Child ID : %s \n' % child_ids

        raise UserError(message)
        return


    @api.multi
    def tukar_relasi(self):
        # counter = 0
        for amplop in self.search([]):
            # if counter > 6:
            #     break
            amplop_name = amplop.name
            child_ids_to_link = []
            parent_ids_to_unlink = []
            for line in amplop.line_ids:
                # harus yang LEN == 1, karena semua duplikat sudah di delete
                if len(line.history_ids) == 1 :
                    child_ids_to_link.append((4, line.history_ids[0].id))
                    parent_ids_to_unlink.append((3, line.id))
            # import ipdb; ipdb.set_trace()
            # amplop.write({
            #     'line_ids':[
            #     (   6,
            #         0,
            #         child_id_to_link
            #     )
            #     ]
            #
            # })

            amplop.write({
                'line_ids' : parent_ids_to_unlink
            })
            amplop.write({
                'line_ids' : child_ids_to_link
            })
            # counter+=1
        return




    def _force_oc(self):
        self.line_ids.write({'trans_number': self.name})
        self.line_ids.write({'trans_date': self.trans_date})
        self.line_ids.write({'trans_trans_due_date': self.trans_due_date})
        self.line_ids.write({'recipient_rece_date': self.recipient_rece_date})

    @api.multi
    def force_oc(self):
        for amplop in self.search([]):
            amplop._force_oc()


    @api.multi
    def pass_partner(self):
        for amplop in self.search([]):
            if amplop.recipient:
                if amplop.recipient.id in amplop.recipient_ids.ids:
                    print 'already a recipient'
                else:
                    amplop.write({
                        'recipient_ids' : [(4, amplop.recipient.id)]
                    })
                    print 'add'
            else:
                print 'no recipient'

    @api.multi
    def write_parent_date(self):
        hist_ids = self.env['master.deliver'].search([['is_history', '=', False]])
        for hist in hist_ids:
            hist.renotes()
        return

    @api.multi
    def remap_exstat(self):
        eja = self.line_ids.mapped('version_id')
        for ej in eja:
            ej.renotes()
        return

    @api.multi
    def write(self, vals):
        # import ipdb; ipdb.set_trace()
        res = super(doc_send, self).write(vals)
        self.remap_exstat()
        return res

    # @api.model
    # def create(self, vals):
    #     res = super(master_deliver, self).create(vals)
    #     return res
    #
