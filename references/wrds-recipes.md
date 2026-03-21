# WRDS Recipes and Data Gotchas

Common WRDS table schemas, standard merge recipes, known data issues, and pitfalls per database. This reference prevents rediscovering the same problems. For Python code templates, see the `python-empirical-code` skill and `assets/code-examples.md`.

**Connection**: `wrds.Connection(wrds_username=os.getenv('WRDS_USERNAME'))`. Credentials in `~/.pgpass`.

---

## CRSP (Center for Research in Security Prices)

### Key tables

| Table | Contents | Frequency | Key columns |
|---|---|---|---|
| `crsp.msf` | Monthly stock file | Monthly | `permno`, `date`, `ret`, `retx`, `prc`, `shrout`, `vol` |
| `crsp.dsf` | Daily stock file | Daily | `permno`, `date`, `ret`, `prc`, `shrout`, `vol`, `bid`, `ask` |
| `crsp.msenames` | Name history | Event | `permno`, `namedt`, `nameendt`, `shrcd`, `exchcd`, `ticker`, `comnam` |
| `crsp.mseall` | Events (delisting, distribution) | Event | `permno`, `date`, `dlret`, `dlstcd`, `event` |
| `crsp.ccmxpf_lnkhist` | CCM link table | Event | `gvkey`, `lpermno`, `linkdt`, `linkenddt`, `linktype`, `linkprim` |
| `crsp.dseall` | Daily events | Event | `permno`, `date`, `dlret`, `dlstcd` |

### Known issues and gotchas

1. **Delisting returns**: CRSP `ret` does NOT include the delisting return. You must merge `dlret` from `crsp.mseall` (monthly) or `crsp.dseall` (daily) and compound:
   ```python
   # Correct delisting return adjustment
   df = df.merge(delist[['permno', 'date', 'dlret']], on=['permno', 'date'], how='left')
   df['ret_adj'] = np.where(
       df['dlret'].notna(),
       (1 + df['ret'].fillna(0)) * (1 + df['dlret']) - 1,
       df['ret']
   )
   ```
   Failing to adjust creates survivorship bias that inflates returns by 0.5-1% annually (Shumway 1997, Beaver et al. 2007).

2. **Share codes**: Filter to common shares: `shrcd in (10, 11)`. Including REITs (18), ADRs (31), closed-end funds (14), etc. contaminates cross-sectional tests.

3. **Exchange codes**: `exchcd in (1, 2, 3)` for NYSE, AMEX, NASDAQ. Code 0 = unknown. Codes change over time (check `msenames` for the date-valid exchange).

4. **Price sign convention**: `prc` is negative when it represents the bid-ask midpoint (no closing trade). Use `abs(prc)` for market cap calculations:
   ```python
   df['me'] = abs(df['prc']) * df['shrout'] / 1000  # in $millions
   ```

5. **Multiple share classes**: A single firm can have multiple `permno`s (e.g., Alphabet GOOGL/GOOG). For firm-level analysis, keep only the primary permno (largest market cap) or aggregate.

6. **Monthly date convention**: CRSP monthly dates are the last trading day of the month. When merging with Compustat (which uses calendar month-end), use month-year matching, not exact date matching:
   ```python
   df['ym'] = df['date'].dt.to_period('M')
   ```

7. **Penny stocks**: Consider excluding stocks with price < $5 (or $1) to avoid microstructure noise.

### Standard filters
```python
# Standard CRSP monthly sample
query = """
SELECT a.permno, a.date, a.ret, a.retx, a.prc, a.shrout, a.vol,
       b.shrcd, b.exchcd, b.ticker
FROM crsp.msf a
LEFT JOIN crsp.msenames b
  ON a.permno = b.permno
  AND a.date BETWEEN b.namedt AND b.nameendt
WHERE a.date BETWEEN '1960-01-01' AND '2024-12-31'
  AND b.shrcd IN (10, 11)
  AND b.exchcd IN (1, 2, 3)
"""
```

---

## Compustat (Standard & Poor's)

### Key tables

| Table | Contents | Frequency | Key columns |
|---|---|---|---|
| `comp.funda` | Annual fundamentals | Annual | `gvkey`, `datadate`, `fyear`, `at`, `lt`, `ceq`, `sale`, `ni`, `oancf` |
| `comp.fundq` | Quarterly fundamentals | Quarterly | `gvkey`, `datadate`, `fqtr`, `fyearq`, `atq`, `saleq`, `niq` |
| `comp.company` | Company identifiers | Static | `gvkey`, `conm`, `sic`, `naics`, `fic`, `loc` |
| `comp.secm` | Monthly security prices | Monthly | `gvkey`, `datadate`, `prccm`, `cshoq`, `cshtrm` |
| `comp.secd` | Daily security prices | Daily | `gvkey`, `datadate`, `prccd`, `cshtrd` |

### Known issues and gotchas

1. **Backfill bias (look-ahead bias)**: Compustat backfills data when firms are added. Historical data for newly added firms reflects current reporting, not what was available in real time. Fix: use the `indfmt='INDL'` and `datafmt='STD'` filters, and only use data that would have been available at the time:
   ```python
   # Compustat annual with standard filters
   query = """
   SELECT gvkey, datadate, fyear, at, lt, ceq, sale, ni, oancf,
          dp, xrd, capx, dltt, dlc, che, csho, prcc_f
   FROM comp.funda
   WHERE indfmt = 'INDL'
     AND datafmt = 'STD'
     AND popsrc = 'D'
     AND consol = 'C'
     AND datadate BETWEEN '1960-01-01' AND '2024-12-31'
   """
   ```

2. **Fiscal year timing**: Firms have different fiscal year-end months. A firm with a June FY-end reports FY2023 data in mid-2023, while a December FY-end firm reports FY2023 data in early 2024. To avoid look-ahead bias, lag accounting data by at least 4 months (6 months is conservative):
   ```python
   # Standard Fama-French timing: match fiscal year t-1 data
   # with returns from July year t to June year t+1
   df['jdate'] = df['datadate'] + pd.DateOffset(months=6)  # available date
   df['jdate'] = df['jdate'] + MonthEnd(0)  # align to month-end
   ```

3. **Missing values vs. zeros**: Compustat uses blanks (NaN) for missing data and genuine zeros for zero values. Do NOT replace NaN with zero for items like R&D (`xrd`), advertising (`xad`), or intangibles (`intan`). A missing R&D is not the same as zero R&D.

4. **Variable definitions change over time**: Some Compustat items are redefined or discontinued. Check the variable documentation for your sample period. Examples:
   - `oancf` (operating cash flow) is only available from 1988
   - `xrd` (R&D) has more coverage after 1975
   - `ppegt` vs. `ppent` (gross vs. net PP&E)

5. **Duplicate observations**: Compustat can have duplicates for firms with multiple fiscal year changes. Deduplicate:
   ```python
   df = df.sort_values(['gvkey', 'datadate', 'fyear'])
   df = df.drop_duplicates(subset=['gvkey', 'fyear'], keep='last')
   ```

6. **Canadian and international firms**: `comp.funda` includes Canadian firms (currency = CAD). Filter to US firms:
   ```python
   # US firms only
   query += " AND fic = 'USA'"
   # Or filter by currency: AND curcd = 'USD'
   ```

### Common variable construction

```python
# Book equity (Davis, Fama, and French 2000)
df['be'] = np.where(
    df['seq'].notna(), df['seq'],
    np.where(df['ceq'].notna(), df['ceq'] + df['pstk'].fillna(0),
             df['at'] - df['lt'])
) - df['ps'].fillna(df['pstkl'].fillna(df['pstk'].fillna(0))) + df['txditc'].fillna(0)
df['be'] = df['be'].clip(lower=0.01)  # Exclude negative book equity

# Market leverage
df['mlev'] = (df['dltt'].fillna(0) + df['dlc'].fillna(0)) / (
    df['dltt'].fillna(0) + df['dlc'].fillna(0) + df['csho'] * df['prcc_f']
)

# Book leverage
df['blev'] = (df['dltt'].fillna(0) + df['dlc'].fillna(0)) / df['at']

# Profitability (ROA)
df['roa'] = df['ni'] / df['at'].replace(0, np.nan)

# Investment (asset growth)
df['ag'] = df.groupby('gvkey')['at'].pct_change()

# Tobin's Q
df['tobinq'] = (df['at'] - df['ceq'] + df['csho'] * df['prcc_f']) / df['at']
```

---

## CRSP-Compustat Merged (CCM)

### Standard merge recipe

```python
# Step 1: Get CCM link table
ccm = db.raw_sql("""
    SELECT gvkey, lpermno AS permno, linkdt, linkenddt, linktype, linkprim
    FROM crsp.ccmxpf_lnkhist
    WHERE linktype IN ('LU', 'LC')
      AND linkprim IN ('P', 'C')
""")
ccm['linkenddt'] = ccm['linkenddt'].fillna(pd.Timestamp('2099-12-31'))

# Step 2: Merge Compustat with CRSP via CCM
# Align fiscal year-end with CRSP monthly dates
df_comp['jdate'] = df_comp['datadate'] + pd.DateOffset(months=6)
df_comp['jdate'] = df_comp['jdate'] + MonthEnd(0)

# Step 3: Merge on gvkey and date range
merged = df_comp.merge(ccm, on='gvkey')
merged = merged[
    (merged['jdate'] >= merged['linkdt']) &
    (merged['jdate'] <= merged['linkenddt'])
]
merged = merged.drop(columns=['linkdt', 'linkenddt', 'linktype', 'linkprim'])

# Step 4: Merge with CRSP
final = df_crsp.merge(merged, on=['permno', 'jdate'], how='inner')
```

### Known issues

1. **Link types**: Use `LU` (link used in research) and `LC` (link confirmed). Exclude `LD` (duplicate), `LN` (no link), `NR`, `NU`.
2. **Link primacy**: Use `P` (primary) and `C` (primary, conditional). `J` (joint) links should be investigated case by case.
3. **Match rate**: Expect ~85-90% of CRSP common stocks to match Compustat. Lower rates indicate a problem with the merge logic.
4. **One-to-many links**: A single `gvkey` can map to multiple `permno`s (holding companies, share classes). Keep the primary link or the largest market cap.

---

## IBES (Institutional Brokers' Estimate System)

### Key tables

| Table | Contents | Key columns |
|---|---|---|
| `ibes.statsum_epsus` | Summary statistics (consensus) | `ticker`, `statpers`, `fpedats`, `fpi`, `meanest`, `medest`, `stdev`, `numest`, `actual` |
| `ibes.det_epsus` | Individual analyst estimates | `ticker`, `analys`, `anndats`, `value`, `fpedats`, `fpi` |
| `ibes.id` | Identifier mapping | `ticker`, `cusip`, `cname`, `sdates` |
| `ibes.iclink` | CRSP link | `ticker`, `permno`, `score` |

### Known issues and gotchas

1. **IBES uses its own ticker**: Not the same as CRSP or exchange tickers. Must use `ibes.iclink` to map to CRSP `permno`:
   ```python
   iclink = db.raw_sql("""
       SELECT ticker, permno, score
       FROM ibes.iclink
       WHERE score IN (0, 1, 2)
   """)
   # score 0 = best match, 1 = good, 2 = acceptable
   # Exclude score > 2 (poor matches)
   ```

2. **Forecast period indicator (`fpi`)**: `1` = current fiscal year (FY1), `2` = next fiscal year (FY2). For quarterly: `6` = current quarter (FQ1), `7` = next quarter (FQ2).

3. **Actual announcement timing**: Use `statpers` (statistics period, i.e., the month the consensus was formed) not `fpedats` (fiscal period end date) for timing. The consensus for FY1 in January 2024 reflects analyst knowledge as of January 2024.

4. **Stale forecasts**: IBES carries forward stale estimates. For research using the most recent consensus, filter to estimates within the last 90 days:
   ```python
   # Keep only non-stale estimates
   query = """
   SELECT ticker, statpers, fpedats, fpi, meanest, medest, actual, numest
   FROM ibes.statsum_epsus
   WHERE fpi = '1'
     AND statpers BETWEEN '1980-01-01' AND '2024-12-31'
     AND EXTRACT(MONTH FROM statpers) = EXTRACT(MONTH FROM fpedats) - 1
   """
   ```

5. **Earnings surprise calculation**:
   ```python
   # Standardized unexpected earnings (SUE)
   df['sue'] = (df['actual'] - df['medest']) / abs(df['prc'])
   # Alternative: scale by std of estimates
   df['sue_alt'] = (df['actual'] - df['medest']) / df['stdev']
   ```

6. **Split adjustment**: IBES adjusts historical data for splits. Be careful when merging with unadjusted CRSP prices. Use CRSP adjusted prices or adjust manually.

---

## TRACE (Trade Reporting and Compliance Engine -- Corporate Bonds)

### Key tables

| Table | Contents | Key columns |
|---|---|---|
| `trace.trace_enhanced` | Enhanced TRACE transactions | `cusip_id`, `trd_exctn_dt`, `trd_exctn_tm`, `rptd_pr`, `entrd_vol_qt`, `rpt_side_cd`, `cntra_mp_id` |

### Known issues and gotchas

1. **Duplicate reports**: TRACE has agency and interdealer trades that create duplicates. The standard cleaning procedure (Dick-Nielsen 2009, 2014):
   ```python
   # Remove cancellations and corrections
   df = df[df['trc_st'].isin(['T', 'Y'])]  # Keep original and corrected
   # Remove reversals
   df = df[df['asof_cd'] != 'R']
   # Remove agency transactions to avoid double-counting
   df = df[~((df['rpt_side_cd'] == 'S') & (df['cntra_mp_id'] == 'C'))]
   ```

2. **Price filters**: Exclude trades with prices below $5 or above $200 (likely errors). Also exclude trades with volume < $10,000 (retail noise):
   ```python
   df = df[(df['rptd_pr'] >= 5) & (df['rptd_pr'] <= 200)]
   df = df[df['entrd_vol_qt'] >= 10000]
   ```

3. **Pre-2012 data quality**: Enhanced TRACE starts in July 2002. Data quality improves significantly after February 2005 (Phase III). Pre-2005 data requires more aggressive cleaning.

4. **Bond identifier**: `cusip_id` in TRACE is 9-character. To match with FISD or other bond databases, you may need 6-character (issuer) or 9-character CUSIP matching.

---

## Fama-French Factor Data

### Access via WRDS or pandas-datareader

```python
# Option 1: WRDS
ff = db.raw_sql("""
    SELECT date, mktrf, smb, hml, rf, umd
    FROM ff.factors_monthly
""")

# Option 2: pandas-datareader (no WRDS needed)
import pandas_datareader.data as web
ff3 = web.DataReader('F-F_Research_Data_Factors', 'famafrench', start='1960')[0] / 100
ff5 = web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench', start='1960')[0] / 100
mom = web.DataReader('F-F_Momentum_Factor', 'famafrench', start='1960')[0] / 100
```

### Known issues

1. **Return units**: WRDS FF data is in decimal (0.01 = 1%). pandas-datareader returns percentage points (1.0 = 1%). Divide by 100 when using datareader.
2. **Monthly date**: FF dates are YYYYMM integers. Convert:
   ```python
   ff.index = pd.to_datetime(ff.index.astype(str), format='%Y%m') + MonthEnd(0)
   ```

---

## Dealscan (Loan-Level Data)

### Key tables

| Table | Contents | Key columns |
|---|---|---|
| `dealscan.facility` | Loan facility details | `facilityid`, `packageid`, `facilityamt`, `facilitystartdate`, `maturity`, `facilitypurpose` |
| `dealscan.package` | Deal package | `packageid`, `dealid`, `borrowercompanyid`, `dealactivedate` |
| `dealscan.borrower` | Borrower info | `borrowercompanyid`, `company`, `ticker` |
| `dealscan.lender` | Lender shares | `facilityid`, `lender`, `lenderrole`, `bankallocation` |
| `tr_dealscan.wrds_compustat_link` | Link to Compustat | `facilityid`, `gvkey`, `bcoid`, `score` |

### Known issues

1. **Identifier linking**: Dealscan uses its own `borrowercompanyid`. Link to Compustat via `tr_dealscan.wrds_compustat_link`:
   ```python
   link = db.raw_sql("""
       SELECT facilityid, gvkey, bcoid, score
       FROM tr_dealscan.wrds_compustat_link
       WHERE score <= 3
   """)
   ```
   Score 1 = best, higher = worse. Most research uses score <= 3.

2. **Multiple facilities per deal**: A single loan deal (`packageid`) can have multiple facilities (term loan + revolver). Decide whether to analyze at the facility or deal level.

3. **Covenant data**: Available in `dealscan.covenant` but coverage is incomplete, especially for recent years. Financial covenants are better covered than non-financial ones.

---

## BoardEx

### Key tables

| Table | Contents | Key columns |
|---|---|---|
| `boardex.na_wrds_company_profile` | Company profiles | `boardid`, `companyid`, `companyname`, `isin`, `ticker` |
| `boardex.na_wrds_org_composition` | Board composition | `companyid`, `directorid`, `datestartrole`, `dateendrole`, `rolename` |
| `boardex.na_dir_profile_emp` | Director employment | `directorid`, `companyid`, `rolename`, `datestartrole` |

### Known issues

1. **Identifier matching**: BoardEx uses its own `companyid`. Match to CRSP/Compustat via ISIN or ticker (imperfect). WRDS provides a linking table in some subscriptions.
2. **Date coverage**: North America coverage starts ~1999. Non-NA coverage varies.
3. **Role classification**: `rolename` strings are messy. CEO identification requires parsing: look for "CEO", "Chief Executive", etc.

---

## Option Metrics

### Key tables

| Table | Contents | Key columns |
|---|---|---|
| `optionm.opprcd` | Option prices | `secid`, `date`, `exdate`, `cp_flag`, `strike_price`, `best_bid`, `best_offer`, `impl_volatility`, `volume`, `open_interest` |
| `optionm.secprd` | Security prices (underlying) | `secid`, `date`, `close`, `return` |
| `optionm.secnmd` | Security identifiers | `secid`, `cusip`, `ticker`, `effect_date` |

### Known issues

1. **`secid` not `permno`**: OptionMetrics uses its own `secid`. Link to CRSP via CUSIP or ticker matching.
2. **Strike price scaling**: `strike_price` is multiplied by 1000. Divide by 1000 for the actual strike:
   ```python
   df['strike'] = df['strike_price'] / 1000
   ```
3. **Implied volatility**: Missing for deep ITM/OTM options and illiquid contracts. Filter to options with valid `impl_volatility`.
4. **American vs. European**: Most US equity options are American-style. IV calculation accounts for early exercise, but this introduces model dependency.

---

## General WRDS tips

### Performance

- **Use SQL filters**: Always filter in the SQL query, not after downloading. WRDS tables can have billions of rows.
- **Select specific columns**: Never use `SELECT *` on large tables.
- **Date ranges**: Always include a date range in the WHERE clause.
- **Chunked downloads**: For very large queries, download in year-chunks:
  ```python
  dfs = []
  for year in range(1960, 2025):
      chunk = db.raw_sql(f"SELECT ... WHERE date BETWEEN '{year}-01-01' AND '{year}-12-31'")
      dfs.append(chunk)
  df = pd.concat(dfs, ignore_index=True)
  ```

### Discovering tables

```python
# List all tables in a library
db.list_tables(library='crsp')

# Describe a table's columns
db.describe_table(library='crsp', table='msf')

# Count rows
db.raw_sql("SELECT COUNT(*) FROM crsp.msf")
```

### Saving and versioning

- Save downloaded data to `raw/` as parquet: `df.to_parquet('raw/crsp_monthly.parquet')`
- Include the download date in a comment or metadata file
- Never modify files in `raw/`. Process in `build/`.

---

## Quick reference: Which identifier links what

| From | To | Link table / method | Match rate |
|---|---|---|---|
| CRSP (`permno`) | Compustat (`gvkey`) | `crsp.ccmxpf_lnkhist` | ~85-90% |
| CRSP (`permno`) | IBES (`ticker`) | `ibes.iclink` | ~80-85% |
| Compustat (`gvkey`) | Dealscan (`bcoid`) | `tr_dealscan.wrds_compustat_link` | varies |
| CRSP (`permno`) | OptionMetrics (`secid`) | CUSIP/ticker match | ~90% |
| CRSP (`permno`) | BoardEx (`companyid`) | ISIN/ticker match | ~80% |
| Compustat (`gvkey`) | CRSP (`permno`) | `crsp.ccmxpf_lnkhist` (reverse) | same link |

### Identifier gotchas

- **CUSIP changes**: CUSIPs change after mergers, spinoffs, and reincorporations. Use historical CUSIP, not current.
- **Ticker reuse**: Tickers are recycled. AAPL was Apple but could be reassigned. Always use permanent identifiers (`permno`, `gvkey`) for merges.
- **PERMNO vs. PERMCO**: `permno` identifies a security (share class). `permco` identifies a company. A company can have multiple permnos.
- **GVKEY persistence**: `gvkey` survives name changes but not mergers. After a merger, the acquired firm gets a new gvkey or is dropped.
