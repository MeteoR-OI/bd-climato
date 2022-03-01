select 'hour' as agg_hour, poste_id, start_dat, count(*) from agg_hour group by 1, 2, 3 having count(*) > 1;
select 'day' as agg_day, poste_id, start_dat, count(*) from agg_day group by 1, 2, 3 having count(*) > 1;
select 'month' as agg_month, poste_id, start_dat, count(*) from agg_month group by 1, 2, 3 having count(*) > 1;
select 'year' as agg_year, poste_id, start_dat, count(*) from agg_year group by 1, 2, 3 having count(*) > 1;
select 'all' as agg_all, poste_id, start_dat, count(*) from agg_all group by 1, 2, 3 having count(*) > 1;

