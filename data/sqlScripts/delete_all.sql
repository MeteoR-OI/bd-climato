delete from obs;
delete from x_min;
delete from x_max;
delete from incidents;
update postes set  last_obs_id=0, last_obs_date=null, last_extremes_id=0, last_extremes_date=null;
