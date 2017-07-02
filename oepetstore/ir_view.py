# # -*- coding: utf-8 -*-
# # Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
# from openerp import fields, models
#
#
# TIMELINE_VIEW = ('pivot2', 'Pivot2')
#
#
# class IrUIView(models.Model):
#     _inherit = 'ir.ui.view'
#
#     type = fields.Selection(selection_add=[TIMELINE_VIEW])
#
#
#
#
# class ActWindowView2(models.Model):
#     # _inherit = 'ir.actions.act_window'
#     _inherit = 'ir.actions.act_window.view'
#
#     view_mode = fields.Selection(selection_add=[TIMELINE_VIEW])


# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


TIMELINE_VIEW = ('ejaview', 'Ejaview')


class IrUIView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[TIMELINE_VIEW])
