delete from obs;
delete from histo_obs;
delete from extremes;
delete from histo_extreme;
delete from incidents;
update postes set  last_obs_id=0, last_obs_date=null, last_extremes_id=0, last_extremes_date=null;
