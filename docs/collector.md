# Collector and Parser

Status: planning reference

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

## Diagnostic commands

Lower-level commands remain available for debugging and maintenance:

```bash
osf fetch 001
osf fetch 001-010

osf build 001
osf build 001-010
osf build --all

osf check 001
osf check 001-010

osf review
osf status
```

Exact CLI spelling is still provisional until implementation.

## Acquisition

Planned implementation language: Python.

Planned acquisition adapter: `yt-dlp` CLI, not deep coupling to yt-dlp internals.

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

The acquisition adapter records what subtitle/caption tracks yt-dlp reports as
available before requesting files.

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

## Relationship review memory

The knowledge layer persists accepted and rejected decisions.

A rejected candidate can be explicitly reopened if later source material changes its interpretation.

## Parser/schema versions

Generated artifacts track:

```yaml
schema_version: 1
parser_version: 1
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

The first formal corpus batch remains 001-010 after parser fixtures prove the architecture.
