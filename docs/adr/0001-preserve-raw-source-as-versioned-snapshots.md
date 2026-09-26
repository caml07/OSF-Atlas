---
status: accepted
---

# Preserve raw source as versioned snapshots

Each Episode keeps the exact source material exposed by YouTube as a Raw Source snapshot. If the upstream description or captions change later, the collector creates a new Source Revision instead of overwriting the previous one; this costs a small amount of extra disk space but keeps the archive reproducible and lets the vault show what changed over time.
