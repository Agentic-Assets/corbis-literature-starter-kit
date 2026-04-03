---
description: Execute WRDS PostgreSQL queries
---

Run the `wrds-psql` skill to query WRDS data.

$ARGUMENTS

Connection: `psql service=wrds` (credentials in `~/.pg_service.conf` and `~/.pgpass`).

**CRSP v2 policy**: All CRSP queries use v2 tables (`crsp.dsf_v2`, `crsp.msf_v2`).

Workflow:
1. Identify which WRDS schemas/tables are needed.
2. Write the SQL query with appropriate filters and joins.
3. Test with `LIMIT 10` to verify correctness.
4. Extract data via `psql COPY ... | python` pipeline -> saves `data.parquet` + `metadata.json`.
5. Report subfolder path, row count, date range, and data quality notes.

**First call may trigger DUO 2FA** -- tell user to check their phone. Always write psql commands as a single line.
