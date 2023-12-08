-- Get status on obs loading, and extremes loading
select meteor, last_obs_date, last_obs_id, last_extremes_date, last_extremes_id from postes 
order by meteor


select meteor, last_obs_date, last_obs_id, last_extremes_date, last_extremes_id from postes 
where meteor in ('BP130', 'LAN030', 'MAT315', 'PAH575', 'PSL310', 'SPC010','TAN1270')
order by meteor
