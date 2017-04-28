
from openerp import tools
from openerp.osv import fields, osv

class mdr_pivot(osv.osv):
    _name = "mdr.pivot"
    _description = "Docment Statistics"
    _auto = False
    # _rec_name = 'date'

    _columns = {
        'discipline' : fields.many2one('conf.discipline', 'Discipline', readonly=True),
        'doc_status' : fields.many2one('conf.doc.status', 'Status', readonly=True),
        'external_status' : fields.many2one('conf.external.status', 'External Status', readonly=True),
        'sched_date' : fields.date(string='Schedule Date', readonly=True),
        'recv_comment' : fields.many2one('conf.rec.comment', 'Status Comment', readonly=True),
        'count': fields.integer('Count', readonly=True),
    }



    def _select(self):
        select_str = """
            SELECT
                min(mdr.id) as id,
                mdr.discipline as discipline,
                mdr.doc_status as doc_status,
                mdr.external_status as external_status,
                mdr.sched_date as sched_date,
                mdr.recv_comment as recv_comment,
                count(*) as count

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
                mdr.discipline,
                mdr.doc_status,
                mdr.external_status,
                mdr.sched_date,
                mdr.recv_comment
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
