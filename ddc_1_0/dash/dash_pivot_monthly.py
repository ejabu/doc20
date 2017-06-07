
from openerp import tools
from openerp.osv import fields, osv

class dash_pivot_monthly(osv.osv):
    _name = "dash.pivot.monthly"
    _description = "Dashboard Monthly"
    _auto = False

    _columns = {
        'discipline' : fields.many2one('conf.discipline', 'Discipline', readonly=True),
        'create_date' : fields.datetime(string='Create Date', readonly=True),
        'count': fields.integer('Amount of Document', readonly=True),
    }

    def _select(self):
        select_str = """
            SELECT
                min(mdr.id) as id,
                mdr.discipline as discipline,
                mdr.create_date as create_date,
                count(*) as count
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
                mdr.discipline,
                mdr.create_date
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
