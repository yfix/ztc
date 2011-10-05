#!/usr/bin/env python
""" ztc.pgsql.queries - python module for ZTC.
Stores postgresql query contsrants

Copyright (c) check_postgres.pl authors
Copyright (c) 2010 Murano Software [http://muranosoft.com/]
Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

AUTOVAC_FREEZE = """SELECT
    freez,
    txns,
    ROUND(100*(txns/freez::float)) AS perc,
    datname
FROM
    (
        SELECT
            foo.freez::int,
            age(datfrozenxid) AS txns,
            datname
        FROM
            pg_database d
        JOIN
            (SELECT setting AS freez FROM pg_settings WHERE name = 'autovacuum_freeze_max_age') AS foo
            ON (true)
            WHERE d.datallowconn
    ) AS foo2
ORDER BY 3 DESC, 4 ASC"""

BLOAT = """SELECT
  schemaname,
  tablename,
  iname,
  reltuples::bigint,
  relpages::bigint,
  otta,
  ROUND(CASE WHEN otta=0 THEN 0.0 ELSE sml.relpages/otta::numeric END,1) AS tbloat,
  CASE WHEN relpages < otta THEN 0 ELSE relpages::bigint - otta END AS wastedpages,
  CASE WHEN relpages < otta THEN 0 ELSE bs*(sml.relpages-otta)::bigint END AS wastedbytes,
  CASE WHEN relpages < otta THEN '0 bytes'::text ELSE (bs*(relpages-otta))::bigint || ' bytes' END AS wastedsize,
  ituples::bigint, ipages::bigint, iotta
FROM (
  SELECT
    schemaname, tablename, cc.reltuples, cc.relpages, bs,
    CEIL((cc.reltuples*((datahdr+ma-
      (CASE WHEN datahdr%ma=0 THEN ma ELSE datahdr%ma END))+nullhdr2+4))/(bs-20::float)) AS otta,
    COALESCE(c2.relname,'?') AS iname, COALESCE(c2.reltuples,0) AS ituples, COALESCE(c2.relpages,0) AS ipages,
    COALESCE(CEIL((c2.reltuples*(datahdr-12))/(bs-20::float)),0) AS iotta -- very rough approximation, assumes all cols
  FROM (
    SELECT
      ma,bs,schemaname,tablename,
      (datawidth+(hdr+ma-(case when hdr%ma=0 THEN ma ELSE hdr%ma END)))::numeric AS datahdr,
      (maxfracsum*(nullhdr+ma-(case when nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2
    FROM (
      SELECT
        schemaname, tablename, hdr, ma, bs,
        SUM((1-null_frac)*avg_width) AS datawidth,
        MAX(null_frac) AS maxfracsum,
        hdr+(
          SELECT 1+count(*)/8
          FROM pg_stats s2
          WHERE null_frac<>0 AND s2.schemaname = s.schemaname AND s2.tablename = s.tablename
        ) AS nullhdr
      FROM pg_stats s, (
        SELECT
          (SELECT current_setting('block_size')::numeric) AS bs,
          CASE WHEN substring(v,12,3) IN ('8.0','8.1','8.2') THEN 27 ELSE 23 END AS hdr,
          CASE WHEN v ~ 'mingw32' THEN 8 ELSE 4 END AS ma
        FROM (SELECT version() AS v) AS foo
      ) AS constants
      GROUP BY 1,2,3,4,5
    ) AS foo
  ) AS rs
  JOIN pg_class cc ON cc.relname = rs.tablename
  JOIN pg_namespace nn ON cc.relnamespace = nn.oid AND nn.nspname = rs.schemaname AND nn.nspname <> 'information_schema'
  LEFT JOIN pg_index i ON indrelid = cc.oid
  LEFT JOIN pg_class c2 ON c2.oid = i.indexrelid
) AS sml
"""

TNX_AGE_IDLE_TNX = "SELECT EXTRACT (EPOCH FROM MAX(age(NOW(), query_start))) as d FROM pg_stat_activity WHERE current_query='<IDLE> in transaction'"
TNX_AGE_RUNNING = "SELECT EXTRACT (EPOCH FROM MAX(age(NOW(), query_start))) as d FROM pg_stat_activity WHERE current_query<>'<IDLE> in transaction' AND current_query<>'<IDLE>'"

# number of connections
CONN_NUMBER = {
    'idle_tnx': """SELECT COUNT(*) FROM pg_stat_activity
        WHERE current_query = '<IDLE> in transaction'""",
    'idle': """SELECT COUNT(*) FROM pg_stat_activity
        WHERE current_query = '<IDLE>'""",
    'total': "SELECT COUNT(*) FROM pg_stat_activity",
    'running': """SELECT COUNT(*) FROM pg_stat_activity
        WHERE current_query NOT LIKE '<IDLE%'""",
    'waiting': "SELECT COUNT(*) FROM pg_stat_activity WHERE waiting<>'f'"
    }