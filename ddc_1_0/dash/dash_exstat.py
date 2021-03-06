
from openerp import tools
from openerp.osv import fields, osv

class dash_exstat(osv.osv):
    _name = "dash.exstat"
    _description = "Dashboard exstat"
    _auto = False

    _columns = {
        'external_status' : fields.many2one('conf.external.status', 'External Status', readonly=True),
        'count': fields.integer('Amount of Document', readonly=True),
    }

    def _select(self):
        select_str = """
            SELECT
                min(mdr.id) as id,
                mdr.external_status as external_status,
                count(*) as count
        """
        return select_str

    def _from(self):

        # master_deliver mdr
        #
        # WHERE is_history is False           : Cari yang Parent. bukan anak2nya. karena kalo sejuta tektok nanti Dokumennya makin banyak
        # AND external_status is not NULL     : Cari yang udah punya anak minimal satu sehingga tidak ada yang UNDEFINED
        # AND trans_date is not NULL          : Cari yang udah pernah dikirim via outgoing Transmittal
        from_str = """
            master_deliver mdr

            WHERE is_history is False
            AND rev_num > 0
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                mdr.external_status
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
