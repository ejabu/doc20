
from openerp import tools
from openerp.osv import fields, osv

class stat_real(osv.osv):
    _name = "stat.real"
    _description = "Dashboard Status Realisasi"
    _auto = False

    _columns = {
        'planned_count': fields.integer('Planned', readonly=True, store=True),
    }

    def _select(self):
        select_str = """
            SELECT
                min(mdr.id) as id,
                mdr.discipline as planned_count
        """
        return select_str

    def _from(self):
        from_str = """
            master_deliver mdr
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                mdr.discipline

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
