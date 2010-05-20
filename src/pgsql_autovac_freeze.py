#!/usr/bin/env python
"""
ZTC PostgreSQL autovacuum freeze item script.

Copyright (c) 2009-2010 Vladimir Rusinov <vladimir@greenmice.info>

License: GPL v3

Checks how close each database is to the Postgres autovacuum_freeze_max_age setting.
This action will only work for databases version 8.2 or higher. The --warning and
--critical options should be expressed as percentages. The 'age' of the transactions
in each database is compared to the autovacuum_freeze_max_age setting (200 million by
default) to generate a rounded percentage.

From PostgreSQL 8.3 docs:
autovacuum_freeze_max_age (integer)

   Specifies the maximum age (in transactions) that a table's pg_class.relfrozenxid field can
attain before a VACUUM operation is forced to prevent transaction ID wraparound within the table.
Note that the system will launch autovacuum processes to prevent wraparound even when
autovacuum is otherwise disabled. The default is 200 million transactions. This
parameter can only be set at server start, but the setting can be reduced
for individual tables by changing storage parameters. For more information see Section 23.1.4. 

Output: float, %

Rewrite of check_postgres.pl function (originaly written on perl)
http://www.bucardo.org/check_postgres/
Copyright (c) Greg Sabino Mullane <greg@endpoint.com>
Copyright (c) Vladimir Rusinov <vladimir@greenmice.info>

License: GNU GPL v.3

TODO:
* support for output of db name (when running manually by DBA)
"""

import ztc.pgsql
import ztc

q = """
SELECT
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
ORDER BY 3 DESC, 4 ASC
"""

p = ztc.pgsql.PgDB()

max_percent = 0
ret = p.query(q)
if not ret:
	# some kind of error
	ztc.notsupported()
for (freeze, age, percent, dbname) in ret:
	max_percent = max(max_percent, percent)

print max_percent