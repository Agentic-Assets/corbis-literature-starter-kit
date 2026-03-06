# Replication Package Checklist

Complete before submission. Every item must be checked or explicitly marked N/A with a reason.

## Documentation
- [ ] Replication README is complete and self-contained
- [ ] Provenance matrix covers every table, figure, and appendix exhibit
- [ ] Data access matrix classifies every data source
- [ ] Rerun order is numbered and unambiguous

## Code
- [ ] All scripts run without error from a clean environment
- [ ] No hardcoded absolute paths remain
- [ ] No credentials, API keys, or tokens in any file
- [ ] Random seeds are set and documented where applicable
- [ ] `requirements.txt` or `environment.yml` is current and complete

## Data
- [ ] Public data are included or download scripts are provided
- [ ] Licensed data queries are included with expected schemas
- [ ] Restricted data have schema-only placeholders and access instructions
- [ ] Confidential data are documented with variable definitions and summary stats
- [ ] No data files are included that should not be shared
- [ ] Data extract dates are recorded

## Outputs
- [ ] Every output file traces to a script in the provenance matrix
- [ ] No orphan outputs (files with no originating script)
- [ ] Table and figure numbering matches the manuscript

## Package structure
- [ ] Folder structure is clean and documented
- [ ] No temporary files, caches, or IDE artifacts
- [ ] `.gitignore` excludes sensitive and generated files
- [ ] Package size is reasonable for the target archive

## Journal-specific
- [ ] Target archive platform identified (Mendeley Data, Harvard Dataverse, etc.)
- [ ] Format matches platform requirements
- [ ] Any required exceptions (restricted data) were requested at initial submission
