# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class popup_quiz(osv.osv_memory):

    _name = 'popup.quiz'
    _columns = {
        'correct': fields.char(string='Correct Answer'),
    }
