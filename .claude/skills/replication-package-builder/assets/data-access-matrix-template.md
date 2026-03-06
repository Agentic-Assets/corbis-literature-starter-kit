# Data Access Matrix Template

Classify every data source used in the project.

| Data source | Tier | Included in package? | Access instructions | Extract date | Key variables used |
|---|---|---|---|---|---|
| CRSP Monthly Stock File | Licensed-reproducible | No (query included) | WRDS institutional subscription; `crsp.msf` | 2024-01-15 | ret, prc, shrout, permno |
| Compustat Annual | Licensed-reproducible | No (query included) | WRDS institutional subscription; `comp.funda` | 2024-01-15 | at, sale, ni, gvkey |
| FRED: 10Y Treasury | Public | Yes (download script) | `fred_series_batch(["DGS10"])` or `fredapi` | 2024-02-01 | DGS10 |
| Census ACS | Public | Yes (download script) | Census API; key required | 2024-01-20 | median_income, pop |
| CoStar | Licensed-restricted | No (schema only) | Commercial license; contact vendor | 2023-Q4 | cap_rate, vacancy, rent_psf |
| Firm-level survey | Confidential | No (summary stats only) | Contact authors | 2023 | [variable list] |

## Tier definitions

| Tier | Meaning | Package action |
|---|---|---|
| **Public** | Freely downloadable | Include data or download script |
| **Licensed-reproducible** | Institutional access; query is reproducible | Include query script + expected schema |
| **Licensed-restricted** | Vendor prohibits redistribution | Schema-only placeholder + access instructions |
| **Confidential** | IRB/NDA restricted | Variable definitions + summary statistics only |
| **Generated** | Created by pipeline scripts | Do not include; pipeline recreates it |
