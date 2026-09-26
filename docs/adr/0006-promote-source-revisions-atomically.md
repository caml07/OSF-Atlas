---
status: accepted
---

# Promote source revisions atomically

New Episode data is first collected into staging and becomes a Source Revision only after required files and validations pass. Failed extractions are recorded as failures and never replace the current valid revision, preventing mixed old/new source state after network, YouTube, or parser errors.
