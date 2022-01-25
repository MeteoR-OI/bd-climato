update agg_todo set status = 0;
delete from agg_histo;
delete from agg_hour;
delete from agg_day;
delete from agg_month;
delete from agg_year;
delete from agg_all;

update tmp_agg_todo set status = 0;
delete from tmp_agg_histo;
delete from tmp_agg_hour;
delete from tmp_agg_day;
delete from tmp_agg_month;
delete from tmp_agg_year;
delete from tmp_agg_all;

delete from incident;
