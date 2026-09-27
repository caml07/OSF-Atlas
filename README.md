# Obsidian Soundfields Atlas

A local-first Obsidian vault for reading, preserving, and connecting the numbered **Obsidian Soundfields (OSF)** series.

The project keeps the source material exposed by each video separate from the knowledge graph built around it:

- exact extracted source is preserved as immutable local revisions;
- a generated Reader Source makes the material comfortable to read in Obsidian;
- Episodes, Entities, and Lore Threads remain distinct graph nodes;
- explicit lore references keep provenance;
- personal notes, favorites, ratings, and reading state remain human-owned;
- video and audio are intentionally not downloaded.

## Open the vault

Open this directory directly in Obsidian:

```text
/home/caml/Documents/Obsidian/Obsidian Soundfields
```

The local vault uses:

- Minimal theme
- Comfortaa
- native Properties
- native Bases
- Graph / Local Graph
- native Templates
- one small local CSS snippet for the OSF visual layer

No community plugin is required for the core experience.

## Start here

Open [[00 Atlas/OSF Atlas|OSF Atlas]].

Useful surfaces:

- [[00 Atlas/Index|Episode Index]]
- [[00 Atlas/Chronology|Chronology]]
- [[00 Atlas/Favorites|Favorites]]
- [[00 Atlas/Reading Progress|Reading Progress]]
- [[00 Atlas/Lore Map|Lore Map]]
- [[00 Atlas/Review Queue|Review Queue]]
- [[00 Atlas/Source Health|Source Health]]

## Structure

```text
00 Atlas/                 home, Bases, review and navigation
01 Episodes/              one note per numbered OSF release
02 Entities/              in-universe graph nodes
03 Lore Threads/          recurring narrative relationships
04 My Notes/              human-owned research / opinions / theories
05 Sources/               Reader Source + local immutable raw revisions
06 Assets/                local thumbnails and future vault assets
90 Templates/             Obsidian note templates
tools/osf/                collector/parser project (next milestone)
tests/                    TDD fixtures and behavioral tests (next milestone)
.osf/                     machine state / canonical knowledge internals
docs/                     architecture, UX, decisions and implementation plan
```

## Human-owned Episode state

Every Episode supports:

```yaml
favorite: false
rating:
status: unread
last_read:
```

Ratings use a **1–10** scale. The `osf-vault` agent skill can maintain these fields during agentic reading and can capture free-form Spanish/English/Spanglish research notes without treating personal interpretation as canon.

## Current implementation state

Planning is complete. The vault scaffold implements the approved Obsidian UX and project structure.

The collector/parser and corpus ingestion have **not** started yet. See [[docs/plan-v3|Plan v3]] for the implementation sequence.
