select 'hour' as agg_hour, start_dat, count(*) from agg_hour group by 2, 1 having count(*) > 1;
select 'day' as agg_day, start_dat, count(*) from agg_day group by 2, 1 having count(*) > 1;
select 'month' as agg_month, start_dat, count(*) from agg_month group by 2, 1 having count(*) > 1;
select 'year' as agg_year, start_dat, count(*) from agg_year group by 2, 1 having count(*) > 1;
select 'all' as agg_all, start_dat, count(*) from agg_all group by 2, 1 having count(*) > 1;

select 'hour' as tmp_agg_hour, start_dat, count(*) from tmp_agg_hour group by 2, 1 having count(*) > 1;
select 'day' as tmp_agg_day, start_dat, count(*) from tmp_agg_day group by 2, 1 having count(*) > 1;
select 'month' as tmp_agg_month, start_dat, count(*) from tmp_agg_month group by 2, 1 having count(*) > 1;
select 'year' as tmp_agg_year, start_dat, count(*) from tmp_agg_year group by 2, 1 having count(*) > 1;
select 'all' as tmp_agg_all, start_dat, count(*) from tmp_agg_all group by 2, 1 having count(*) > 1;
