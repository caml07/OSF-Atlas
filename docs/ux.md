# Obsidian UX

Status: scaffold implemented; collector-backed content pending

## Design intent

The vault should feel like a dark, quiet OSF research atlas rather than a corporate dashboard. Reading the original source is primary; graph exploration, lore analysis, and personal research sit around it.

## Episode Note

The scaffold implements the approved information hierarchy:

```text
Episode title
thumbnail → clickable YouTube video
compact metadata / personal properties

Source
  embedded Reader Source

Lore Overview
Entities
Connections
  Confirmed
  Candidates
  Inferred

My Notes
```

The source appears high on the page because reading the complete OSF material is the primary use case.

### Human-owned properties

Episode templates include from v1:

```yaml
favorite: false
rating:
status: unread
last_read:
```

- `favorite`: checkbox
- `rating`: numeric personal rating from 1 through 10; decimals are allowed when explicitly chosen
- `status`: `unread | reading | complete`
- `last_read`: date/time, human-owned

Obsidian Properties natively supports checkboxes, numbers, dates, and date/time values, so these fit the core property model without a community plugin.

## Reader Source

The Reader Source is embedded into the Episode Note.

Example shape:

```markdown
# Source — 090 // The Between

> [!info]
> Reader projection generated from Source Revision
> `2026-09-25_05-43-00Z`.
> Raw source files are preserved unchanged.

## YouTube Description

<complete description with safe confirmed wiki-link annotations>

> [!abstract]- English Manual Captions
> <complete caption text>

> [!abstract]- English Automatic Captions
> <complete caption text>
```

The YouTube Description remains expanded. Other source tracks are collapsible.

## Atlas

`00 Atlas/OSF Atlas.md` is the home screen of the vault.

Desired areas:

- corpus count / ingestion coverage
- personal reading progress
- Continue Reading
- Favorites
- highly rated episodes
- Needs Lore Review
- Recently Confirmed Connections
- Recent Source Changes / Failed Extractions
- Browse Episodes
- Browse Entities
- Browse Lore Threads
- Chronology
- My Notes / research notes

The Atlas should use native Obsidian links, embeds, callouts, and Bases views rather than hard-coding data that will become stale.

## Research notes outside Episodes

Personal/agentic notes do not need to live inside an Episode.

A research note may freely link:

```markdown
[[OSF 114 - The Veiled Monolith Interior]]
[[Terminal]]
[[OSF 053 - Terminal]]
[[Network Hypothesis]]
```

These notes remain human-owned and become first-class graph nodes under `04 My Notes/`.

## Review Queue

A central Review Queue exposes:

- candidates awaiting review
- recently auto-confirmed explicit references
- inferred connections
- rejected decisions
- reopened decisions

Rejected decisions persist so a rebuild does not repeatedly suggest the same relationship. A rejected decision may be reopened when new lore changes the interpretation.

## last_read automation

Core Obsidian can store `last_read` as Date & time but does not itself provide a built-in rule that updates an arbitrary property merely because a file was opened.

v1 includes the property as human-owned state.

The first automatic mechanism is the vault-local `osf-vault` agent skill:

- active reading/review → refresh `last_read` and set `status: reading` unless already complete;
- explicit completion → refresh `last_read` and set `status: complete`;
- factual lookup alone → no reading-state mutation.

A future small Obsidian plugin may additionally update `last_read` for normal
non-agentic Episode opens, but it is intentionally deferred until the core vault
experience proves that behavior useful.

## Continue Reading

The Atlas chooses Continue Reading deterministically:

1. the most recently read Episode whose status is `reading`;
2. otherwise the first chronological Episode whose status is `unread`.

This avoids another manually maintained dashboard field.

## Visual direction

The Atlas should be **minimalist and brutalist**, not dashboard-corporate:

- strong typography;
- restrained monochrome/dark surfaces;
- large episode imagery where useful;
- deliberate whitespace;
- thin structural rules and compact metadata;
- little decorative chrome;
- utility-heavy Bases behind a more editorial Atlas front page.
