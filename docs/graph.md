# Graph Design

Status: scaffold implemented

## Why filter the graph

Obsidian Graph represents notes as nodes and internal links as edges. If generated source files, technical manifests, templates, and archival internals are all visible, the graph stops representing lore and starts representing the implementation of the archive.

The default graph therefore emphasizes semantic/research nodes.

## Visible by default

- `01 Episodes/`
- `02 Entities/`
- `03 Lore Threads/`
- `04 My Notes/`
- selected Atlas/MOC notes when useful

## Hidden by default

- `05 Sources/`
- `06 Assets/`
- `90 Templates/`
- `docs/`
- `tests/`
- `.osf/`
- implementation/tooling files

These files are not deleted or inaccessible. They are simply filtered out of the normal global Graph so lore remains legible.

The user can deliberately remove/alter filters when they want to inspect technical/source nodes.

The default implementation should prefer a Graph-specific search filter such as negative `path:` clauses rather than Obsidian's global **Excluded files** setting. This keeps Sources and technical notes available to File Explorer and normal Search while hiding them from the lore graph.

## Node semantics

### Episode

A numbered YouTube release/document.

Example:

```text
OSF 053 - Terminal
```

### Entity

An in-universe concept with independent lore identity.

Example:

```text
Terminal
```

Episode and Entity remain distinct even when they share a name.

This enables:

```text
Terminal
├── appears in → OSF 053 - Terminal
├── referenced by → OSF 114 - ...
└── connected to → other Entities
```

## Entity creation threshold

Create an Entity when at least one is true:

1. source explicitly establishes it as a place/system/organization/person/phenomenon;
2. it appears across multiple Episodes;
3. another Episode explicitly references it;
4. it is the primary subject/location of an Episode;
5. the user intentionally promotes it into an Entity.

Do not create nodes for every capitalized word.

## Aliases

Aliases require evidence.

Safe aliases may resolve automatically. Ambiguous phrases such as generic uses of “the Monolith” should not silently resolve to a canonical Entity.

## Relationship provenance

A visible graph edge should be traceable to evidence in the canonical knowledge layer.

Connection states:

- confirmed
- inferred
- candidate
- rejected
- reopened

Only meaningful accepted relationships should shape the normal lore graph. Candidate/rejected review state may be surfaced in Review Queue instead of cluttering the primary graph.

## Global vs local graph

The global graph is for the shape of the entire OSF knowledge base.

The local graph is especially valuable while reading a single Episode or Entity because it can show that note's immediate neighborhood without the full 125-episode corpus.
