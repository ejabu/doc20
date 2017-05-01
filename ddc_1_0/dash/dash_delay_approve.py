from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

from openerp.exceptions import Warning

class dash_delay_approve(models.Model):

    _name= "dash.delay.approve"

    name = fields.Char(string='Report Name', required=True)
    query_result= fields.Text(string='Query Result',)
