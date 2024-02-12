Install timescaledb on mac with postgres appl:
=============================================
(install timescaledb 2.13.0 with postgres 15)
=============================================
brew tap timescale/tap
brew install timescaledb

timescaledb-tune --yes --conf-path=/Users/nico/Library/Application\ Support/Postgres/var-15/postgresql.conf

/usr/bin/install -c -m 755 /opt/homebrew/Cellar/timescaledb/2.13.0/lib/timescaledb/postgresql/timescaledb-2.13.0.so  /Applications/Postgres.app/Contents/Versions/15/lib/postgresql/
/usr/bin/install -c -m 755 /opt/homebrew/Cellar/timescaledb/2.13.0/lib/timescaledb/postgresql/timescaledb-tsl-2.13.0.so  /Applications/Postgres.app/Contents/Versions/15/lib/postgresql/
/usr/bin/install -c -m 755 /opt/homebrew/Cellar/timescaledb/2.13.0/lib/timescaledb/postgresql/timescaledb.so  /Applications/Postgres.app/Contents/Versions/15/lib/postgresql/

/usr/bin/install -c -m 644 /opt/homebrew/Cellar/timescaledb/2.13.0/share/timescaledb/* /Applications/Postgres.app/Contents/Versions/15/share/postgresql/extension/

*/
============================================
(install timescaledb 2.14.0 with postgres 16)
=============================================
be sure the PATH points to: /Applications/Postgres.app/Contents/Versions/16/bin

git clone https://github.com/timescale/timescaledb
git checkout 2.14.0

./bootstrap

cd build && make

make install


*/

-- Display chunck-name, and date range
select  hypertable_name, chunk_name, primary_dimension, primary_dimension_type, range_start, range_end from timescaledb_information.chunks order by 1, 5;

-- Display materialized views
select hypertable_name, view_name,compression_enabled as compress, materialization_hypertable_schema, materialization_hypertable_name, view_definition, finalized from timescaledb_information.continuous_aggregates;

-- Display dimension info + chunk time_interval
select hypertable_schema, hypertable_name, dimension_number, column_name, column_type, dimension_type, time_interval from timescaledb_information.dimensions;

-- Diplay hypertables info
select * from timescaledb_information.hypertables;

-- Display info on scheduled jobs
select  job_id, application_name, schedule_interval, max_runtime, max_retries as retry, retry_period as period, proc_schema, proc_name, scheduled as sched, fixed_schedule as fixed, config,  next_start, initial_start from timescaledb_information.jobs;

-- taille des hypertables:
SELECT hypertable_name, pg_size_pretty(hypertable_size(format('%I.%I', hypertable_schema, hypertable_name)::regclass))                                                                                                                                                                                                                                              FROM timescaledb_information.hypertables;

-- taille de la BD:
SELECT pg_size_pretty(pg_database_size('climato'));

-- tailles des chunks d'une hypertable:
select chunk_name,  pg_size_pretty(table_bytes) as tables_bytes,  pg_size_pretty(index_bytes) as index_bytes,  pg_size_pretty(toast_bytes) as toast_bytes,  pg_size_pretty(total_bytes) as total_bytes FROM chunks_detailed_size('obs') ORDER BY chunk_name;
