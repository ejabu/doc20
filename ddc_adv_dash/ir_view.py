from openerp import fields, models


NEW_VIEW = ('statReal', 'statReal')


class IrUIView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[NEW_VIEW])
