---
description: Query WRDS data or explore available tables
---

Connect to WRDS and execute the following request:

$ARGUMENTS

Load credentials from `.env` and connect:
```python
from dotenv import load_dotenv
import os, wrds
load_dotenv()
db = wrds.Connection(wrds_username=os.getenv('WRDS_USERNAME'))
```

**Available libraries**: crsp, comp, ibes, tfn, dealscan, tr_dealscan, trace, optionm, boardex, ciq, risk, ff, frb, bank, wrdsapps.
**Not available**: fisd, kld, mfl, rpna, taq.

Common operations:
- "list tables in [library]" → `db.list_tables(library='crsp')`
- "describe [table]" → `db.describe_table(library='crsp', table='msf')`
- "download [query]" → `db.raw_sql("SELECT ...")`
- "how many observations in [table]" → `db.raw_sql("SELECT COUNT(*) FROM ...")`

When downloading data:
- Save to `raw/` directory as parquet: `df.to_parquet('raw/filename.parquet')`
- Print shape and column names after download
- Follow the date alignment and identifier conventions from the `python-empirical-code` skill
- Do not download more data than needed for the task
