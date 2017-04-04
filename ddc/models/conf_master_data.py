from openerp import api
from openerp import models, fields


class conf_discipline(models.Model):
    _name= "conf.discipline"
    name = fields.Char(string='Discipline')

class conf_doc_categ(models.Model):
    _name= "conf.doc.categ"
    name = fields.Char(string='Document Category')

class conf_doc_sub(models.Model):
    _name= "conf.doc.sub"
    name = fields.Char(string='Document Subsystem')

class conf_doc_type(models.Model):
    _name= "conf.doc.type"
    name = fields.Char(string='Document Type')

class conf_rev_num(models.Model):
    _name= "conf.rev.num"
    name = fields.Char(string='Document Rev Number')

class conf_internal_status(models.Model):
    _name= "conf.internal.status"
    name = fields.Char(string='Document Internal Status')
    
class conf_external_status(models.Model):
    _name= "conf.external.status"
    name = fields.Char(string='Document External Status')
