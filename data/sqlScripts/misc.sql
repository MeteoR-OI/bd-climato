select 
    a.id as agg_histo_id,
    o.stop_dat as obs_stop_dat,
    a.agg_level as level,
    ah.start_dat as start_H,
    ad.start_dat as start_D,
    a.j['out_temp_s'] as out_temp_s,
    a.j['out_temp_d'] as out_temp_d 
    
    from agg_histo a
        join obs o on o.id = a.obs_id 
        left join agg_hour ah on ah.id = a.agg_id and a.agg_level = 'H'
        left join agg_day ad on ad.id = a.agg_id and a.agg_level = 'D' 
        
    where a.j['out_temp_d'] is not null;

select 
    a.id as agg_histo_id,
    o.stop_dat as obs_stop_dat,
    a.agg_level as level,
    ah.start_dat as start_H,
    ad.start_dat as start_D,
    a.j['out_temp_omm_max'] as out_temp_omm_max,
    a.j['out_temp_omm_max_time'] as out_temp_omm_max_time 
    
    from agg_histo a
        join obs o on o.id = a.obs_id 
        left join agg_hour ah on ah.id = a.agg_id and a.agg_level = 'H'
        left join agg_day ad on ad.id = a.agg_id and a.agg_level = 'D' 
        
    where a.j['out_temp_omm_max_time'] is not null;


CREATE OR REPLACE FUNCTION
  get_obs_key(obs_id bigint, keystr varchar(255) default 'out_temp')
  RETURNS TABLE(histo_id bigint, obs_stop_dat text, level varchar(2), start_agg_H text, start_agg_D text, sum_value text, avg_value text, duration text, ah_id bigint, ad_id bigint)
AS $CODE$
select 
    a.id as histo_id,
    o.stop_dat as obs_stop_dat,
    a.agg_level as level,
    ah.start_dat as start_agg_H,
    ad.start_dat as start_agg_D,
    a.j[concat(keystr, '_s')] as sum_value,
    a.j[concat(keystr, '_avg')] as avg_value,
    a.j[concat(keystr, '_d')] as duration,
    ah.id as ah_id,
    ad.id as ad_id
    
    from agg_histo a
        join obs o on o.id = a.obs_id 
        left join agg_hour ah on ah.id = a.agg_id and a.agg_level = 'H' and ah.poste_id = o.poste_id
        left join agg_day ad on ad.id = a.agg_id and a.agg_level = 'D' and ad.poste_id = o.poste_id
        
    where a.obs_id = obs_id and a.j[concat(keystr, '_d')] is not null
    order by a.agg_level, a.id;
  $CODE$
  LANGUAGE sql IMMUTABLE;
