
from openerp import tools
from openerp.osv import fields, osv

class dash_discipline(osv.osv):
    _name = "dash.discipline"
    _description = "Dashboard discipline"
    _auto = False

    _columns = {
        'discipline' : fields.many2one('conf.discipline', 'Discipline', readonly=True),
        # 'external_status' : fields.many2one('conf.external.status', 'External Status', readonly=True),
        'planned_count': fields.integer('Planned', readonly=True),
        'actual_count': fields.integer('Actual', readonly=True),
        'percentage': fields.float('Percentage', readonly=True , group_operator = 'avg'),
    }

    def _select(self):
        select_str = """
            SELECT
                min(mdr.id) as id,
                mdr.discipline as discipline,
                count(*) as planned_count,
                count(rev_num > 0) as actual_count,
                round((count(rev_num > 0)::decimal * 100.0 / count(*)::decimal ),2) as percentage

        """
        return select_str

    def _from(self):
        from_str = """
            master_deliver mdr

            WHERE is_history is False
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
