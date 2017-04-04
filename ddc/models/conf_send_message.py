from openerp import api
from openerp import models, fields


class conf_send_message(models.Model):

    _name= "conf.send.message"

    name = fields.Char(string='Message')
