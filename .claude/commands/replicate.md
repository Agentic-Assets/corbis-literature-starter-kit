---
description: Build a replication package for journal submission
---

Run the `replication-package-builder` skill for this project.

$ARGUMENTS

Steps:
1. Inventory the project directory structure
2. Classify every data source by shareability (public, licensed, restricted, confidential)
3. Build the dependency graph and rerun order
4. Map every paper output to its originating script (provenance matrix)
5. Capture the software environment
6. Scrub for hardcoded paths, credentials, and sensitive files
7. Generate a standalone replication README
8. Run a dry-run validation check

Produce all required deliverables: replication README, rerun order, provenance matrix, data access matrix, environment spec, sanitization checklist, and dry-run report.
