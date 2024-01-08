 SELECT archive_day_windSpeed.dateTime as dt,
 	from_unixtime(archive_day_windSpeed.dateTime + 4*3600) as utc,
 	archive_day_windGust.max as gust,
 	archive_day_windSpeed.max as speed,
	archive_day_wind.max as wind,
 	archive_day_wind.max_dir as maxDir,
 	(archive_day_windSpeed.max - archive_day_wind.max)*100/archive_day_wind.max  as p_windMax,
 	(archive_day_windGust.max - archive_day_wind.max)*100/archive_day_wind.max  as gust_wind,
 	(archive_day_windGust.max - archive_day_windSpeed.max)*100/archive_day_windSpeed.max  as gust_speed

 FROM archive_day_windSpeed
 	INNER JOIN archive_day_windGust ON archive_day_windSpeed.dateTime=archive_day_windGust.dateTime
 	INNER JOIN archive_day_wind ON archive_day_windSpeed.dateTime=archive_day_wind.dateTime
 WHERE archive_day_windGust.max > 0 order by 8 desc limit 100;
select count(*), avg(min), min(min), avg(max), max(max) from archive_day_windSpeed;
select count(*), avg(min), min(min), avg(max), max(max) from archive_day_wind;
select count(*), avg(min), min(min), avg(max), max(max) from archive_day_windGust;

-- => change order by 7,8,9 et asc/desc pour mieux analyser les donnees...
