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


-- type_data
COPY public.type_data (id, name, model_value) FROM stdin;
1	Temp	{}
2	Pression	{}
3	Rain	{}
4	Wind	{}
5	Solar	{}
6	Divers	{}
\.
SELECT pg_catalog.setval('public.agg_day_id_seq', 1, true);


-- Poste
COPY public.poste (id, meteor, meteofr, title, cas_gestion_extreme, agg_min_extreme, owner, email, phone, address, zip, city, country, latitude, longitude, start, "end", comment) FROM stdin;
1	BBF015	MF	Bain Boeuf - MRU	3	H	Nicolas	nicolas@cuvillier.net	+230	CP B1	33701	BB	MRU	-20	-57	2021-02-09 10:42:18+04	2021-06-11 10:43:31+04	Hello
\.
SELECT pg_catalog.setval('public.poste_id_seq', 1, true);

-- obs
COPY public.obs (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
1	2021-02-09 10:48:54+04	2021-02-09 10:49:20+04	300	0	0	f	{"rain": "2.2"}	1
2	2021-02-09 10:53:00+04	2021-02-09 11:22:37.597514+04	300	0	0	f	{"rain": "3,3"}	1
\.
SELECT pg_catalog.setval('public.observation_id_seq', 2, true);

-- agg_hour
COPY public.agg_hour (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
1	2021-02-09 10:00:00+04	2021-02-09 11:49:08.821168+04	600	0	0	f	{"rain": "5.5"}	1
\.
SELECT pg_catalog.setval('public.agg_hour_id_seq', 1, true);

-- agg_day
COPY public.agg_day (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
1	2021-02-09 04:00:00+04	2021-02-09 12:12:34.394691+04	600	0	0	f	{"rain": "5.5"}	1
\.
SELECT pg_catalog.setval('public.agg_day_id_seq', 1, true);

-- agg_month
COPY public.agg_month (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
1	2021-02-01 04:00:00+04	2021-02-09 12:13:30.057132+04	600	0	0	f	{"rain": "5.5"}	1
\.
SELECT pg_catalog.setval('public.agg_month_id_seq', 1, true);

-- agg_year
COPY public.agg_year (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
1	2021-01-01 04:00:00+04	2021-02-09 12:13:52.445459+04	600	0	0	f	{"rain": "5.5"}	1
\.
SELECT pg_catalog.setval('public.agg_year_id_seq', 1, true);

-- agg_all
COPY public.agg_global (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
1	2000-01-01 04:00:00+04	2021-02-09 12:13:06.513518+04	600	0	0	f	{"rain": "5.5"}	1
\.
SELECT pg_catalog.setval('public.agg_global_id_seq', 1, true);
