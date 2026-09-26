---
status: accepted
---

# Use a modular ingestion pipeline

The project uses separate acquisition, source-storage, structural-parsing, lore-analysis, knowledge-resolution, rendering, and validation modules instead of one monolithic script. The extra seams make source preservation independently testable and let lore analysis evolve without risking the archived originals.
