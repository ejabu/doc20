SELECT
*
-- CURRENT_DATE - 7 + cast(abs(extract(dow from current_date) - 7 )+ 1 as int) as haha
FROM report_stat_real

WHERE
week_date = (
CURRENT_DATE - 7 + cast(abs(extract(dow from current_date) - 7 )+ 1 as int)
)



-----------

BEGIN;

INSERT INTO report_stat_real as hehe

        SELECT
        (random()*200)::int as id,
        to_char(next_week_date,'DD-Mon-YY') as week_name,
        next_week_date as week_date,
        IFI as ifi,
        IFR as ifr,
        IFA as ifa,
        AFC as afc,
        IFR - IFI as def_ifr,
        IFA - IFR as def_ifa,
        AFC - IFA as def_afc

        FROM (
            SELECT
            (CURRENT_DATE + cast(abs(extract(dow from current_date) - 7)+ 1 as int)) as next_week_date,
            sum(case when exs.name  = 'IFI' then 1 else 0 end) as IFI,
            sum(case when exs.name  = 'IFR' then 1 else 0 end) as IFR,
            sum(case when exs.name  = 'IFA' then 1 else 0 end) as IFA,
            sum(case when exs.name  = 'AFC' then 1 else 0 end) as AFC
            FROM master_deliver mdr JOIN conf_external_status exs ON mdr.external_status = exs.id
            WHERE is_history is FALSE
            ) b ;



COMMIT;


------------------------------


BEGIN;

INSERT INTO report_stat_real (id,week_name, week_date, ifi, ifr, ifa, afc, def_ifr, def_ifa, def_afc, diff_IFI, diff_IFR, diff_IFA, diff_AFC)

        SELECT
        (random()*200)::int as id,
        to_char(next_week_date,'DD-Mon-YY') as week_name,
        next_week_date as week_date,
        this_week.IFI as ifi,
        this_week.IFR as ifr,
        this_week.IFA as ifa,
        this_week.AFC as afc,
        this_week.IFR - this_week.IFI as def_ifr,
        this_week.IFA - this_week.IFR as def_ifa,
        this_week.AFC - this_week.IFA as def_afc,
        this_week.IFI - last_week.IFI as diff_IFI,
        this_week.IFR - last_week.IFR as diff_IFR,
        this_week.IFA - last_week.IFA as diff_IFA,
        this_week.AFC - last_week.AFC as diff_AFC


        FROM (
            SELECT
            (CURRENT_DATE + cast(abs(extract(dow from current_date) - 7)+ 1 as int)) as next_week_date,
            sum(case when exs.name  = 'IFI' then 1 else 0 end) as IFI,
            sum(case when exs.name  = 'IFR' then 1 else 0 end) as IFR,
            sum(case when exs.name  = 'IFA' then 1 else 0 end) as IFA,
            sum(case when exs.name  = 'AFC' then 1 else 0 end) as AFC
            FROM master_deliver mdr JOIN conf_external_status exs ON mdr.external_status = exs.id
            WHERE is_history is FALSE
        ) this_week
,
        (
            SELECT
            max(IFI) IFI,
            max(IFR) IFR,
            max(IFA) IFA,
            max(AFC) AFC,
            FROM report_stat_real as hehe

            WHERE
            week_date = (
            CURRENT_DATE - 7 + cast(abs(extract(dow from current_date) - 7 )+ 1 as int)
            )

        ) last_week

;

COMMIT;









--------------------------------------------



---Dummy



INSERT INTO report_stat_real as hehe (id, week_name, week_date, ifi, ifr, ifa, afc, def_ifr, def_ifa, def_afc, diff_IFI, diff_IFR, diff_IFA, diff_AFC)

        SELECT

        nextval('report_stat_real_id_seq') as id,
        '26-Jun-17' as week_name,
        '2017-06-26' as week_date,
        30 as ifi,
        40 as ifr,
        30 as ifa,
        0 as afc,
        3 as def_ifr,
        4 as def_ifa,
        4 as def_afc,
        3 as diff_IFI,
        4 as diff_IFR,
        4 as diff_IFA,
        4 as diff_AFC
