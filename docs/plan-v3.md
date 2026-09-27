# OSF Atlas Plan v3

Status: approved implementation plan

Progress:

- Milestone 0 — vault scaffold: **complete**
- Milestone 1 — parser project and TDD seams: **complete**
- Representative parser/adaptor checks: **complete**
- Batch 001–010: **complete**
- Batch 011–020: **complete**
- Batch 021–030: **complete**
- Discovery model / ELI5 README: **complete**
- Public-safe GitHub main: **complete**
- Batch 031–040: **complete**
- Batch 041–050: **complete**
- Batch 051–060: **complete**
- Batch 061–070: **complete**
- Batch 071–080: **complete**
- Batch 081–090: **complete**
- Batch 091–100: **complete**
- Batch 101–110: **complete**
- Batch 111–125: **complete**
- Final 001–125 consistency/lore-link sweep: **complete**

## Senior review

**Altitude:** balanced.

The design now defines product intent, source integrity, public module seams,
failure behavior, human/machine ownership, knowledge provenance, Obsidian UX,
and measurable batch completion.

### Blockers

None remaining after the final review.

### Major findings resolved

1. Raw preservation and Obsidian reading are separate layers.
2. Human-owned state cannot be overwritten by renderer rebuilds.
3. Parsing and semantic lore resolution are separate modules.
4. Relationship evidence and rejected/reopened decisions persist centrally.
5. Retrieval is staged and promoted atomically.
6. yt-dlp process success is not treated as proof of subtitle availability;
   expected artifacts are validated explicitly.
7. Source Revision identity excludes volatile popularity metadata and includes
   material archival artifacts.
8. Episode and Entity remain separate domain concepts.
9. Primary Episode subjects start as unclassified Entities; the parser does not
   guess Place/System/Person/etc. without evidence or human review.
10. Lore Threads emerge from reviewed discoveries instead of being generated as
    authoritative story summaries ahead of the user's reading.

### Deliberate v1 limitation

`last_read` updates automatically during agentic reading through the
`osf-vault` skill. Detecting ordinary non-agentic Obsidian note opens is
deferred rather than adding a custom plugin before it proves useful.

## Product goal

Create a local-first Obsidian atlas for the complete numbered Obsidian
Soundfields corpus where:

- source text exposed by each video is preserved exactly as extracted;
- source history is retained when upstream material changes;
- the complete description is comfortable to read from each Episode note;
- available original English captions remain accessible without dominating the
  page;
- thumbnails are stored locally in the best available retrieved quality and
  link back to YouTube;
- recurring lore produces a provenance-backed graph of Episodes, Entities, and
  Lore Threads;
- the user's own notes, favorites, ratings, and reading state are first-class
  human-owned data;
- no video or audio is downloaded.

## Implementation order

### Milestone 0 — Replace the provisional scaffold

Preserve:

- `CONTEXT.md`
- `docs/`
- `docs/adr/`
- local Git history

Replace/rebuild the provisional Atlas, templates, Base definitions, .obsidian
configuration, and old source-folder assumptions from the approved design.

Verification:

- the vault opens cleanly in Obsidian;
- Graph default filters hide technical/source nodes;
- Bases load without syntax errors;
- Episode template exposes human-owned properties;
- Atlas has the approved brutalist/minimalist information hierarchy.

### Milestone 1 — Establish parser project and TDD seams

Create the Python project under `tools/osf/` and test harness under `tests/`.

Public seams:

1. Collector
2. StructuralParser
3. KnowledgeResolver
4. Renderer
5. Validator

Work vertically red → green. Do not test private regex/helper implementation
unless it becomes an intentional public seam.

### Milestone 2 — Source acquisition and immutable revisions

Implement Collector + source staging first.

Required behavior:

- no video/audio;
- complete description;
- original English manual captions when available;
- original English automatic captions when available;
- no automatic translations;
- best available thumbnail;
- useful metadata;
- readable UTC revision directory name;
- hashes/fingerprint;
- failed attempt records;
- atomic promotion;
- idempotent unchanged re-fetch.

Verification:

- a failed or incomplete retrieval cannot replace the current valid revision;
- expected captions are validated from reported availability, not process exit
  code alone;
- repeated unchanged acquisition creates no duplicate revision;
- a material source or thumbnail change creates a new revision.

### Milestone 3 — Reader Source and Renderer

Generate `source.md` from preserved Raw Source.

Reader behavior:

- YouTube Description expanded;
- manual/automatic caption tracks collapsed;
- safe confirmed wiki-link annotations allowed;
- Raw Source remains unchanged.

Renderer behavior:

- merges frontmatter by ownership;
- preserves favorite/rating/status/last_read;
- protects My Notes;
- renders machine-owned sections reproducibly;
- records parser/schema versions.

Verification:

- source payload survives raw preservation without truncation/transformation;
- rebuilding cannot clobber human-owned properties or prose.

### Milestone 4 — Knowledge layer

Implement canonical relationship storage and evidence.

States:

- candidate
- confirmed
- inferred
- rejected
- reopened

Rules:

- explicit numbered OSF references may auto-confirm when unambiguous;
- confirmed canonical aliases may link;
- fuzzy/semantic similarity remains candidate;
- rejected choices persist;
- relationships are stored once and projected into all affected notes.

### Milestone 5 — Representative fixtures

Before formal corpus ingestion, exercise architecture against representative
sources:

- early/simple Episode;
- direct sequel/location variant;
- Incident Log/later-lore Episode;
- Episode 090 style source with no captions;
- Episode 114 style explicit numbered cross-reference;
- an Episode with original captions, if one exists.

These fixtures prove parser shape; they do not count as completing corpus
batches.

### Milestone 6 — Batch 001–010

Run the first real chronological batch through the complete pipeline.

Per-Episode ingestion gate:

- metadata retrieved;
- complete source preserved;
- available original English captions preserved;
- thumbnail preserved;
- hashes/fingerprint valid;
- Reader Source generated;
- Episode Note generated;
- explicit references resolved;
- internal links valid;
- human-owned state unchanged.

Batch ingestion closes only at 10/10 valid Episodes with no unresolved
extraction failure or silent truncation.

Lore review remains a separate completion state.

### Milestone 7+ — Continue chronological batches

- 011–020
- 021–030
- 031–040
- 041–050
- 051–060
- 061–070
- 071–080
- 081–090
- 091–100
- 101–110
- 111–120
- 121–125

Later discoveries may update the canonical knowledge layer and regenerate
earlier Episode/Entity views without mutating preserved source.

### Final milestone — consistency sweep

- validate all 125 Episodes;
- validate source coverage;
- check broken wiki-links;
- check orphaned/duplicate Entities;
- review unresolved candidates;
- verify Atlas/Bases/Graph;
- verify rebuild from Raw Source;
- verify human-owned fields survive a full rebuild.

## Agentic research

The `osf-vault` skill is the human/research companion layer.

It can:

- capture free-form opinions and Spanglish notes;
- create/link Research Notes;
- distinguish Episode from Entity;
- update favorite/rating/status/last_read;
- record lore review decisions when the knowledge schema exists;
- make narrow local Git commits after completed note work.

It cannot:

- ingest YouTube;
- modify Raw Source;
- silently convert interpretation into canon;
- push Git without explicit user instruction.

## Deferred

- custom Obsidian plugin for automatic `last_read` on ordinary note opens;
- GitHub/public distribution;
- copyright/publication policy;
- audio/video archival;
- heavy community-plugin dependency.
