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

