
from openerp import tools
from openerp.osv import fields, osv

class stat_real(osv.osv):
    _name = "stat.real"
    _description = "Dashboard Status Realisasi"
    _auto = False

    _columns = {
        'external_status': fields.char('External Status', readonly=True),
        'weekly': fields.datetime('Weekly', readonly=True),
        'count': fields.integer('Count', readonly=True),
    }

    def init(self, cr):
            tools.drop_view_if_exists(cr, self._table)
            cr.execute("""CREATE or REPLACE VIEW %s as (


SELECT
(random()*200)::int AS id,

a.external_status as external_status,
b.weekz as weekly,
a.count as count


FROM
(

SELECT
min(mdr.id) as id,
exs.name as external_status,
to_char(date_trunc('week', mdr.revision_date) ,'DD-Mon-YY') as weekly,
COUNT(*) as count

FROM master_deliver mdr JOIN conf_external_status exs ON mdr.external_status = exs.id
WHERE is_history is TRUE
AND revision_date >  CURRENT_DATE - INTERVAL '3 months'
AND exs.name in ('IFI','IFA','IFR','IFC')

GROUP BY mdr.external_status, exs.name, weekly
ORDER BY weekly

) a




--SUPAYA KEAMBIL SEMUA WEEK WALAUPUN NULL
RIGHT JOIN
   (
SELECT



to_char(timestamp ,'DD-Mon-YY') as weekz

FROM

generate_series(

((CURRENT_DATE + cast(abs(extract(dow from current_date) - 7)+ 1 as int)) - INTERVAL '3 months'), CURRENT_DATE, '1 week'::interval

) as timestamp

) b

ON a.weekly = b.weekz




                )""" % (self._table))
