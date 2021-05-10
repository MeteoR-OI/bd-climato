select start_dat as dat_hour, j->>'out_temp_omm_avg' as omm_h, j->>'out_temp_omm_max' as max_h, j->>'out_temp_omm_min' as min_h from agg_hour order by 1;
select start_dat as dat_dqy, j->>'out_temp_omm_avg' as omm_avg_d, j->>'out_temp_omm_max' as max_d, j->>'out_temp_omm_min' as min_d from agg_day order by 1;
select start_dat as dat_month, j->>'out_temp_omm_avg' as omm_avg_m, j->>'out_temp_omm_max' as max_m, j->>'out_temp_omm_min' as min_m from agg_month order by 1;
select start_dat as dat_year, j->>'out_temp_omm_avg' as omm_avg_y, j->>'out_temp_omm_max' as max_y, j->>'out_temp_omm_min' as min_y from agg_year order by 1;
