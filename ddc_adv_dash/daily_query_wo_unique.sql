BEGIN;

INSERT INTO report_stat_real (id, week_name, week_date, ifi, ifr, ifa, afc, def_ifr, def_ifa, def_afc, diff_IFI, diff_IFR, diff_IFA, diff_AFC)

        SELECT
        -- random ini diperlukan ketika mau TEST dengan paginate_result tercentant pada phppgadmin
        --(random()*200)::int as id,
        nextval('report_stat_real_id_seq') as id,
        to_char(next_week_date,'DD-Mon-YY') as week_name,
        next_week_date as week_date,
        this_week.IFI as ifi,
        this_week.IFR as ifr,
        this_week.IFA as ifa,
        this_week.AFC as afc,
        this_week.IFR - this_week.IFI as def_ifr,
        this_week.IFA - this_week.IFR as def_ifa,
        this_week.AFC - this_week.IFA as def_afc,
        --COALESCE gunanya, ketika no rows found, nilai kolom akan dikurangi 0

        this_week.IFI - COALESCE( NULLIF(last_week.IFI, null) , '0' ) as diff_IFI,
        this_week.IFR - COALESCE( NULLIF(last_week.IFR, null) , '0' ) as diff_IFR,
        this_week.IFA - COALESCE( NULLIF(last_week.IFA, null) , '0' ) as diff_IFA,
        this_week.AFC - COALESCE( NULLIF(last_week.AFC, null) , '0' ) as diff_AFC


        FROM (
            SELECT
            (CURRENT_DATE + cast(abs(extract(dow from current_date) - 7 )+ 1 as int)) as next_week_date,
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
                --max gunanya, ketika no rows found, nilai kolom tetap ada yaitu NULL
                max(IFI) IFI,
                max(IFR) IFR,
                max(IFA) IFA,
                max(AFC) AFC
            FROM report_stat_real

            WHERE
            week_date = (
            CURRENT_DATE - 7 + cast(abs(extract(dow from current_date) - 7 )+ 1 as int)
            )

        ) last_week

;

COMMIT;
