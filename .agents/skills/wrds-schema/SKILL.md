---
name: wrds-schema
description: Use this skill at the start of a session when working with WRDS data (CRSP, OptionMetrics, Compustat). It pre-loads schema knowledge -- table names, column names, join keys, data types, and common gotchas -- so you can write correct queries without exploratory round-trips. Invoke when the user mentions WRDS, OptionMetrics, CRSP, or options analysis.
argument-hint: "[databases: crsp optionm comp jkp all]"
---

# WRDS Schema Pre-loader

You are starting a session that involves WRDS PostgreSQL queries. Before writing any queries, load the schema knowledge you need.

## Examples

- `/wrds-schema crsp` -- load CRSP schema only
- `/wrds-schema crsp optionm` -- load CRSP + OptionMetrics schemas
- `/wrds-schema all` -- load all available schemas

## Connection

Connection details are in `~/.pg_service.conf`; password in `~/.pgpass`.

```bash
psql service=wrds
```

## What to do

Based on `$ARGUMENTS` (or "all" if none given), query the WRDS database to retrieve current schema details and return a concise reference.

### Schema queries to run

For each requested database, run the appropriate queries:

| Keyword | Tables to check | Key queries |
|---------|----------------|-------------|
| `crsp` | `crsp.dsf_v2`, `crsp.dsi`, `crsp.msf_v2`, `crsp.stksecurityinfohist`, `crsp.ccmxpf_lnkhist` | Column names, date ranges, PERMNO lookups. Confirm column names (`dlycaldt` not `date` in v2), index columns in `dsi` (`spindx`, `sprtrn`). |
| `optionm` | `optionm.opprcd{YYYY}` (yearly partitioned), `optionm.securd`, `optionm.zerocd` | Confirm: `strike_price` is strike*1000, column names for options tables. |
| `comp` | `comp.funda`, `comp.fundq` | Key columns, standard filters (INDL/STD/D/C), CCM linking via `crsp.ccmxpf_lnkhist` (columns, linktype LC/LU, linkprim P/C, deduplication pattern). |
| `jkp` | `contrib.global_factor` | Key columns (permno, gvkey, eom, excntry, me, ret_exc, be_me, etc.), standard filters (excntry='USA', obs_main=1, common=1, exch_main=1, primary_sec=1). 443 cols, 30M+ rows. |

### Query template for each table

```bash
psql service=wrds -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='...' AND table_name='...' ORDER BY ordinal_position;"
```

Quick validation queries (e.g., `SELECT MIN(date), MAX(date) FROM crsp.dsi LIMIT 1`)

### After retrieving schemas

Compile results into a single **Schema Reference** block and present it to the user. Keep it compact -- a lookup table, not prose. Example format:

```
=== CRSP ===
crsp.dsi: date(date), vwretd(numeric), sprtrn(numeric), spindx(numeric) | 1926-2024
crsp.dsf_v2: permno(int), dlycaldt(date), dlyret(numeric), dlyprc(numeric), dlyvol(numeric) | 1926-2024
crsp.msf_v2: permno(int), mthcaldt(date), mthret(numeric), mthprc(numeric), mthcap(numeric) | 1926-2024

=== OPTIONMETRICS ===
optionm.opprcd{YYYY}: secid, date, exdate, cp_flag, strike_price(/1000!), best_bid, best_offer, impl_volatility, delta, volume, open_interest
optionm.zerocd: date, days, rate | zero-coupon rates by maturity
optionm.securd: secid, ticker, cusip, index_flag
  Gotcha: strike_price is strike * 1000 (divide by 1000 in queries)

=== COMPUSTAT ===
comp.funda: gvkey, datadate, fyear, at, lt, seq, ceq, pstk, pstkrv, txditc, ni, ib, revt, csho, prcc_f
  REQUIRED filters: indfmt='INDL' AND datafmt='STD' AND popsrc='D' AND consol='C'
comp.fundq: gvkey, datadate, fqtr, rdq, atq, seqq, ceqq, pstkq, pstkrq, ibq, saleq, cshoq
```

## Known gotchas (always include these)

1. **Decimal type** -- psycopg2 returns `decimal.Decimal` for numeric columns. Always `.apply(float)` or `float()` before math/numpy operations.
2. **CRSP column names** -- `crsp.dsi` uses `date` (not `caldt`), `spindx` (not `sprindx`). v2 daily uses `dly` prefix; monthly uses `mth` prefix.
3. **OptionMetrics strike** -- `strike_price` column stores strike * 1000. Divide by 1000.
4. **OptionMetrics yearly tables** -- option prices are in `optionm.opprcd{YYYY}`, NOT a single table. Loop years 1996-2025.
5. **Compustat standard filters** -- every `comp.funda`/`comp.fundq` query MUST include: `indfmt='INDL' AND datafmt='STD' AND popsrc='D' AND consol='C'`.
6. **CCM link column** -- `lpermno` not `permno` in `crsp.ccmxpf_lnkhist`. Always alias.
7. **WRDS data lag** -- databases lag months behind the current date. Use historical years for smoke tests.
