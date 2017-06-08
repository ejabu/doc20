from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta

from openerp.exceptions import UserError

class res_partner(models.Model):
    _inherit = "res.partner"

    send_ids = fields.Many2many('doc.send', 'send_rel_partner', 'recipient_ids', 'send_ids', string='Send IDS', copy=False)
