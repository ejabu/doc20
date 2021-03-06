from openerp import api
from openerp import models, fields


class conf_discipline(models.Model):
    _name= "conf.discipline"
    name = fields.Char(string='Discipline', required=True)
    categ_ids = fields.One2many('conf.doc.categ', 'discipline', 'Related Category')
    sub_ids = fields.One2many('conf.doc.sub', 'discipline', 'Related Subsystem')
    type_ids = fields.One2many('conf.doc.type', 'discipline', 'Related Type')

class conf_doc_categ(models.Model):
    _name= "conf.doc.categ"
    name = fields.Char(string='Document Category', required=True)
    desc = fields.Char(string='Description', required=True)
    discipline = fields.Many2one('conf.discipline', 'Discipline', required=True, ondelete='restrict')

class conf_doc_sub(models.Model):
    _name= "conf.doc.sub"
    name = fields.Char(string='Document Subsystem', required=True)
    discipline = fields.Many2one('conf.discipline', 'Discipline', required=True, ondelete='restrict')

class conf_doc_type(models.Model):
    _name= "conf.doc.type"
    name = fields.Char(string='Document Type', required=True)
    desc = fields.Char(string='Description', required=True)
    discipline = fields.Many2one('conf.discipline', 'Discipline', required=True, ondelete='restrict')

class conf_doc_status(models.Model):
    _name= "conf.doc.status"
    name = fields.Char(string='Document Status', required=True)

class conf_rev_num(models.Model):
    _name= "conf.rev.num"

    _order = 'sequence'

    name = fields.Char(string='Document Rev Number', required=True)
    sequence = fields.Integer('Sequence', required=True, help='Use to arrange calculation sequence', select=True)

    _defaults = {
        'sequence': 10,
    }
class conf_internal_status(models.Model):
    _name= "conf.internal.status"
    name = fields.Char(string='Document Internal Status', required=True)
    _order = 'sequence'
    sequence = fields.Integer('Sequence', required=True, help='Use to arrange calculation sequence', select=True)

    _defaults = {
        'sequence': 10,
    }
class conf_external_status(models.Model):
    _name= "conf.external.status"
    _order = 'sequence'
    name = fields.Char(string='Document External Status', required=True)
    sequence = fields.Integer('Sequence', required=True, help='Use to arrange calculation sequence', select=True)

    _defaults = {
        'sequence': 10,
    }
