SELECT  activity.pid,activity.usename,activity.query,blocking.pid AS blocking_id,
blocking.query AS blocking_query
FROM pg_stat_activity AS activity
  JOIN pg_stat_activity AS blocking
ON blocking.pid = ANY(pg_blocking_pids(activity.pid));

-- display current locks
SELECT locktype, relation::regclass, mode, transactionid AS tid, virtualtransaction AS vtid, pid, granted
   FROM pg_catalog.pg_locks l LEFT JOIN pg_catalog.pg_database db ON db.oid = l.database
   WHERE (db.datname = current_database() OR db.datname IS NULL) AND NOT pid = pg_backend_pid();

-- see active queries
SELECT query,state,wait_event,pid FROM pg_stat_activity
  WHERE datname=current_database() AND NOT (state='idle' OR pid=pg_backend_pid());

-- see blocked queries
select pid, 
       usename, 
       pg_blocking_pids(pid) as blocked_by, 
       query as blocked_query
from pg_stat_activity
where cardinality(pg_blocking_pids(pid)) > 0;

-- see blocked and blocking queries
SELECT blockeda.pid AS blocked_pid, blockeda.query as blocked_query,
  blockinga.pid AS blocking_pid, blockinga.query as blocking_query
FROM pg_catalog.pg_locks blockedl
JOIN pg_stat_activity blockeda ON blockedl.pid = blockeda.pid
JOIN pg_catalog.pg_locks blockingl ON(blockingl.transactionid=blockedl.transactionid
  AND blockedl.pid != blockingl.pid)
JOIN pg_stat_activity blockinga ON blockingl.pid = blockinga.pid
WHERE NOT blockedl.granted AND blockinga.datname=current_database();

-- ??
SELECT
  COALESCE(blockingl.relation::regclass::text,blockingl.locktype) as locked_item,
  blockeda.pid AS blocked_pid, blockeda.query as blocked_query,
  blockedl.mode as blocked_mode, blockinga.pid AS blocking_pid,
  blockinga.query as blocking_query, blockingl.mode as blocking_mode
FROM pg_catalog.pg_locks blockedl
JOIN pg_stat_activity blockeda ON blockedl.pid = blockeda.pid
JOIN pg_catalog.pg_locks blockingl ON(
  ( (blockingl.transactionid=blockedl.transactionid) OR
    (blockingl.relation=blockedl.relation AND blockingl.locktype=blockedl.locktype)
  ) AND blockedl.pid != blockingl.pid)
JOIN pg_stat_activity blockinga ON blockingl.pid = blockinga.pid
WHERE NOT blockedl.granted
AND blockinga.datname=current_database();

--  last query in the blocking station
SELECT
    activity.pid,
    activity.usename,
    activity.query,
    blocking.pid AS blocking_id,
    blocking.query AS blocking_query
FROM pg_stat_activity AS activity
JOIN pg_stat_activity AS blocking ON blocking.pid = ANY(pg_blocking_pids(activity.pid));

-- kill a query
SELECT pg_cancel_backend(a.pid), pg_terminate_backend(a.pid);

-- find recursive lock chain
;with recursive 
    find_the_source_blocker as (
        select  pid
               ,pid as blocker_id
        from pg_stat_activity pa
        where pa.state<>'idle'
              and array_length(pg_blocking_pids(pa.pid), 1) is null

        union all

        select              
                t.pid  as  pid
               ,f.blocker_id as blocker_id
        from find_the_source_blocker f 
        join (  SELECT
                    act.pid,
                    blc.pid AS blocker_id
                FROM pg_stat_activity AS act
                LEFT JOIN pg_stat_activity AS blc ON blc.pid = ANY(pg_blocking_pids(act.pid))
                where act.state<>'idle') t on f.pid=t.blocker_id
        )
    
select distinct 
       s.pid
      ,s.blocker_id
      ,pb.usename       as blocker_user
      ,pb.query_start   as blocker_start
      ,pb.query         as blocker_query
      ,pt.query_start   as trans_start
      ,pt.query         as trans_query
from find_the_source_blocker s
join pg_stat_activity pb on s.blocker_id=pb.pid
join pg_stat_activity pt on s.pid=pt.pid
where s.pid<>s.blocker_id;


