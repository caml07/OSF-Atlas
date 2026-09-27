# Collector and Parser

Status: implemented v1; corpus ingestion in progress

## Purpose

The collector/parser preserves source material first and builds Obsidian projections second. Source acquisition must remain useful even if semantic analysis fails.

## Main command

Normal use should expose one deep interface:

```bash
osf ingest 001-010
```

Conceptually:

```text
fetch
→ stage
→ validate
→ preserve/promote
→ parse
→ resolve
→ render
→ validate
```

## Commands

The implemented CLI currently exposes:

```bash
osf ingest 001-010
osf check 001
osf check 001-010
osf status
osf catalog
```

Lower-level `fetch/build/review` commands remain future extensions; the v1 CLI
keeps the normal interface intentionally small.

## Acquisition

Implementation language: Python.

Acquisition adapter: `yt-dlp` CLI, not deep coupling to yt-dlp internals.

For each Episode retrieve without downloading video/audio:

- video ID
- title
- publication metadata
- full description
- original English manual captions if present
- original English automatic captions if present
- best available thumbnail
- info JSON needed by the project

Do not archive auto-translated subtitle tracks.

Manual English tracks are preserved when exposed by `subtitles`. Automatic
English captions are accepted only when YouTube/yt-dlp exposes an English
original track (`en-orig`) or metadata establishes English as the original
language. Auto-translated tracks are not archived.

## Staging and failure

New retrieval first lands under a staging area.

A failed attempt:

- records failure state and useful diagnostics;
- does not create/promote a Source Revision;
- does not replace the last valid revision;
- makes failure visible in status/Atlas.

Process exit code is not sufficient evidence of a complete extraction. The
Validator compares reported source availability with the files/manifests
actually produced, so a missing requested caption track becomes a failed or
explicitly unavailable result rather than a silent success.

## Parsing

Do not implement one giant regex.

The StructuralParser may use targeted regexes internally for concrete syntax such as:

- `OSF-053`
- incident-log labels
- standalone structural labels such as `[VISITOR'S PASS]`
- separators
- known footer boundaries
- hashtags/links

Semantic relationships are resolved separately.

## Link policy

Reader Source annotations may link:

- explicit numbered OSF references → automatically when unambiguous
- confirmed canonical Entities → yes
- confirmed aliases → yes
- candidates → no
- fuzzy matches → no
- rejected matches → no

Knowledge resolution may also surface an **exact canonical Episode title or a
safe article-stripped alias** as a `candidate` when it appears in another
Episode's source. This does not annotate Reader Source until reviewed.

Example from Batch 011-020:

```text
018 // Phantom Port
source mentions "Veiled Monolith"
→ candidate connection to 014 // The Veiled Monolith
```

## Relationship review memory

The knowledge layer persists accepted and rejected decisions.

A rejected candidate can be explicitly reopened if later source material changes its interpretation.

## Parser/schema versions

Generated artifacts track:

```yaml
schema_version: 1
parser_version: 2
```

This allows derived Markdown and knowledge projections to be rebuilt from preserved raw sources without refetching YouTube.

## Source fingerprint

Idempotence uses a fingerprint derived from material archival source:

- description payload;
- original English caption tracks;
- thumbnail bytes;
- stable video/source identity.

Volatile fields such as view/like/comment counts do not participate in the
fingerprint, even if a retrieved metadata file contains them.

## TDD

Behavior is developed vertically, red → green, one seam at a time.

Representative fixtures should include at minimum:

- an early/simple Episode;
- a direct sequel/location variant;
- a later Episode with an Incident Log;
- `090`-style source with no captions;
- `114`-style explicit numbered cross-reference;
- an Episode with original captions, if such an Episode exists.

The representative checks now cover:

- early/simple source and exact description preservation;
- synthetic manual + automatic English caption handling;
- exact colon-title variants such as `Silent Arbiter: Interior Hall` → `Silent Arbiter`;
- standalone all-caps bracket labels such as `[VISITOR'S PASS]` without
  assigning semantic meaning to the label;
- `090 // The Between` with no captions and `Incident Log 07-B`;
- `114 // The Veiled Monolith: Interior` with explicit parenthetical references
  to `OSF-014` and `OSF-053`.

The first formal corpus batch `001-010` passed its ingestion gate.

Batch `051-060` was the first formal corpus batch where YouTube exposed real
manual English caption tracks. Episodes `052`, `054`, `055`, `056`, `058`, and
`060` preserved those VTT tracks separately from the YouTube description and
passed source/hash/Reader Source validation without requiring a parser change.
