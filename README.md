# OSF Atlas

A local-first Obsidian atlas for **OBSIDIAN SOUNDFIELDS (OSF)**.

The short version:

> OSF publishes the world. The collector preserves the clues. The parser points at interesting things. **You decide what they mean.**

This project is meant for discovering the lore while listening to the soundfields and looking at the art — not for having an AI explain the whole universe in advance.

## The idea, like I'm five

Imagine OSF is a box of 125 illustrated story cards.

Each numbered YouTube release is one **Episode**:

```text
014 // The Veiled Monolith
018 // Phantom Port
028 // Obscura Highrise
...
```

The Episode has art, ambience, and a description containing lore.

OSF Atlas keeps the Episode, preserves the source locally, and starts noticing clues.

If Episode 018 mentions **Veiled Monolith**, the Atlas does **not** say:

> "These are definitely part of the same storyline."

It says:

> "Hey, 018 mentioned the name of 014. Maybe look at this."

That becomes a **Candidate Connection**.

If you read both and decide the relationship matters, you can confirm it, keep it as an interpretation, or reject it.

After enough of those discoveries, a larger story may start to emerge. That is a **Lore Thread**.

```text
OSF Episode
    │
    │ talks about
    ▼
Entity
    │
    │ may connect to
    ▼
other Entities / Episodes
    │
    │ after evidence + review
    ▼
Connections
    │
    │ several meaningful connections
    ▼
Lore Thread
```

The important part is that the arrows are not all created automatically.

## Episode vs Entity

These sound similar at first, but they answer different questions.

### Episode

An **Episode** is the actual numbered OSF release.

```text
OSF 018 // Phantom Port
```

It represents the YouTube entry and its local reading page.

An Episode can have:

- YouTube metadata;
- a local thumbnail;
- preserved source material;
- reading progress;
- favorite/rating state;
- detected references;
- your notes.

### Entity

An **Entity** is a named thing that appears to exist inside the OSF world.

That might eventually be a:

- place;
- person;
- organization;
- system;
- phenomenon;
- or something we have not classified yet.

For example:

```text
Episode: OSF 018 // Phantom Port

Primary subject:
Phantom Port
    │
    └── Entity, currently unclassified until evidence/review says what it is
```

The collector does **not** get to decide that every title is a place.

New primary Entities start as:

```yaml
entity_type: unknown
review_status: unclassified
```

Later, evidence or human review can classify them.

This distinction becomes useful when another Episode mentions the same thing:

```text
OSF 018 ─────► Phantom Port ◄───── OSF 028
  describes                         mentions
```

Now the graph can represent *what* connects the Episodes instead of merely drawing a mysterious line between two video numbers.

## Connections: how sure are we?

Not every clue deserves the same confidence.

### Confirmed

The source makes the reference explicit enough that resolving it does not require a lore theory.

Example shape:

```text
Terminal (OSF-053)
```

The OSF number is explicit, so the Atlas can resolve the target deterministically.

### Candidate

The machine found a concrete clue worth reviewing, but it should not become canon automatically.

Current rule:

```text
exact canonical Episode title/name mentioned
        ↓
candidate
```

Real examples discovered during ingestion:

```text
014 // The Veiled Monolith
          ▲
          │ candidate
018 // Phantom Port
          ▲
          │ candidate
028 // Obscura Highrise
```

018 mentions **Veiled Monolith**.

028 mentions **Phantom Port**.

That is interesting enough to surface for review, but the parser does not claim a deeper relationship.

### Inferred

A relationship that makes sense after interpretation, but is not directly stated by the source.

This is where reading, context, visual clues, chronology, and your own reasoning can matter.

An inference must remain visibly different from a confirmed fact.

### Rejected

A candidate was reviewed and does not hold up.

We keep that decision so the parser does not keep asking the same question forever.

### Reopened

A rejected connection can become interesting again when later Episodes provide new evidence.

Lore discovery is allowed to change your mind.

## What the parser is allowed to do

The parser is intentionally boring.

It can detect things such as:

- explicit `OSF-053` references;
- exact canonical title mentions;
- structured labels such as an Incident Log;
- deterministic title variants.

It can say:

> "This looks worth reviewing."

It cannot say:

> "I have solved the lore."

It does not automatically create relationships from fuzzy semantic similarity, vibes, similar architecture, similar colors, or an LLM's confidence.

In other words:

```text
parser = clue detector
parser ≠ lore authority
```

## What is a Lore Thread?

A **Lore Thread** is not a tag and it is not an AI-generated summary.

It is a narrative path that becomes useful after multiple discoveries connect.

Imagine that, while reading, you eventually confirm or infer several related clues:

```text
Episode A ──► Entity X
                │
Episode B ──────┤
                │
Episode C ──► Entity Y
                │
                └── related evidence
```

At some point you may realize:

> "Wait. These all seem to be part of the same ongoing thing."

That is when a Lore Thread deserves to exist.

So a Lore Thread is closer to a **research trail of what has been discovered and connected** than a pre-written wiki article.

It can contain:

- Episodes involved;
- Entities involved;
- confirmed evidence;
- interpretations;
- rejected ideas;
- open questions;
- your notes.

## Where my notes fit

Your notes are a separate layer.

You might listen to an Episode and tell the agent:

> "I don't think Argus is malfunctioning. It feels like it is following its protection directive too literally."

The agentic `osf-vault` skill should treat that as **your interpretation**.

It may connect the note to the relevant Episode or Entity, but it must not rewrite the source or silently promote the idea to canon.

```text
OSF source ───────────────► evidence
                               │
                               ▼
                         knowledge graph
                               ▲
                               │
your notes / theories ─────────┘
```

Both can live in the same graph without pretending they have the same authority.

## The layers

The project deliberately separates five kinds of information.

### 1. Raw Source — what OSF actually exposed

The exact locally extracted description/captions and acquisition metadata.

This is archival truth. It is not cleaned, rewritten, summarized, or annotated.

### 2. Reader Source — source made comfortable to read

A generated Markdown projection for Obsidian.

It can eventually contain safe annotations for already-confirmed links, while Raw Source stays unchanged.

### 3. Knowledge — what we have resolved

Entities, connection states, evidence, and review decisions.

Every relationship should be explainable by provenance instead of "trust me bro."

### 4. Obsidian View — how you explore it

Episode Notes, Entities, Bases, Graph, Review Queue, Favorites, reading progress, and Lore Threads.

### 5. My Notes — what *you* think

Opinions, theories, observations, questions, favorites, ratings, and reading history.

Automation must preserve this layer.

## How discovery works

The intended loop is:

```text
1. Collect Episode
        ↓
2. Preserve source locally
        ↓
3. Detect small structural clues
        ↓
4. Surface candidates
        ↓
5. Read / listen / inspect
        ↓
6. Human or agent-assisted review
        ↓
7. Confirm / infer / reject
        ↓
8. Repeated discoveries begin forming Lore Threads
```

The goal is not to reach step 8 as quickly as possible.

The goal is to make every step trustworthy enough that the graph becomes more useful as the vault grows.

## Why batches of ten?

The corpus is ingested chronologically in batches of ten.

After every batch we stop and ask:

- Was every source preserved?
- Did YouTube expose captions?
- Did the parser encounter a new reference format?
- Did it create false positives?
- Did new candidates appear?
- Does the data model still make sense?

This has already changed the project in useful ways.

For example, Batch 011–020 taught the resolver to surface exact canonical-name mentions as **candidates**, not confirmed lore.

## Current progress

Corpus ingestion is intentionally paused while this knowledge model is reviewed.

```text
001–010  complete
011–020  complete
021–030  complete
031–125  paused
```

Current automated gates:

```text
30/30 ingested Episodes validate
10/10 tests pass
0 failed extractions
```

## Project structure

```text
00 Atlas/                 home, Bases, review and navigation
01 Episodes/              one note per numbered OSF release
02 Entities/
├── Unclassified/         primary subjects waiting for semantic review
├── Places/
├── People/
├── Organizations/
├── Systems/
└── Phenomena/
03 Lore Threads/          narrative trails discovered across the graph
04 My Notes/              human-owned research, opinions and theories
05 Sources/               local generated Reader Source + raw revisions
06 Assets/                local thumbnails and vault assets
90 Templates/             Obsidian note templates
tools/osf/                collector/parser/renderer/validator
tests/                    behavioral TDD suite
.osf/                     canonical machine state and review decisions
docs/                     architecture, ADRs and implementation notes
```

## Collector

The collector uses `yt-dlp` as an acquisition adapter and intentionally downloads **no video and no audio**.

For each Episode it can preserve locally:

- full description;
- metadata;
- highest available thumbnail;
- original English captions when available;
- hashes and a manifest.

Then the pipeline runs:

```text
Acquire
  → Preserve
  → StructuralParser
  → KnowledgeResolver
  → Renderer
  → Validator
```

Run the tests:

```bash
.venv/bin/python -m pytest -q tests
```

Ingest a batch:

```bash
.venv/bin/osf --vault . ingest 031-040
```

Check a range without ingesting:

```bash
.venv/bin/osf --vault . check 001-030
```

## Public repo vs local vault

The GitHub repository contains the **Atlas system and derived project structure**, not a redistribution mirror of OBSIDIAN SOUNDFIELDS.

The following stay local and are regenerated by the collector:

- complete Raw Source revisions;
- generated Reader Source containing complete upstream descriptions/captions;
- downloaded thumbnails.

The public repository can still contain Episode metadata, knowledge state, short evidence needed to explain a decision, code, tests, templates, and personal/project documentation.

This keeps the project useful as an open tool while the personal vault remains the full research archive.

## Source ownership and license

OBSIDIAN SOUNDFIELDS media, artwork, descriptions, names, and other upstream creative material belong to their respective creator/rightsholders. This repository is an independent personal research/organization tool and is not an official OSF project.

The repository's own code and documentation are released under the included **GPL-3.0** license. The GPL does not grant rights to third-party OSF material.

## Design rule

If there is one rule to remember, it is this:

> **Preserve first. Detect second. Interpret carefully. Let the human discover the lore.**
