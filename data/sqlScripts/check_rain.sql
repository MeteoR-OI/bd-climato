with rr as 
    (with r as 
        ( select meteor,
          substring(date_local::text, 1, 10) as day,
          CASE WHEN obs_id IS NULL then 1 else 2 end as obs_linked,
          sum(max) as sum
          from x_max join postes on postes.id = poste_id
          where max <> 0
            and mesure_id = 52
          group by 1, 2, 3
          order by 1,2,3
        ) select meteor, 
                 day, 
                 sum(case when obs_linked = 1 then sum  * 10 else 0 end) as arch_day, 
                 sum(case when obs_linked = 2 then sum else 0 end) as arch
                 from r
                 group by 1,2
    )   select meteor,
             day,
             round(arch::numeric, 2) as arch, 
             round(arch_day::numeric,2) as arch_day, 
             round(((arch_day - arch) *100 / arch_day)::numeric,2) as percent
        from rr
        where arch_day <> 0 and arch<>0
;


 select meteor,
          substring(date_local::text, 1, 10) as day,
          sum(value) as sum
          from obs join postes on postes.id = poste_id
          where value <> 0
            and mesure_id = 52
          group by 1,2
          order by 1,2

 meteor |    day     |        sum
--------+------------+--------------------
 MTG320 | 2019-08-09 |            0.09525
 MTG320 | 2019-08-11 |            0.03175
 MTG320 | 2019-08-12 |            0.09525
 MTG320 | 2019-08-21 |            0.03175
 MTG320 | 2019-08-29 |             0.0635
 MTG320 | 2019-08-31 |              0.635
 MTG320 | 2019-09-03 |            0.09525
 MTG320 | 2019-09-06 |             0.0635
 MTG320 | 2019-09-11 |            0.47625
 MTG320 | 2019-09-12 |             0.0635
 MTG320 | 2019-09-13 | 0.7619999999999998
 MTG320 | 2019-09-14 | 0.4127499999999999
 MTG320 | 2019-09-17 |            0.53975
 MTG320 | 2019-09-23 |              0.127
 MTG320 | 2019-09-24 |            0.03175
 MTG320 | 2019-10-04 |            0.28575
 MTG320 | 2019-10-05 | 2.3177500000000006
 MTG320 | 2019-10-07 |             0.0635
 MTG320 | 2019-10-12 | 1.2382499999999999
 MTG320 | 2019-10-13 |            0.22225
 MTG320 | 2019-10-15 |            0.15875
 MTG320 | 2019-10-16 |              0.127

 MTG320 | 2019-10-21 |            0.53975

 MTG320 | 2019-10-22 | 1.1112499999999994

 MTG320 | 2019-10-23 | 1.1747499999999997

 MTG320 | 2019-10-28 |              0.254
 MTG320 | 2019-10-29 |            0.03175
 MTG320 | 2019-11-02 |              2.286
 MTG320 | 2019-11-05 |            0.03175
 MTG320 | 2019-11-08 |              0.127
 MTG320 | 2019-11-12 | 0.7302499999999996
 MTG320 | 2019-11-14 |              0.127
 MTG320 | 2019-11-15 |            0.15875
 MTG320 | 2019-11-16 |            0.15875
 MTG320 | 2019-11-17 |             0.1905
 MTG320 | 2019-11-18 |            0.03175
 MTG320 | 2019-11-21 |             0.0635
 MTG320 | 2019-11-23 | 1.4922499999999999
 MTG320 | 2019-11-24 |            0.28575
 MTG320 | 2019-11-29 |              0.254
 MTG320 | 2019-11-30 |            0.03175
 MTG320 | 2019-12-11 |            0.03175
 MTG320 | 2019-12-12 |            0.66675
 MTG320 | 2019-12-15 |            0.03175
 MTG320 | 2019-12-17 | 0.7302500000000001
 MTG320 | 2019-12-19 | 1.3652499999999999
-- buggy mariadb...
with rr as (
    select  substring(cast(from_unixtime(dateTime+4*3600) as varchar(40)),1,10) as datetime, sum(rain) as max_arch,   0 as max_march_day, from_unixtime(dateTime) as maxtime from MTG320.archive group by 1 having sum(rain) <> 0
        union all
     select  substring(cast(from_unixtime(dateTime+4*3600) as varchar(40)),1,10) as datetime,         0 as max_arch, max as max_arch_day, from_unixtime(maxtime) as maxtime from MTG320.archive_day_rain where max <> 0)
select * from rr order by 1;
rr.datetime, sum(rr.max_arch) as max_arch, sum(rr.max_arch_day) as max_arch_day from rr group by 1;
+------------+--------------------+----------------------+---------------------+
| datetime   | max_arch           | max_march_day        | maxtime             |
+------------+--------------------+----------------------+---------------------+
| 2019-10-12 | 1.2382499999999999 |                    0 | 2019-10-11 20:00:00 |
| 2019-10-12 |                  0 |  0.20000000005000002 | 2019-10-12 11:55:00 |

| 2019-10-13 |                  0 |     0.07500000001875 | 2019-10-13 02:00:00 |
| 2019-10-13 |            0.22225 |                    0 | 2019-10-12 20:00:00 |

| 2019-10-15 |            0.15875 |                    0 | 2019-10-14 20:00:00 |
| 2019-10-15 |                  0 | 0.025000000006250373 | 2019-10-15 09:54:22 |

| 2019-10-16 |              0.127 |                    0 | 2019-10-15 20:00:00 |
| 2019-10-16 |                  0 |  0.10000000002500001 | 2019-10-16 04:30:00 |

| 2019-10-21 |            0.03175 |                    0 | 2019-10-20 20:00:00 |
| 2019-10-21 |                  0 | 0.025000000006250002 | 2019-10-21 17:30:00 |

| 2019-10-22 |                  0 |     0.17500000004375 | 2019-10-22 00:00:00 |
| 2019-10-22 | 1.6192499999999992 |                    0 | 2019-10-21 20:00:00 |

| 2019-10-23 | 1.1747499999999997 |                    0 | 2019-10-22 20:00:00 |
| 2019-10-23 |                  0 |  0.20000000005000002 | 2019-10-23 13:50:00 |

| 2019-10-28 |              0.254 |                    0 | 2019-10-27 20:00:00 |
+------------+--------------------+----------------------+---------------------+


MTG320  | 2019-09-24 |  0.03 |     0.25 |   87.30
 MTG320  | 2019-10-04 |  0.29 |     0.75 |   61.90
 MTG320  | 2019-10-05 |  2.32 |     5.25 |   55.85
 MTG320  | 2019-10-07 |  0.06 |     0.25 |   74.60
 MTG320  | 2019-10-12 |  1.24 |     2.00 |   38.09
 MTG320  | 2019-10-13 |  0.22 |     0.75 |   70.37
 MTG320  | 2019-10-15 |  0.16 |     0.25 |   36.50
 MTG320  | 2019-10-16 |  0.13 |     1.00 |   87.30

 MTG320  | 2019-10-21 |  0.54 |     0.25 | -115.90

 MTG320  | 2019-10-22 |  1.11 |     1.75 |   36.50

 MTG320  | 2019-10-23 |  1.17 |     2.00 |   41.26

 MTG320  | 2019-10-28 |  0.25 |     0.75 |   66.13
 MTG320  | 2019-10-29 |  0.03 |     0.25 |   87.30
 MTG320  | 2019-11-02 |  2.29 |     2.00 |  -14.30
 MTG320  | 2019-11-05 |  0.03 |     0.25 |   87.30
 MTG320  | 2019-11-08 |  0.13 |     0.25 |   49.20
 MTG320  | 2019-11-12 |  0.73 |     1.50 |   51.32
 MTG320  | 2019-11-14 |  0.13 |     0.25 |   49.20
 MTG320  | 2019-11-15 |  0.16 |     0.25 |   36.50
 MTG320  | 2019-11-16 |  0.16 |     1.00 |   84.13
 MTG320  | 2019-11-17 |  0.19 |     0.25 |   23.80
 MTG320  | 2019-11-18 |  0.03 |     0.25 |   87.30
 MTG320  | 2019-11-23 |  1.49 |     3.00 |   50.26
 MTG320  | 2019-11-24 |  0.29 |     1.00 |   71.43
 MTG320  | 2019-11-29 |  0.25 |     1.00 |   74.60
 MTG320  | 2019-11-30 |  0.03 |     0.50 |   93.65
 MTG320  | 2019-12-11 |  0.03 |     0.25 |   87.30
 MTG320  | 2019-12-12 |  0.67 |     1.00 |   33.33
 MTG320  | 2019-12-15 |  0.03 |     0.25 |   87.30
 MTG320  | 2019-12-19 |  1.37 |     2.50 |   45.39
 MTG320  | 2019-12-23 |  4.19 |     4.25 |    1.39
 MTG320  | 2019-12-25 |  0.73 |     0.75 |    2.63
 MTG320  | 2019-12-26 |  2.79 |     4.00 |   30.15
 MTG320  | 2019-12-27 |  0.67 |     1.25 |   46.66
 MTG320  | 2019-12-28 |  0.03 |     0.25 |   87.30
 MTG320  | 2019-12-30 |  0.10 |     0.50 |   80.95
 MTG320  | 2019-12-31 |  0.03 |     0.50 |   93.65
 MTG320  | 2020-01-03 |  2.89 |     1.50 |  -92.62
 MTG320  | 2020-01-04 |  1.78 |     0.75 | -137.07
 MTG320  | 2020-01-05 |  0.89 |     0.75 |  -18.53
 MTG320  | 2020-01-06 |  0.19 |     0.25 |   23.80
 MTG320  | 2020-01-07 |  0.19 |     0.50 |   61.90
 MTG320  | 2020-01-08 |  0.10 |     0.50 |   80.95
 MTG320  | 2020-01-09 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-01-10 |  0.25 |     0.75 |   66.13
 MTG320  | 2020-01-11 |  0.98 |     2.00 |   50.79
 MTG320  | 2020-01-17 |  0.10 |     0.25 |   61.90
 MTG320  | 2020-01-18 |  0.13 |     1.00 |   87.30
 MTG320  | 2020-01-19 |  1.27 |     1.50 |   15.33
 MTG320  | 2020-01-20 |  1.78 |     0.75 | -137.07
 MTG320  | 2020-01-21 |  4.89 |     5.00 |    2.21
 MTG320  | 2020-01-22 |  0.29 |     0.75 |   61.90
 MTG320  | 2020-01-24 |  1.52 |     2.50 |   39.04
 MTG320  | 2020-01-25 |  0.16 |     0.50 |   68.25
 MTG320  | 2020-01-28 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-01-29 |  0.10 |     0.50 |   80.95
 MTG320  | 2020-01-30 |  0.19 |     0.25 |   23.80
 MTG320  | 2020-01-31 |  0.03 |     0.50 |   93.65
 MTG320  | 2020-02-02 |  0.35 |     0.75 |   53.43
 MTG320  | 2020-02-03 |  1.27 |     4.75 |   73.26
 MTG320  | 2020-02-06 |  0.06 |     0.25 |   74.60
 MTG320  | 2020-02-09 |  0.10 |     0.25 |   61.90
 MTG320  | 2020-02-12 |  0.16 |     1.50 |   89.42
 MTG320  | 2020-02-15 |  3.27 |     4.50 |   27.33
 MTG320  | 2020-02-18 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-02-19 |  0.06 |     0.25 |   74.60
 MTG320  | 2020-02-25 |  0.35 |     0.25 |  -39.70
 MTG320  | 2020-02-26 |  4.19 |     3.50 |  -19.74
 MTG320  | 2020-02-29 |  0.95 |     4.50 |   78.83
 MTG320  | 2020-03-01 |  0.06 |     0.50 |   87.30
 MTG320  | 2020-03-02 |  0.38 |     1.25 |   69.52
 MTG320  | 2020-03-06 |  1.37 |     3.25 |   57.99
 MTG320  | 2020-03-07 |  0.16 |     0.25 |   36.50
 MTG320  | 2020-03-08 |  0.10 |     0.25 |   61.90
 MTG320  | 2020-03-09 |  0.60 |     0.50 |  -20.65
 MTG320  | 2020-03-10 |  0.16 |     0.75 |   78.83
 MTG320  | 2020-03-11 |  1.17 |     3.00 |   60.84
 MTG320  | 2020-03-14 |  0.06 |     0.25 |   74.60
 MTG320  | 2020-03-23 |  0.48 |     1.00 |   52.38
 MTG320  | 2020-03-24 |  1.59 |     1.75 |    9.29
 MTG320  | 2020-03-26 |  0.06 |     0.50 |   87.30
 MTG320  | 2020-03-29 |  0.83 |     2.00 |   58.73
 MTG320  | 2020-03-30 |  2.48 |     1.75 |  -41.51
 MTG320  | 2020-03-31 |  0.48 |     3.00 |   84.13
 MTG320  | 2020-04-04 |  0.89 |     3.00 |   70.37
 MTG320  | 2020-04-11 |  0.60 |     2.25 |   73.19
 MTG320  | 2020-04-12 |  0.79 |     0.75 |   -5.83
 MTG320  | 2020-04-13 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-04-17 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-04-21 |  0.22 |     0.25 |   11.10
 MTG320  | 2020-04-23 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-04-24 |  0.06 |     0.25 |   74.60
 MTG320  | 2020-05-03 |  0.06 |     0.25 |   74.60
 MTG320  | 2020-05-16 |  0.19 |     0.75 |   74.60
 MTG320  | 2020-05-22 |  0.19 |     0.75 |   74.60
 MTG320  | 2020-05-23 |  0.19 |     0.75 |   74.60
 MTG320  | 2020-05-24 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-05-25 |  0.35 |     0.25 |  -39.70
 MTG320  | 2020-05-26 |  2.38 |     2.50 |    4.75
 MTG320  | 2020-05-31 |  0.06 |     0.50 |   87.30
 MTG320  | 2020-06-13 |  0.60 |     2.00 |   69.84
 MTG320  | 2020-06-14 |  0.06 |     0.25 |   74.60
 MTG320  | 2020-06-15 |  0.03 |     0.25 |   87.30
 MTG320  | 2020-06-25 |  0.30 |     0.75 |   60.00
 MTG320  | 2020-06-26 |  0.08 |     0.50 |   85.00
 MTG320  | 2020-07-11 |  0.13 |     0.50 |   75.00
 MTG320  | 2020-07-13 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-07-14 |  0.03 |     0.25 |   90.00
 MTG320  | 2020-07-28 |  0.10 |     0.25 |   60.00
 MTG320  | 2020-08-14 |  0.63 |     1.25 |   50.00
 MTG320  | 2020-08-20 |  0.20 |     0.25 |   20.00
 MTG320  | 2020-08-25 |  0.13 |     0.25 |   50.00
 MTG320  | 2020-08-28 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-08-29 |  0.08 |     0.25 |   70.00
 MTG320  | 2020-08-30 |  0.03 |     0.25 |   90.00
 MTG320  | 2020-08-31 |  0.08 |     0.50 |   85.00
 MTG320  | 2020-09-01 |  1.20 |     3.00 |   60.00
 MTG320  | 2020-09-07 |  0.53 |     0.50 |   -5.00
 MTG320  | 2020-09-11 |  0.03 |     0.25 |   90.00
 MTG320  | 2020-09-13 |  0.23 |     0.50 |   55.00
 MTG320  | 2020-09-25 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-09-27 |  0.28 |     0.50 |   45.00
 MTG320  | 2020-10-04 |  0.48 |     0.25 |  -90.00
 MTG320  | 2020-10-05 |  1.00 |     0.50 | -100.00
 MTG320  | 2020-10-06 |  0.45 |     0.25 |  -80.00
 MTG320  | 2020-10-08 |  0.08 |     0.25 |   70.00
 MTG320  | 2020-10-15 |  0.20 |     1.00 |   80.00
 MTG320  | 2020-10-17 |  0.78 |     0.50 |  -55.00
 MTG320  | 2020-10-18 |  0.03 |     0.25 |   90.00
 MTG320  | 2020-10-26 |  0.48 |     0.25 |  -90.00
 MTG320  | 2020-10-27 |  0.23 |     1.25 |   82.00
 MTG320  | 2020-10-28 |  0.13 |     0.50 |   75.00
 MTG320  | 2020-11-12 |  0.03 |     0.25 |   90.00
 MTG320  | 2020-11-14 |  0.15 |     0.50 |   70.00
 MTG320  | 2020-11-22 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-11-26 |  0.08 |     0.25 |   70.00
 MTG320  | 2020-11-28 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-12-02 |  0.03 |     1.25 |   98.00
 MTG320  | 2020-12-03 |  0.30 |     0.50 |   40.00
 MTG320  | 2020-12-05 |  0.15 |     0.50 |   70.00
 MTG320  | 2020-12-07 |  0.03 |     0.25 |   90.00
 MTG320  | 2020-12-08 |  0.70 |     1.50 |   53.33
 MTG320  | 2020-12-09 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-12-13 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-12-15 |  1.60 |     1.25 |  -28.00
 MTG320  | 2020-12-17 |  0.30 |     0.50 |   40.00
 MTG320  | 2020-12-18 |  0.38 |     0.75 |   50.00
 MTG320  | 2020-12-20 |  0.75 |     1.50 |   50.00
 MTG320  | 2020-12-21 |  0.30 |     1.50 |   80.00
 MTG320  | 2020-12-23 |  0.03 |     0.25 |   90.00
 MTG320  | 2020-12-26 |  0.05 |     0.25 |   80.00
 MTG320  | 2020-12-27 |  0.45 |     0.75 |   40.00
 MTG320  | 2020-12-28 |  0.60 |     0.50 |  -20.00
 MTG320  | 2020-12-31 |  0.05 |     0.50 |   90.00
 MTG320  | 2021-01-01 |  0.45 |     1.00 |   55.00
 MTG320  | 2021-01-04 |  0.30 |     0.50 |   40.00
 MTG320  | 2021-01-05 |  0.23 |     0.50 |   55.00
 MTG320  | 2021-01-07 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-01-11 |  0.88 |     1.50 |   41.67
 MTG320  | 2021-01-12 |  3.88 |     2.25 |  -72.22
 MTG320  | 2021-01-13 |  0.93 |     2.00 |   53.75
 MTG320  | 2021-01-14 |  0.58 |     1.00 |   42.50
 MTG320  | 2021-01-18 |  0.08 |     0.50 |   85.00
 MTG320  | 2021-01-20 |  0.15 |     0.25 |   40.00
 MTG320  | 2021-01-21 |  4.00 |     5.25 |   23.81
 MTG320  | 2021-01-22 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-01-23 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-01-24 |  4.75 |    10.25 |   53.66
 MTG320  | 2021-01-25 |  3.10 |     5.25 |   40.95
 MTG320  | 2021-01-26 |  0.75 |     1.50 |   50.00
 MTG320  | 2021-01-27 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-01-28 |  0.25 |     0.75 |   66.67
 MTG320  | 2021-01-30 |  0.35 |     1.00 |   65.00
 MTG320  | 2021-02-02 |  0.18 |     0.50 |   65.00
 MTG320  | 2021-02-05 |  0.05 |     0.75 |   93.33
 MTG320  | 2021-02-06 |  1.10 |     2.75 |   60.00
 MTG320  | 2021-02-08 |  0.05 |     0.50 |   90.00
 MTG320  | 2021-02-11 |  0.93 |     1.50 |   38.33
 MTG320  | 2021-02-16 |  1.15 |     1.75 |   34.29
 MTG320  | 2021-02-17 |  0.30 |     0.50 |   40.00
 MTG320  | 2021-02-18 |  0.93 |     4.50 |   79.44
 MTG320  | 2021-02-19 |  1.10 |     1.50 |   26.67
 MTG320  | 2021-02-20 |  3.63 |     2.00 |  -81.25
 MTG320  | 2021-02-21 |  0.28 |     1.75 |   84.29
 MTG320  | 2021-02-26 |  0.05 |     0.25 |   80.00
 MTG320  | 2021-02-28 |  0.03 |     0.50 |   95.00
 MTG320  | 2021-03-03 |  1.63 |     4.50 |   63.89
 MTG320  | 2021-03-04 |  0.20 |     0.25 |   20.00
 MTG320  | 2021-03-05 |  2.08 |     4.00 |   48.13
 MTG320  | 2021-03-06 |  1.85 |     2.50 |   26.00
 MTG320  | 2021-03-07 |  5.38 |     9.00 |   40.28
 MTG320  | 2021-03-10 |  0.90 |     1.00 |   10.00
 MTG320  | 2021-03-15 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-03-16 |  0.40 |     1.25 |   68.00
 MTG320  | 2021-03-17 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-03-18 |  0.53 |     2.25 |   76.67
 MTG320  | 2021-03-20 |  0.05 |     0.25 |   80.00
 MTG320  | 2021-03-21 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-03-23 |  0.03 |     1.75 |   98.57
 MTG320  | 2021-03-25 |  4.53 |     7.50 |   39.67
 MTG320  | 2021-03-27 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-03-29 |  0.35 |     1.00 |   65.00
 MTG320  | 2021-04-05 |  0.95 |     5.75 |   83.48
 MTG320  | 2021-04-08 |  0.03 |     1.25 |   98.00
 MTG320  | 2021-04-09 |  0.35 |     0.50 |   30.00
 MTG320  | 2021-04-10 |  0.20 |     1.00 |   80.00
 MTG320  | 2021-04-11 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-04-12 |  0.28 |     0.75 |   63.33
 MTG320  | 2021-04-15 |  0.40 |     0.25 |  -60.00
 MTG320  | 2021-04-16 |  2.13 |     3.50 |   39.29
 MTG320  | 2021-04-17 |  4.80 |     9.25 |   48.11
 MTG320  | 2021-04-20 |  3.75 |     7.75 |   51.61
 MTG320  | 2021-04-23 |  0.26 |     0.25 |   -4.00
 MTG320  | 2021-04-24 |  0.38 |     0.25 |  -50.00
 MTG320  | 2021-04-25 |  0.05 |     0.76 |   93.33
 MTG320  | 2021-04-26 |  0.15 |     0.51 |   70.00
 MTG320  | 2021-04-27 |  1.42 |     1.52 |    6.67
 MTG320  | 2021-04-28 |  2.97 |     2.79 |   -6.36
 MTG320  | 2021-04-29 |  0.99 |     1.78 |   44.29
 MTG320  | 2021-04-30 |  6.76 |    20.83 |   67.56
 MTG320  | 2021-05-06 |  0.64 |     1.02 |   37.50
 MTG320  | 2021-05-08 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-05-09 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-05-16 |  0.05 |     0.25 |   80.00
 MTG320  | 2021-05-26 |  0.25 |     1.27 |   80.00
 MTG320  | 2021-05-31 |  0.84 |     5.08 |   83.50
 MTG320  | 2021-06-04 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-06-05 |  2.51 |     2.03 |  -23.75
 MTG320  | 2021-06-06 |  3.99 |     5.84 |   31.74
 MTG320  | 2021-06-11 |  0.05 |     0.25 |   80.00
 MTG320  | 2021-06-12 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-06-15 |  0.36 |     0.51 |   30.00
 MTG320  | 2021-06-16 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-06-17 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-06-23 |  0.13 |     0.25 |   50.00
 MTG320  | 2021-06-28 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-06-30 |  0.03 |     0.51 |   95.00
 MTG320  | 2021-07-01 |  0.03 |     0.51 |   95.00
 MTG320  | 2021-07-08 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-07-10 |  0.38 |     0.51 |   25.00
 MTG320  | 2021-07-11 |  0.03 |     0.51 |   95.00
 MTG320  | 2021-07-14 |  1.27 |     2.29 |   44.44
 MTG320  | 2021-07-15 |  0.10 |     0.51 |   80.00
 MTG320  | 2021-07-16 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-07-17 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-07-18 |  1.85 |     1.78 |   -4.29
 MTG320  | 2021-07-21 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-07-27 |  0.36 |     0.25 |  -40.00
 MTG320  | 2021-07-28 |  0.51 |     0.51 |    0.00
 MTG320  | 2021-07-29 |  0.10 |     0.25 |   60.00
 MTG320  | 2021-07-30 |  0.13 |     0.25 |   50.00
 MTG320  | 2021-08-14 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-08-25 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-08-28 |  1.52 |     1.52 |    0.00
 MTG320  | 2021-08-29 |  0.08 |     0.51 |   85.00
 MTG320  | 2021-08-31 |  0.08 |     0.51 |   85.00
 MTG320  | 2021-09-01 |  0.03 |     0.51 |   95.00
 MTG320  | 2021-09-13 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-09-15 |  0.20 |     0.51 |   60.00
 MTG320  | 2021-09-17 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-09-18 |  0.05 |     0.25 |   80.00
 MTG320  | 2021-09-23 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-09-27 |  0.15 |     0.51 |   70.00
 MTG320  | 2021-10-03 |  0.23 |     0.51 |   55.00
 MTG320  | 2021-10-04 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-10-05 |  0.94 |     1.52 |   38.33
 MTG320  | 2021-10-07 |  0.58 |     0.25 | -130.00
 MTG320  | 2021-10-08 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-10-09 |  0.33 |     1.27 |   74.00
 MTG320  | 2021-10-10 |  0.03 |     0.76 |   96.67
 MTG320  | 2021-10-11 |  1.88 |     1.02 |  -85.00
 MTG320  | 2021-10-12 |  2.21 |     2.03 |   -8.75
 MTG320  | 2021-10-15 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-10-22 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-10-28 |  1.42 |     1.78 |   20.00
 MTG320  | 2021-10-29 |  1.22 |     4.83 |   74.74
 MTG320  | 2021-11-02 |  0.10 |     0.25 |   60.00
 MTG320  | 2021-11-27 |  0.10 |     0.51 |   80.00
 MTG320  | 2021-11-28 |  0.08 |     0.25 |   70.00
 MTG320  | 2021-11-29 |  0.69 |     1.27 |   46.00
 MTG320  | 2021-11-30 |  1.19 |     5.08 |   76.50
 MTG320  | 2021-12-04 |  0.10 |     0.25 |   60.00
 MTG320  | 2021-12-13 |  0.05 |     0.25 |   80.00
 MTG320  | 2021-12-14 |  0.05 |     0.25 |   80.00
 MTG320  | 2021-12-15 |  0.25 |     0.76 |   66.67
 MTG320  | 2021-12-17 |  0.38 |     0.51 |   25.00
 MTG320  | 2021-12-20 |  0.15 |     0.76 |   80.00
 MTG320  | 2021-12-22 |  3.00 |     3.56 |   15.71
 MTG320  | 2021-12-23 |  2.06 |     6.10 |   66.25
 MTG320  | 2021-12-24 |  0.10 |     0.25 |   60.00
 MTG320  | 2021-12-27 |  0.13 |     0.76 |   83.33
 MTG320  | 2021-12-28 |  0.03 |     0.25 |   90.00
 MTG320  | 2021-12-29 |  0.05 |     0.25 |   80.00
 MTG320  | 2022-01-02 |  0.05 |     0.25 |   80.00
 MTG320  | 2022-01-06 |  0.56 |     0.51 |  -10.00
 MTG320  | 2022-01-07 |  0.10 |     0.25 |   60.00
 MTG320  | 2022-01-08 |  0.25 |     1.02 |   75.00
 MTG320  | 2022-01-09 | 10.69 |    10.92 |    2.09
 MTG320  | 2022-01-10 |  5.56 |     7.11 |   21.79
 MTG320  | 2022-01-11 |  7.72 |     4.83 |  -60.00
 MTG320  | 2022-01-12 |  6.10 |     5.84 |   -4.35
 MTG320  | 2022-01-13 |  0.79 |     4.83 |   83.68
 MTG320  | 2022-01-14 |  6.88 |     5.33 |  -29.05
 MTG320  | 2022-01-15 | 10.03 |    11.94 |   15.96
 MTG320  | 2022-01-17 |  0.05 |     0.25 |   80.00
 MTG320  | 2022-01-18 |  1.96 |     5.33 |   63.33
 MTG320  | 2022-01-19 |  0.41 |     2.54 |   84.00
 MTG320  | 2022-01-20 |  0.43 |     1.27 |   66.00
 MTG320  | 2022-01-21 |  0.79 |     1.78 |   55.71
 MTG320  | 2022-01-22 |  1.55 |     4.57 |   66.11
 MTG320  | 2022-01-24 |  1.40 |     2.79 |   50.00
 MTG320  | 2022-01-29 |  0.03 |     0.25 |   90.00
 MTG320  | 2022-02-01 |  0.03 |     0.51 |   95.00
 MTG320  | 2022-02-02 |  3.20 |     1.52 | -110.00
 MTG320  | 2022-02-03 | 12.21 |     6.35 |  -92.28
 MTG320  | 2022-02-04 |  6.73 |     6.10 |  -10.42
 MTG320  | 2022-02-05 |  0.18 |    10.41 |   98.29
 MTG320  | 2022-02-06 |  0.28 |     1.02 |   72.50
 MTG320  | 2022-02-08 |  0.36 |     0.51 |   30.00
 MTG320  | 2022-02-09 |  0.25 |     0.76 |   66.67
 MTG320  | 2022-02-10 |  0.08 |     0.51 |   85.00
 MTG320  | 2022-02-13 |  0.36 |     2.54 |   86.00
 MTG320  | 2022-02-15 |  0.25 |     1.02 |   75.00
 MTG320  | 2022-02-19 |  0.43 |     0.25 |  -70.00
 MTG320  | 2022-02-20 |  1.63 |     3.81 |   57.33
 MTG320  | 2022-02-21 |  2.31 |     1.52 |  -51.67
 MTG320  | 2022-02-22 |  5.49 |    12.70 |   56.80
 MTG320  | 2022-02-23 |  0.38 |     1.02 |   62.50
 MTG320  | 2022-02-24 |  0.74 |     1.78 |   58.57
 MTG320  | 2022-02-25 |  0.05 |     0.25 |   80.00
 MTG320  | 2022-02-27 |  0.05 |     0.25 |   80.00



System check identified no issues (0 silenced).
timestamp=2024-01-26 15:24:18.748919 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="worker <class 'app.classes.workers.svcLoadCsv.SvcCsvLoader'> new instance" 
timestamp=2024-01-26 15:24:18.764964 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="svc thread started"   svc=svcLoadCsv   status=started 
timestamp=2024-01-26 15:24:19.833887 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="worker <class 'app.classes.workers.svcMigrate.SvcMigrate'> new instance" 
timestamp=2024-01-26 15:24:19.850555 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="svc thread started"   svc=svcMigrate   status=started 
timestamp=2024-01-26 15:24:20.860883 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="Stop command received"   svc=svcMigrate   status=stopped 
January 26, 2024 - 15:24:20
Django version 4.2.6, using settings 'Clim_MeteoR.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

timestamp=2024-01-26 15:24:23.161782 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="svc thread started"   svc=svcMigrate   status=started 
timestamp=2024-01-26 15:24:24.171235 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="New work item added in queue"   svc=migrate   meteor=BBF015   work_item={'meteor': 'BBF015', 'info': 'BBF015', 'bd': 'BBF015', 'spanID': 'Start BBF015 migration'} 
[26/Jan/2024 15:24:24] "POST /app/svc HTTP/1.1" 200 49
timestamp=2024-01-26 15:24:24.175622 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="--- New Span: Start BBF015 migration, parent: None" traceID=3039 spanID=8aa52 
timestamp=2024-01-26 15:24:24.176622 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="job = django" traceID=3039 spanID=8aa52 
timestamp=2024-01-26 15:24:24.177559 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="info = BBF015" traceID=3039 spanID=8aa52 
timestamp=2024-01-26 15:24:24.178469 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="meteor = BBF015" traceID=3039 spanID=8aa52 
timestamp=2024-01-26 15:24:24.247240 level=INFO pyFile=myTools.py pyLine=192 pyFunc=LogMe msg="ts_archive (ts utc)    from: 1438372621 to 1441051200" traceID=3039 spanID=8aa52   svc=migrate   meteor=BBF015 

-------------------------------------------------
Meteor: BBF015
Archive (dt utc)       from: 2015-06-25 00:07:00 to 2015-07-01 00:00:00
ts_archive (ts utc)    from: 1435176420 to 1435694400
-------------------------------------------------
'select dateTime, usUnits, `interval`, barometer, dewpoint, ET, extraTemp1, extraTemp2, extraTemp3, extraHumid1, extraHumid2, windGust, windGustDir, hailRate, hail, heatindex, heatingTemp, inHumidity, outHumidity, leafTemp1, leafTemp2, leafWet1, leafWet2, pressure, radiation, rainRate, rain, rxCheckPercent, soilMoist1, soilMoist2, soilMoist3, soilMoist4, soilTemp1, soilTemp2, soilTemp3, soilTemp4, inTemp, outTemp, UV, consBatteryVoltage, windSpeed, windSpeed, windSpeed, windDir, windchill from archive
    where dateTime >= 1435176420
      and dateTime < 1435694400
    order by dateTime'

    -- delete from x_max where poste_id = 2; delete from x_min where poste_id = 2; delete from obs where poste_id = 2; update postes set last_obs_date_local = null, last_obs_id = null where id = 2;
    