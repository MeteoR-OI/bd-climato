/********************
* Init TimeScaleDB
********************/
  CREATE EXTENSION IF NOT EXISTS timescaledb;
  ALTER TABLE obs DROP CONSTRAINT obs_pkey;
  SELECT create_hypertable('obs',  by_range('date_local',  INTERVAL '100 days'), migrate_data => true);
  SELECT set_chunk_time_interval('obs', INTERVAL '100 days');
  DROP index if exists obs_poste_id_7ed1db30;
  DROP index if exists obs_mesure_id_2198080c;

  ALTER TABLE x_min DROP CONSTRAINT x_min_pkey;
  SELECT create_hypertable('x_min', by_range('date_local',  INTERVAL '200 days'), migrate_data => true);
  SELECT set_chunk_time_interval('x_min',  INTERVAL '200 days');
  DROP index if exists x_min_mesure_id_915a2d2e;
  DROP index if exists x_min_poste_id_a7ee3864;

  ALTER TABLE x_max DROP CONSTRAINT x_max_pkey;
  SELECT create_hypertable('x_max',  by_range('date_local',  INTERVAL '200 days'), migrate_data => true);
  SELECT set_chunk_time_interval('x_max',  INTERVAL '200 days');
  DROP index if exists x_max_mesure_id_a633699c;
  DROP index if exists x_max_poste_id_529ea905;

/*
* obs_hour
*/
create materialized view obs_hour WITH (timescaledb.continuous) as
  select
        timescaledb_experimental.time_bucket_ng('1 hour', o.date_local, origin => '1950-01-01') as date_local,
        o.poste_id as poste_id,
        o.mesure_id as mesure_id,
        m.agreg_type as agreg_type,
        sum(o.duration) as duration,
        CASE
          WHEN m.agreg_type = 1 THEN avg(o.value)
          WHEN m.agreg_type = 2 THEN sum(o.value)
          WHEN m.agreg_type = 3 THEN max(o.value)
          WHEN m.agreg_type = 4 THEN min(o.value)
           END AS value
  from obs o join mesures m on m.id = mesure_id
  where qa_value != 9 and duration <= 60 and m.agreg_type != 0
  group by 1,2,3,4
  order by 1,2,3
;

ALTER MATERIALIZED VIEW obs_hour set (timescaledb.materialized_only = false);

SELECT add_continuous_aggregate_policy('obs_hour',
  start_offset => INTERVAL '60 minute',
  end_offset => NULL,
  schedule_interval => INTERVAL '30 minutes');

/*
* obs_day
*/
create materialized view obs_day WITH (timescaledb.continuous) as
  select
        timescaledb_experimental.time_bucket_ng('1 day', o.date_local, origin => '1950-01-01') as date_local,
        o.poste_id as poste_id,
        o.mesure_id as mesure_id,
        m.agreg_type as agreg_type,
        sum(o.duration) as duration,
        CASE
          WHEN m.agreg_type = 1 THEN avg(o.value)
          WHEN m.agreg_type = 2 THEN sum(o.value)
          WHEN m.agreg_type = 3 THEN max(o.value)
          WHEN m.agreg_type = 4 THEN min(o.value)
           END AS value
  from obs o join mesures m on m.id = mesure_id
  where qa_value != 9 and m.agreg_type != 0
  group by 1,2,3,4
  order by 1,2,3
;

ALTER MATERIALIZED VIEW obs_day set (timescaledb.materialized_only = false);

SELECT add_continuous_aggregate_policy('obs_day',
  start_offset => INTERVAL '60 minute',
  end_offset => NULL,
  schedule_interval => INTERVAL '30 minutes');

/*
* obs_month
*/
create materialized view obs_month WITH (timescaledb.continuous) as
  select
        timescaledb_experimental.time_bucket_ng('1 month', o.date_local, origin => '1950-01-01') as date_local,
        o.poste_id,
        o.mesure_id,
        o.agreg_type,
        sum(o.duration) as duration,
        CASE
          WHEN o.agreg_type = 1 THEN avg(o.value)
          WHEN o.agreg_type = 2 THEN sum(o.value)
          WHEN o.agreg_type = 3 THEN max(o.value)
          WHEN o.agreg_type = 4 THEN min(o.value)
           END AS value
  from obs_day o join mesures m on m.id = mesure_id
  group by 1,2,3,4
  order by 1,2,3
;

ALTER MATERIALIZED VIEW obs_month set (timescaledb.materialized_only = false);

SELECT add_continuous_aggregate_policy('obs_month',
  start_offset => INTERVAL '2 days',
  end_offset => NULL,
  schedule_interval => INTERVAL '1 day');

/*
* x_min_day
*/
create materialized view x_min_day WITH (timescaledb.continuous) as
  select
        timescaledb_experimental.time_bucket_ng('1 day', x.date_local, origin => '1950-01-01') as date_local,
        x.poste_id as poste_id,
        x.mesure_id as mesure_id,
        m.agreg_type as agreg_type,
        CASE
          WHEN m.agreg_type = 2 THEN sum(x.min)  -- on utilise la somme quotidienne pour les mesures sommables
          ELSE min(x.min)
        END AS min,
        first(x.min_time, x.min) as min_time
  from x_min x join mesures m on m.id = x.mesure_id
  where x.qa_min != 9 and m.agreg_type != 3 and m.agreg_type != 0 and m.min is true
  group by 1,2,3,4
  order by 1,2,3
;

ALTER MATERIALIZED VIEW x_min_day set (timescaledb.materialized_only = false);

SELECT add_continuous_aggregate_policy('x_min_day',
  start_offset => INTERVAL '12 hours',
  end_offset => NULL,
  schedule_interval => INTERVAL '6 hours');

/*
* x_min_month
*/
create materialized view x_min_month WITH (timescaledb.continuous) as
  select
        timescaledb_experimental.time_bucket_ng('1 month', date_local, origin => '1950-01-01') as date_local,
        poste_id as poste_id,
        mesure_id as mesure_id,
        agreg_type as agreg_type,
        min(min) AS min,    -- on prend le min des min quotidiens
        first(min_time, min) as min_time
  from x_min_day
 group by 1,2,3,4
 order by 1,2,3
;

ALTER MATERIALIZED VIEW x_min_month set (timescaledb.materialized_only = false);

SELECT add_continuous_aggregate_policy('x_min_month',
  start_offset => INTERVAL '2 days',
  end_offset => NULL,
  schedule_interval => INTERVAL '1 day');

/*
* x_max_day
*/
create materialized view x_max_day WITH (timescaledb.continuous) as
  select
        timescaledb_experimental.time_bucket_ng('1 day', x.date_local, origin => '1950-01-01') as date_local,
        x.poste_id as poste_id,
        x.mesure_id as mesure_id,
        m.agreg_type as agreg_type,
        CASE
          WHEN m.agreg_type = 2 THEN sum(x.max)   -- on utilise la somme quotidienne pour les mesures sommables
          ELSE max(x.max)
        END AS max,
        last(x.max_time, x.max) as max_time,
        last(x.max_dir, x.max) as max_dir
  from x_max x join mesures m on m.id = mesure_id
  where qa_max != 9 and m.agreg_type != 4 and m.agreg_type != 0 and m.max is true
  group by 1,2,3,4
  order by 1,2,3
;

ALTER MATERIALIZED VIEW x_max_day set (timescaledb.materialized_only = false);

SELECT add_continuous_aggregate_policy('x_max_day',
  start_offset => INTERVAL '12 hours',
  end_offset => NULL,
  schedule_interval => INTERVAL '6 hours');

/*
* x_max_month
*/
create materialized view x_max_month WITH (timescaledb.continuous) as
  select
        timescaledb_experimental.time_bucket_ng('1 month', date_local, origin => '1950-01-01') as date_local,
        poste_id as poste_id,
        mesure_id as mesure_id,
        agreg_type as agreg_type,
        max(max) AS max,      -- on prend le max des max quotidiens
        last(max_time, max) as max_time,
        last(max_dir, max) as max_dir
  from x_max_day
  group by 1,2,3,4
  order by 1,2,3
;

ALTER MATERIALIZED VIEW x_max_month set (timescaledb.materialized_only = false);

SELECT add_continuous_aggregate_policy('x_max_month',
  start_offset => INTERVAL '2 days',
  end_offset => NULL,
  schedule_interval => INTERVAL '1 day');

-- refresh all materialized views
CREATE OR REPLACE PROCEDURE refresh_all_mv(start_date timestamp = null, end_date timestamp = null)
LANGUAGE plpgsql
AS $$
BEGIN
  CALL refresh_continuous_aggregate('obs_hour', start_date, end_date);
  CALL refresh_continuous_aggregate('obs_day', start_date, end_date);
  CALL refresh_continuous_aggregate('obs_month', start_date, end_date);
  CALL refresh_continuous_aggregate('x_min_day', start_date, end_date);
  CALL refresh_continuous_aggregate('x_min_month', start_date, end_date);
  CALL refresh_continuous_aggregate('x_max_day', start_date, end_date);
  CALL refresh_continuous_aggregate('x_max_month', start_date, end_date);
END; $$;

-- create materialized view compare_month WITH (timescaledb.continuous) as
-- materialized view does not support left join...

--  select
--         timescaledb_experimental.time_bucket_ng('1 month', o.date_local, origin => '1950-01-01') as date_local,
--         o.poste_id,
--         avg(o.value) as avg_value,
--         min(mi.min),
--         first(mi.min_time, mi.min) as min_time,
--         max(ma.max),
--         last(ma.max_time, ma.max) as max_time
--     from obs_month o 
--       left join x_min_month mi on 
--         o.poste_id = mi.poste_id
--         and o.mesure_id = mi.mesure_id
--         and timescaledb_experimental.time_bucket_ng('1 month', mi.date_local, origin => '1950-01-01') = timescaledb_experimental.time_bucket_ng('1 month', mi.date_local, origin => '1950-01-01')
--       left join x_max_month ma on 
--         o.poste_id = ma.poste_id
--         and o.mesure_id = ma.mesure_id
--         and timescaledb_experimental.time_bucket_ng('1 month', ma.date_local, origin => '1950-01-01') = timescaledb_experimental.time_bucket_ng('1 month', ma.date_local, origin => '1950-01-01')
--     where o.mesure_id = 1
-- --       Important to add a where on each table => 
-- --           timescale can limit the search in the underlying chunks for each table
--       and o.date_local > '202-12-01'
--       and mi.date_local > '202-12-01'
--       and ma.date_local > '202-12-01'
--     group by 1,2;

/*
Id_station;Id_omm;Nom_usuel;Latitude;Longitude;Altitude;Date_ouverture;Pack
97401520;;LE TEVELAVE;-21.211667;55.361333;908;1953-01-01;ETENDU
97401540;;LES AVIRONS - CIRAD;-21.239500;55.327500;180;1952-01-01;ETENDU
97402240;;BELLEVUE BRAS-PANON;-21.005000;55.622667;480;1990-09-01;RADOME
97403410;;LE DIMITILE_SAPC;-21.189000;55.481500;1808;2013-09-27;ETENDU
97403435;;BRAS-LONG_SAPC;-21.228333;55.474667;510;2013-05-22;ETENDU
97404540;;PONT-MATHURIN;-21.265000;55.380000;19;1961-06-01;RADOME
97405420;;PITON-BLOC_SAPC;-21.321167;55.572333;812;1990-01-01;ETENDU
97406220;;PLAINE DES PALMISTES;-21.136167;55.627167;1032;1952-01-01;RADOME
97407520;61981;LE PORT;-20.946167;55.282000;9;1971-04-18;RADOME
97408510;;POSSESSION;-20.921333;55.346167;9;1997-10-01;ETENDU
97408560;;AURERE_SAPC;-21.018833;55.424833;940;1952-01-01;ETENDU
97408580;;LA NOUVELLE_SAPC;-21.076667;55.423333;1415;1970-01-01;ETENDU
97408582;;DOS D'ANE;-20.978500;55.390500;1027;2022-05-02;ETENDU
97409210;;BOIS-ROUGE;-20.913667;55.641333;5;1952-01-01;ETENDU
97409230;;LE COLOSSE;-20.934500;55.664500;16;1957-03-01;RADOME
97409240;;MENCIOL;-20.961167;55.625667;181;1953-01-01;ETENDU
97410202;;BEAUVALLON;-21.008000;55.693333;16;1952-01-01;ETENDU
97410238;;SAINT-BENOIT;-21.058833;55.719333;43;1952-01-01;RADOME
97410250;;TAKAMAKA - PK12_SAPC;-21.076333;55.630833;660;1971-11-01;ETENDU
97410265;;CHEMIN DE CEINTURE_SAPC;-21.076333;55.685500;255;2003-07-24;ETENDU
97411132;;CHAUDRON;-20.897000;55.495000;38;1967-01-01;ETENDU
97411141;;GRANDE-CHALOUPE;-20.898333;55.369833;10;1997-10-01;ETENDU
97411146;;COLORADO_SAPC;-20.910500;55.421500;702;2003-02-26;ETENDU
97411150;;SAINT-FRANCOIS;-20.921333;55.456333;545;1953-03-01;ETENDU
97411155;;MONTAUBAN_SAPC;-20.938667;55.496833;420;2009-09-29;ETENDU
97411164;;LE BRULE - VAL FLEURI_SAPC;-20.941667;55.429500;1069;1956-09-01;ETENDU
97411170;;PLAINE DES CHICOTS_SAPC;-20.987333;55.444833;1834;1982-01-01;ETENDU
97412302;;COMMERSON_SAPC;-21.208000;55.643667;2310;1968-01-01;ETENDU
97412336;;GRAND-COUDE_SAPC;-21.301667;55.631333;1085;1978-01-01;ETENDU
97412340;;GRAND-GALET;-21.311000;55.639500;505;1953-08-06;ETENDU
97412356;;LA CRETE_SAPC;-21.337500;55.667667;659;1968-10-01;ETENDU
97412384;;ST-JOSEPH_SAPC;-21.385167;55.609667;13;1960-04-01;ETENDU
97412801;;ST JOSEPH-CIRAD;-21.385167;55.609667;13;2021-10-05;ETENDU
97413520;;COLIMACONS;-21.130333;55.304667;798;1963-08-01;RADOME
97413542;;ST-LEU;-21.190000;55.292333;79;1950-10-01;ETENDU
97413545;;SAINT-LEU - CIRAD;-21.187333;55.300833;222;1997-01-01;ETENDU
97413550;;ETANG SAINT-LEU - CIRAD;-21.173333;55.308833;429;2002-02-01;ETENDU
97413580;;PITON SAINT-LEU_SAPC;-21.215167;55.325833;530;1973-02-01;ETENDU
97414409;;PLAINE DES MAKES_SAPC;-21.199500;55.409167;980;2004-12-29;ETENDU
97414431;;LE GOL LES HAUTS - CIRAD;-21.245833;55.428000;365;1997-01-01;ETENDU
97414451;;LE TAPAGE - CIRAD;-21.224667;55.444167;863;2002-03-25;ETENDU
97415516;;BOIS DE NEFLES ST-PAUL_SAPC;-20.997500;55.341167;595;1952-01-01;ETENDU
97415536;;PETITE-FRANCE;-21.045000;55.342000;1200;1999-09-01;RADOME
97415541;;TAN-ROUGE_SAPC;-21.069167;55.299667;750;1960-01-01;ETENDU
97415550;;L'ERMITAGE - CIRAD;-21.053000;55.241333;147;2002-05-01;ETENDU
97415557;;LE GUILLAUME;-21.064667;55.324333;1035;1953-01-01;ETENDU
97415566;;PITON-MAIDO;-21.076667;55.381167;2150;1998-11-18;RADOME
97415590;;POINTE DES TROIS-BASSINS;-21.105167;55.247667;5;1987-10-02;RADOME
97415592;;TAN ROUGE-CIRAD;-21.069167;55.299667;746;2021-06-02;ETENDU
97416410;;RAVINE DES CABRIS - CIRAD;-21.274500;55.475333;310;1997-01-01;ETENDU
97416463;;PIERREFONDS-AEROPORT;-21.320000;55.425500;21;1999-01-01;RADOME
97416465;;LIGNE-PARADIS - CIRAD;-21.319167;55.485167;156;1966-01-01;ETENDU
97417340;;LE TREMBLET;-21.317333;55.801000;91;1953-01-01;ETENDU
97417360;;LE BARIL;-21.359000;55.732167;114;1989-02-01;RADOME
97418110;61980;GILLOT-AEROPORT;-20.892167;55.528667;8;1953-01-01;RADOME
97418123;;LA MARE - CIRAD;-20.903500;55.532000;68;2001-01-01;ETENDU
97418170;;PLAINE DES FOUGERES_SAPC;-20.967333;55.527833;1064;1993-06-01;ETENDU
97419310;;RIVIERE DE L'EST - CIRAD;-21.120167;55.758667;144;1953-01-01;ETENDU
97419320;;HAUTS DE SAINTE-ROSE_SAPC;-21.159500;55.763667;820;1973-07-01;ETENDU
97419350;;GROS PITON SAINTE-ROSE;-21.179500;55.828833;181;1987-09-01;RADOME
97419380;;BELLECOMBE-JACOB;-21.217833;55.687000;2245;1966-11-01;RADOME
97420110;;GRAND-HAZIER - CIRAD;-20.902833;55.586000;69;1953-01-01;ETENDU
97420150;;BAGATELLE_SAPC;-20.931000;55.576667;262;1953-01-01;ETENDU
97420180;;BRAS-PISTOLET_SAPC;-20.969000;55.587500;556;2002-12-01;ETENDU
97421210;;MARE A VIEILLE PLACE;-21.027833;55.512167;870;1989-07-01;ETENDU
97421220;;GRAND-ILET_SAPC;-21.028667;55.471667;1185;1973-07-01;ETENDU
97421240;;SALAZIE-VILLAGE_SAPC;-21.031667;55.538500;476;1996-01-01;ETENDU
97421260;;BELOUVE_SAPC;-21.060833;55.536500;1500;1955-09-01;ETENDU
97421265;;ILET A VIDOT_SAPC;-21.063167;55.510333;940;2003-12-01;ETENDU
97422440;;PLAINE DES CAFRES;-21.209167;55.572833;1560;1948-01-01;RADOME
97422445;;BRAS-SEC;-21.205667;55.525167;1210;1969-11-15;ETENDU
97422455;;PONT D'YVES;-21.231333;55.503167;835;1977-07-19;ETENDU
97422465;;LE TAMPON - CIRAD;-21.251667;55.530333;860;1958-01-01;ETENDU
97424410;;CILAOS;-21.134167;55.471667;1197;1952-01-01;RADOME
97424450;;ILET A CORDES_SAPC;-21.153500;55.438167;1067;1977-08-08;ETENDU
97424460;;PALMISTE-ROUGE;-21.168667;55.474500;830;1962-01-01;ETENDU
*/