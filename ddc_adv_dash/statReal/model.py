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


    # def view_init(self, cr, uid, fields_list, context=None):
    #     import ipdb; ipdb.set_trace()
    #     print 'a'
    # def _auto_init(self, cr, context=None):
    #     import ipdb; ipdb.set_trace()
    #     print 'a'

    def ejaboy(self, cr, user, allfields=None, context=None, write_access=True, attributes=None):
        # import ipdb; ipdb.set_trace()
        cr.execute("""
        BEGIN;

        --- ALL FINALE

        ----BIKIN UNTUK PERTAMA KALI

        CREATE TABLE IF NOT EXISTS coba11 as (
        --30
            SELECT * ,
            to_char(revision_date ,'DD-Mon-YY') as week_name,
            IFR - IFI as defIFR,
            IFA - IFR as defIFA,
            AFC - IFA as defAFC

            FROM (
                SELECT
                (CURRENT_DATE + cast(abs(extract(dow from current_date) - 7)+ 1 as int)) as revision_date,
                sum(case when exs.name  = 'IFI' then 1 else 0 end) as IFI,
                sum(case when exs.name  = 'IFR' then 1 else 0 end) as IFR,
                sum(case when exs.name  = 'IFA' then 1 else 0 end) as IFA,
                sum(case when exs.name  = 'AFC' then 1 else 0 end) as AFC
                FROM master_deliver mdr JOIN conf_external_status exs ON mdr.external_status = exs.id
                WHERE is_history is FALSE
                ) a
        );

        ALTER TABLE coba11 DROP CONSTRAINT IF EXISTS unique_rev_10 ;
        ALTER TABLE coba11 ADD CONSTRAINT unique_rev_10 UNIQUE (revision_date);

        SELECT * FROM coba11;

        INSERT INTO coba11 as hehe

        SELECT * ,
        to_char(revision_date ,'DD-Mon-YY') as week_name,
        IFR - IFI as defIFR,
        IFA - IFR as defIFA,
        AFC - IFA as defAFC

        FROM (
            SELECT
            (CURRENT_DATE + cast(abs(extract(dow from current_date) - 7)+ 1 as int)) as revision_date,
            sum(case when exs.name  = 'IFI' then 1 else 0 end) as IFI,
            sum(case when exs.name  = 'IFR' then 1 else 0 end) as IFR,
            sum(case when exs.name  = 'IFA' then 1 else 0 end) as IFA,
            sum(case when exs.name  = 'AFC' then 1 else 0 end) as AFC
            FROM master_deliver mdr JOIN conf_external_status exs ON mdr.external_status = exs.id
            WHERE is_history is FALSE
            ) b
        on conflict (revision_date)
        do UPDATE

        SET (IFI, IFR,IFA, AFC, defIFR, defIFA, defAFC) =
        (
            SELECT
            a.IFI as IFI,
            a.IFR as IFR,
            a.IFA as IFA,
            a.AFC as AFC,
            IFR - IFI as defIFR,
            IFA - IFR as defIFA,
            random()*200 as defAFC
            FROM (
                SELECT

                sum(case when exs.name  = 'IFI' then 1 else 0 end) as IFI,
                sum(case when exs.name  = 'IFR' then 1 else 0 end) as IFR,
                sum(case when exs.name  = 'IFA' then 1 else 0 end) as IFA,
                sum(case when exs.name  = 'AFC' then 1 else 0 end) as AFC

                FROM master_deliver mdr JOIN conf_external_status exs ON mdr.external_status = exs.id

                WHERE is_history is FALSE
            ) a

        )

        where hehe.revision_date= hehe.revision_date;

        SELECT * FROM coba11;

        COMMIT;
        """)
    # print 'a'

    def init(self, cr):
            tools.drop_view_if_exists(cr, 'stat_real')
            # import ipdb; ipdb.set_trace()
            cr.execute("""CREATE or REPLACE VIEW stat_real as (
            SELECT
            row_number() OVER () AS id,

            week_name as weekly,
            week_name as external_status,
            defAFC as count
            FROM coba11
            )
            """)
            cr.commit()
