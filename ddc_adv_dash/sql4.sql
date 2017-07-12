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
    AFC - IFA as defAFC
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
z
