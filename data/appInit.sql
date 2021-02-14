--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

COPY public.poste (id, meteor, meteofr, title, cas_gestion_extreme, agg_min_extreme, owner, email, phone, address, zip, city, country, latitude, longitude, start, "end", comment, fuseau) FROM stdin;
1	BBF015	MF	Bain Boeuf - MRU	3	H	Nicolas	nicolas@cuvillier.net	+230	CP B1	33701	BB	MRU	-20	-57	2021-02-09 10:42:18+04	2021-06-11 10:43:31+04	Hello	4
2	test	mf	test station	1	H	toto	toto@toto.com	123	earth	12345	city	country	0	0	2021-02-11 10:39:22+04	2021-02-11 10:40:13+04	comment	4
\.
SELECT pg_catalog.setval('public.poste_id_seq', 2, true);

COPY public.type_instrument (id, name, model_value) FROM stdin;
1	Temp	{"temp_out": "int"}
2	Pression	{}
3	Rain	{}
4	Wind	{}
5	Solar	{}
6	Divers	{}
\.
-- SELECT pg_catalog.setval('public.type_data_id_seq', 6, true);
SELECT pg_catalog.setval('public.type_instrument_id_seq', 6, true);

COPY public.exclusion (id, start_x, end_x, value, poste_id_id, type_instrument_id) FROM stdin;
1	2021-02-11 11:33:13+04	2100-12-21 04:00:00+04	{"temp_out": -1}	1	1
2	2021-02-11 11:41:56+04	2021-02-01 11:42:06+04	{"temp_out": "null", "actif": "none"}	1	1
3	2021-02-11 11:41:34+04	2100-12-21 04:00:00+04	{"temp_out": 123}	2	1
4	2021-02-11 11:34:24+04	2100-12-21 04:00:00+04	{"rain_sum": 0}	1	3
\.
SELECT pg_catalog.setval('public.exclusion_id_seq', 4, true);

COPY public.obs (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, poste_id_id, barometer, barometer_max, barometer_max_time, barometer_min, barometer_min_time, dewpoint, etp, heat_index, humidity, humidity_max, humidity_max_time, humidity_min, humidity_min_time, in_humidity, in_temp, radiation, out_temp, out_temp_max, out_temp_max_time, out_temp_min, out_temp_min_time, pressure, rain_rate_max, rain_rate_max_time, rain, soil_temp, soil_temp_min, soil_temp_min_time, uv_indice, wind_i_dir, wind_dir, rain_rate, wind_max_dir, wind_max_time, wind, windchill, rx, voltage, wind10, wind_i, wind_max) FROM stdin;
1	2021-02-13 16:49:55+04	2021-02-13 16:50:25.462786+04	300	0	0	f	1	1035.0	\N	\N	\N	\N	\N	0.000	\N	82	\N	\N	\N	\N	\N	\N	100	30.0	\N	\N	\N	\N	\N	\N	\N	0.0	\N	\N	\N	8	\N	80	0.0	\N	\N	5.0	\N	\N	\N	\N	\N	\N
\.
SELECT pg_catalog.setval('public.obs_id_seq', 1, true);

