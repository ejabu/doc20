from openerp import api
from openerp import models, fields


class conf_rec_comment(models.Model):

    _name= "conf.rec.comment"

    name = fields.Char(string='Message')
