
select row_to_json(t)
from (
	select p.meteor as meteor,
	(	select jsonb_build_object('start_dat', h.start_dat, 'j', h.j) as hour 
		from agg_hour h
		where h.poste_id_id = p.id
		order by h.start_dat desc
		limit 1
	),(	select jsonb_build_object('start_dat', d.start_dat, 'j', d.j) as day 
		from agg_day d
		where d.poste_id_id = p.id
		order by d.start_dat desc
		limit 1
	),(	select jsonb_build_object('start_dat', m.start_dat, 'j', m.j) as month 
		from agg_month m
		where m.poste_id_id = p.id
		order by m.start_dat desc
		limit 1
	),(	select jsonb_build_object('start_dat', y.start_dat, 'j', y.j) as year 
		from agg_year y
		where y.poste_id_id = p.id
		order by y.start_dat desc
		limit 1
	),(	select jsonb_build_object('start_dat', a.start_dat, 'j', a.j) as all 
		from agg_all a
		where a.poste_id_id = p.id
		order by a.start_dat desc
		limit 1
	)
	from poste p
	where p.id = 2
) t;
