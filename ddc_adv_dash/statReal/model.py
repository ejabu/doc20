# -*- coding: utf-8 -*-

# from openerp import tools
# from openerp.osv import fields, osv
from openerp import fields, models, tools
from sql_script import *

class stat_real(models.Model):
    _name = "stat.real"
    _description = "Dashboard Status Realisasi"
    _auto = False

    # id = fields.Integer('Count', readonly=True)
    # string = fields.Char('string', readonly=True)
    # string = fields.Date('string', readonly=True)
    # string = fields.Integer('string', readonly=True)


    week_name = fields.Char('Week Name', readonly=True, store=False)
    week_date = fields.Date('Date', readonly=True)
    ifi = fields.Integer('IFI', readonly=True, store=False)
    ifr = fields.Integer('IFR', readonly=True, store=False)
    ifa = fields.Integer('IFA', readonly=True, store=False)
    afc = fields.Integer('AFC', readonly=True, store=False)
    def_ifr = fields.Integer('def_ifr', readonly=True, store=False)
    def_ifa = fields.Integer('def_ifa', readonly=True, store=False)
    def_afc = fields.Integer('def_afc', readonly=True, store=False)
    diff_ifi = fields.Integer('diff_IFI', readonly=True, store=False)
    diff_ifr = fields.Integer('diff_IFR', readonly=True, store=False)
    diff_ifa = fields.Integer('diff_IFA', readonly=True, store=False)
    diff_afc = fields.Integer('diff_AFC', readonly=True, store=False)

    def ejaboy(self, cr, user, allfields=None, context=None, write_access=True, attributes=None):
        # import ipdb; ipdb.set_trace()
        cr.execute(periodic_script)


    def init(self, cr):
        tools.drop_view_if_exists(cr, 'stat_real')
        self.create_report_stat_real(cr)
        self.create_stat_real(cr) #harus diakhirkan karena memerukan real table, report_stat_real
        # import ipdb; ipdb.set_trace()



    def create_stat_real(self, cr):
        # Script ini untuk membentuk View bukan Table !!
        cr.execute("""CREATE or REPLACE VIEW stat_real as (
            SELECT
            *
            FROM report_stat_real
            )
        """)
        cr.commit()


    def create_report_stat_real(self, cr):
        # Script ini untuk membentuk Table bukan View !!
        cr.execute("""
            CREATE TABLE IF NOT EXISTS report_stat_real (
                id                      SERIAL NOT NULL, PRIMARY KEY(id),
                week_name               varchar(40), UNIQUE(week_name),
                week_date               date,
                IFI                     integer,
                IFR                     integer,
                IFA                     integer,
                AFC                     integer,
                def_IFR                 integer,
                def_IFA                 integer,
                def_AFC                 integer,
                diff_IFI                integer,
                diff_IFR                integer,
                diff_IFA                integer,
                diff_AFC                integer
            )

        """)
        cr.commit()
