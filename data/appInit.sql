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
1	Temp	{"out_temp": "float", "windchill": "float", "heatindex": "float", "dewpoint": "float", "soiltemp": "float"}
2	Humidite	{"humidity": "int"}
3	Pression	{"barometer": "float", "pressure": "float"}
4	Rain	{"rain": "int", "rain_rate": "float"}
5	Wind	{"win_i": "int", "wind_i_dir": "int", "wind": "int", "wind_dir": "int", "wind10": "int"}
6	Solar	{"uv_indice": "int", "etp": "int", "radiation": "float"}
7	Interieur	{"in_temp": "float", "in_humidity": "int"}
9	Divers	{"rx": "int", "voltage": "float"}
\.
-- SELECT pg_catalog.setval('public.type_data_id_seq', 6, true);
SELECT pg_catalog.setval('public.type_instrument_id_seq', 6, true);

COPY public.exclusion (id, start_x, end_x, value, poste_id_id, type_instrument_id) FROM stdin;
1	2021-02-11 11:33:13+04	2100-12-21 04:00:00+04	{"out_temp": "value", "windchill": "value", "heatindex": "value", "dewpoint": 22.5, "soiltemp": "null"}	1	1
\.
SELECT pg_catalog.setval('public.exclusion_id_seq', 4, true);

SELECT pg_catalog.setval('public.obs_id_seq', 1, true);
