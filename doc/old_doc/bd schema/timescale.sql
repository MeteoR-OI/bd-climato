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
(install timescaledb 2.13.0 with postgres 16)
=============================================

Do not work yet.... ???

brew tap timescale/tap
brew install timescaledb

timescaledb-tune --yes --conf-path=/Users/nico/Library/Application\ Support/Postgres/var-16/postgresql.conf

/usr/bin/install -c -m 755 /opt/homebrew/Cellar/timescaledb/2.13.0/lib/timescaledb/postgresql/timescaledb-2.13.0.so  /Applications/Postgres.app/Contents/Versions/16/lib/postgresql/
/usr/bin/install -c -m 755 /opt/homebrew/Cellar/timescaledb/2.13.0/lib/timescaledb/postgresql/timescaledb-tsl-2.13.0.so  /Applications/Postgres.app/Contents/Versions/16/lib/postgresql/
/usr/bin/install -c -m 755 /opt/homebrew/Cellar/timescaledb/2.13.0/lib/timescaledb/postgresql/timescaledb.so  /Applications/Postgres.app/Contents/Versions/16/lib/postgresql/

/usr/bin/install -c -m 644 /opt/homebrew/Cellar/timescaledb/2.13.0/share/timescaledb/* /Applications/Postgres.app/Contents/Versions/16/share/postgresql/extension/

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

