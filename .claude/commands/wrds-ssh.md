---
description: SSH to WRDS servers for SAS/Python
---

Run the `wrds-ssh` skill to connect to WRDS servers.

$ARGUMENTS

Connection: `ssh wrds` (pre-configured in `~/.ssh/config`).

Key operations:
- **SAS jobs**: Create `.sas` file on WRDS, submit with `qsas` (async), check `.log`/`.lst` output.
- **Python**: Submit with `qpython`.
- **SQL fallback**: `psql` on WRDS server (prefer local `psql service=wrds` instead).
- **File transfer**: `scp` or `rsync` to/from `wrds:~/scratch/`.

Notes:
- `qsas` is required on WRDS Cloud -- cannot run `sas` directly.
- Jobs are always asynchronous. Poll with `qstat`.
- Use `~/scratch/` for large files (auto-deleted after 48 hours).
