
from openerp import tools
from openerp.osv import fields, osv

class dash_sent(osv.osv):
    _name = "dash.sent"
    _description = "Dashboard sent"
    _auto = False

    _columns = {
        'external_status' : fields.many2one('conf.external.status', 'External Status', readonly=True),
        'name': fields.char('Name', readonly=True),
        'trans_date': fields.datetime('Outgoing Date', readonly=True),
        'date_diff': fields.integer('Day Diff', readonly=True),
        'count': fields.integer('Amount of Document', readonly=True),
    }

    def _select(self):
        select_str = """
            SELECT
                min(mdr.id) as id,
                mdr.external_status as external_status,
                mdr.name as name,
                mdr.trans_date as trans_date,
                now()::date - mdr.trans_date as date_diff,
                count(*) as count
        """
        return select_str

    def _from(self):
        from_str = """

            master_deliver mdr
            WHERE is_history is False
                    AND trans_date is not NULL
                    AND recv_rece_date is NULL
                    AND external_status is not NULL
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                mdr.external_status,
                mdr.name,
                mdr.trans_date
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
