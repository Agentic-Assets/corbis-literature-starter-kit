---
description: Fetch data from public APIs (FRED, BLS, Census, BEA, FHFA, SEC EDGAR, Yahoo Finance)
---

Fetch data from public sources for the following request:

$ARGUMENTS

Load API keys from `.env` file using `python-dotenv`. Connect to the appropriate source based on the request.

**Available sources and when to use them:**

| Source | Use for | Connection |
|---|---|---|
| FRED | Macro series (rates, prices, employment, housing) | `fredapi.Fred(api_key=os.getenv('FRED_API_KEY'))` |
| BLS | CPI components, employment by industry, wages | `requests` to `https://api.bls.gov/publicAPI/v2/timeseries/data/` with `registrationkey` |
| Census/ACS | Demographics, income, housing by geography | `requests` to `https://api.census.gov/data/` with `key` param |
| BEA | GDP components, regional income, IO tables | `requests` to `https://apps.bea.gov/api/data` with `UserID` param |
| FHFA | House price indices by metro/state | Direct download from `https://www.fhfa.gov/data` (no key needed) |
| SEC EDGAR | Company filings (10-K, 10-Q, 8-K, proxy) | `sec_edgar_downloader` (no key, rate limited) |
| Yahoo Finance | Stock prices, quick market data | `yfinance.download()` (no key) |
| Fama-French | Factor returns, industry portfolios | `pandas_datareader.famafrench` (no key) |

**Common FRED series for finance/RE research:**
- Housing: CSUSHPISA, USSTHPI, HOUST, PERMIT, MSACSR, MSPUS
- Mortgage: MORTGAGE30US, MORTGAGE15US, MORTGAGE5US
- Rates: FEDFUNDS, DGS10, DGS2, T10Y2Y, BAMLC0A0CM
- Macro: UNRATE, GDPC1, CPIAUCSL, RSAFS, UMCSENT
- Credit: DRTSCILM, TOTBKCR, BUSLOANS
- CRE: BOGZ1FL075035503Q, COMREPUSQ159N

**Common BLS series:**
- CPI-U: CUSR0000SA0
- CPI Rent: CUSR0000SEHA
- CPI OER: CUSR0000SEHC
- Employment: CES0000000001

**Code template:**
```python
import os
from dotenv import load_dotenv
load_dotenv()

# Then use the appropriate library
```

**Rules:**
- Save downloaded data to `raw/` as parquet
- Print shape, date range, and column names after download
- If an API key is missing, tell the user which key they need and point them to `.env.example`
- For large downloads, warn about size and confirm before proceeding
