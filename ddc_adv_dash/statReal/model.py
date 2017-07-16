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


    week_name = fields.Char('Week Name', readonly=True, store=True)
    week_date = fields.Date('Date', readonly=True)
    ifi = fields.Integer('IFI', readonly=True, store=True)
    ifr = fields.Integer('IFR', readonly=True, store=True)
    ifa = fields.Integer('IFA', readonly=True, store=True)
    afc = fields.Integer('AFC', readonly=True, store=True)
    def_ifr = fields.Integer('def_ifr', readonly=True, store=True)
    def_ifa = fields.Integer('def_ifa', readonly=True, store=True)
    def_afc = fields.Integer('def_afc', readonly=True, store=True)
    diff_ifi = fields.Integer('diff_IFI', readonly=True, store=True)
    diff_ifr = fields.Integer('diff_IFR', readonly=True, store=True)
    diff_ifa = fields.Integer('diff_IFA', readonly=True, store=True)
    diff_afc = fields.Integer('diff_AFC', readonly=True, store=True)

    def fetch_report_stat_real(self, cr, user, allfields=None, context=None, write_access=True, attributes=None):
        cr.execute(periodic_script)


    def init(self, cr):
        tools.drop_view_if_exists(cr, 'stat_real')
        self.create_report_stat_real(cr)
        self.create_stat_real(cr) #harus diakhirkan karena memerukan real table, report_stat_real



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
