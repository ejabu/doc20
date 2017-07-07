# -*- coding: utf-8 -*-

# from openerp import tools
# from openerp.osv import fields, osv
from openerp import fields, models, tools

class stat_real(models.Model):
    _name = "stat.real"
    _description = "Dashboard Status Realisasi"
    _auto = False

    external_status = fields.Char('External Status', readonly=True)
    weekly = fields.Char('Weekly', readonly=True)
    count = fields.Integer('Count', readonly=True)

    def init(self, cr):
            tools.drop_view_if_exists(cr, 'stat_real')
            # import ipdb; ipdb.set_trace()
            cr.execute("""CREATE or REPLACE VIEW %s as (


SELECT
row_number() OVER () AS id,
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
