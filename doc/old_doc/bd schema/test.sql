
select
    timescaledb_experimental.time_bucket_ng('1 month', date_local) as date_local,
    sum(value) as value, 
    null as min,
    null as max
from obs join mesures on mesures.id = 52
WHERE
    date_local >= '1991-01-01T00:00:00.485Z'
    and date_local <= '2023-12-18T17:33:00.486Z' 
    and poste_id = 87 and
    mesure_id = 52
    and is_avg is FALSE 
group by 1

union all

select
    timescaledb_experimental.time_bucket_ng('1 month', date_local) as date_local, 
    null as value,
    sum(x_min.min) as min,
    null as max
from x_min join mesures on mesures.id = 52
WHERE
    date_local >= '1991-01-01T00:00:00.485Z'
    and date_local <= '2023-12-18T17:33:00.486Z' 
    and poste_id = 87
    and mesure_id = 52 
group by 1

union all

select
    timescaledb_experimental.time_bucket_ng('1 month', date_local) as date_local, 
    null as value,
    null as min,
    sum(x_max.max) as max
from x_max join mesures on mesures.id = 52
WHERE
    date_local >= '1991-01-01T00:00:00.485Z'
    and date_local <= '2023-12-18T17:33:00.486Z' 
    and poste_id = 87
    and mesure_id = 52 
group by 1

order by 1,3;
