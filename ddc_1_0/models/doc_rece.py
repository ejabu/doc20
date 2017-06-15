from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta

from openerp.exceptions import UserError

class doc_rece(models.Model):

    _name= "doc.rece"
    _inherit = ['mail.thread']

    recipient = fields.Many2one('res.partner', string='Recipient', required=True, copy=False)
    name = fields.Char(string='Incoming Transmittal Number', required=True)

    recv_rece_date = fields.Date(string='Transmittal Date', required=True)


    # line_ids = fields.One2many('master.deliver', 'rece_id', 'MDR Line')
    line_ids = fields.Many2many('master.deliver', 'master_to_rece', 'rece_id', 'line_ids', string="Related MDR", copy=False)
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    _defaults={
        'state': 'new',
        'recv_rece_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
    }

    @api.onchange('line_ids','name')
    def oc_name(self):
        for rec in self.line_ids:
            rec.write({'recv_trans_number': self.name})

    @api.onchange('recv_rece_date', 'line_ids')
    def oc_recv_rece_date(self):
        for rec in self.line_ids:
            rec.write({'recv_rece_date': self.recv_rece_date})


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
        parent_ids, child_ids, all_counter = doc_rece._check_child_id(self)
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
        self.line_ids.write({'recv_trans_number': self.name})
        self.line_ids.write({'recv_rece_date': self.recv_rece_date})

    @api.multi
    def force_oc(self):
        for amplop in self.search([]):
            amplop._force_oc()


    @api.multi
    def remap_exstat(self):
        eja = self.line_ids.mapped('version_id')
        for ej in eja:
            ej.renotes()
        return

    @api.multi
    def write(self, vals):
        # import ipdb; ipdb.set_trace()
        res = super(doc_rece, self).write(vals)
        self.remap_exstat()
        return res
