
from openerp import tools
from openerp.osv import fields, osv

class stat_real(osv.osv):
    _name = "stat.real"
    _description = "Dashboard Status Realisasi"
    _auto = False

    _columns = {
        'external_status': fields.integer('External Status', readonly=True),
        'weekly': fields.datetime('Weekly', readonly=True),
        'count': fields.integer('Count', readonly=True),
    }

    def _select(self):
        select_str = """
            SELECT
                min(mdr.id) as id,
                mdr.external_status as external_status,
                date_trunc('week', mdr.revision_date::date) as weekly,
                COUNT(*) as count
        """
        return select_str

    def _from(self):
        from_str = """
            master_deliver mdr
            WHERE is_history is TRUE
            AND revision_date >  CURRENT_DATE - INTERVAL '3 months'
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY external_status, weekly
            ORDER BY weekly

        """
        return group_by_str



    def init(self, cr):
            # self._table = sale_report
            tools.drop_view_if_exists(cr, self._table)
            cr.execute("""CREATE or REPLACE VIEW %s as (
                %s
                FROM %s
                %s
                )""" % (self._table, self._select(), self._from(), self._group_by()))
