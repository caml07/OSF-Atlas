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

The machine does **not** promote that Entity into a semantic type later just because more corpus text was ingested. Classification happens when **you read the material and make the call**.

For example, while reading you might say:

> "They keep talking about this thing called Argus. It sounds like an AI/system."

That is the moment the Entity can move from:

```text
02 Entities/Unclassified/Argus.md
```

to something like:

```text
02 Entities/Systems/Argus.md
```

and its properties can become:

```yaml
entity_type: system
review_status: human-reviewed
```

The important distinction is that **Argus never stops being an Entity**. `System` is its human-reviewed classification, not a different domain object. The same applies to `Place`, `Person`, `Organization`, and `Phenomenon`.

If the source is still unclear, there is no pressure to classify it. `unknown` is a valid state for as long as necessary.

This distinction becomes useful when another Episode mentions the same thing:

```text
OSF 018 ─────► Phantom Port ◄───── OSF 028
  describes                         mentions
```

Now the graph can represent *what* connects the Episodes instead of merely drawing a mysterious line between two video numbers.

## The human discovery contract

This is the central rule of OSF Atlas.

**Ingestion discovers material. You discover meaning.**

The system may prepare an Episode, preserve its source, create an unclassified primary Entity, and surface small deterministic clues. It must stop before semantic interpretation becomes authoritative.

A normal discovery session should feel closer to this:

```text
You open OSF 029.
        │
        ▼
You listen / look at the artwork / read the source.
        │
        ▼
"Wait, who or what is Argus?"
        │
        ▼
You notice the text describes Argus like an AI.
        │
        ▼
You tell the agent:
"Argus seems to be a system / AI."
        │
        ▼
The agent records the Entity classification + evidence.
        │
        ▼
Later you find Argus somewhere else.
        │
        ▼
"OHH, this connects back to 029."
        │
        ▼
A reviewed Connection is recorded.
        │
        ▼
After several discoveries:
"These connections look like one larger thread."
        │
        ▼
You create / name a Lore Thread.
```

The agent is there to keep the notebook organized while you do the discovering.

### What happens when I say something?

| What you notice while reading | What the Atlas should do | What it must **not** do |
| --- | --- | --- |
| "This thing has a name." | Create or link an Entity if it has independent identity. | Invent a semantic type. |
| "This seems like a place." | Classify the Entity as `place`, record that this was human-reviewed, and move it to `Places/`. | Pretend the source explicitly called it a place if it did not. |
| "This sounds like an AI/system." | Classify it as `system` with the relevant evidence/reading context. | Generate extra capabilities or backstory. |
| "They mention X here." | Link the mention/evidence and surface the existing Entity/Episode. | Claim the mention proves a larger relationship. |
| "This seems connected to X." | Record an `inferred` Connection with your reasoning/evidence. | Promote it to `confirmed`. |
| "The source literally says this is X / points to OSF-053." | Record a `confirmed` Connection with the exact evidence. | Replace the Raw Source with an annotated version. |
| "Nah, I don't think these are connected." | Mark the candidate `rejected` and keep the decision. | Delete the history and ask again next rebuild. |
| "Wait, later lore makes that rejected idea make sense." | `reopen` the decision for review. | Erase the earlier rejection. |
| "These discoveries are all part of the same thing." | Start or extend a Lore Thread. | Auto-generate a storyline before you make that connection. |
| "I think X means Y." | Save it as your note/theory and link relevant nodes. | Present your theory as OSF canon. |

### Classification belongs to the reader

There is deliberately no automatic pipeline like:

```text
Entity → LLM guesses type → Place/System/Person
```

The intended pipeline is:

```text
Entity: unknown
      │
      │ you read the Episode
      ▼
"this seems like a place"
      │
      │ human-reviewed classification
      ▼
Entity: place
```

This matters because names in OSF can be ambiguous. A title that sounds like a building could be a machine, a project, an event, or something stranger. Keeping it `unknown` costs almost nothing; confidently classifying it wrong pollutes the graph.

### Connections belong to evidence + interpretation

Classification and connection are separate decisions.

You may discover:

```text
Entity A = place
Entity B = system
```

without knowing whether they are related.

Later, while reading, you may say:

> "This place seems to be controlled by that system from the other Episode."

If that is your interpretation rather than an explicit statement, the Atlas records an **Inferred Connection** and keeps your reasoning beside it. If the source explicitly establishes the relationship, it can become **Confirmed**.

The graph therefore records not only *what connects*, but also **why we believe it connects**.

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

### A Lore Thread is something *you notice*

The Atlas should never create a Lore Thread merely because several nodes are mathematically close in the Obsidian Graph. A dense cluster can be a useful hint, but it is not a story by itself.

A thread begins when your reading reaches a moment like:

> "Hold on. The thing from 014 gets mentioned in 018, Phantom Port gets mentioned again in 028, and what I just read changes how I understand those earlier Episodes. I want to follow this."

At that point the thread can preserve the path you took:

```text
first clue
   ↓
what I thought at the time
   ↓
second clue
   ↓
connection I accepted / inferred / rejected
   ↓
new evidence from a later Episode
   ↓
what changed in my understanding
```

That makes a Lore Thread useful even if your interpretation changes later. It is a record of discovery, not a frozen encyclopedia answer.

### Example: the first tiny chain we found

So far the parser has surfaced this review path:

```text
014 // The Veiled Monolith
          ▲
          │ candidate mention
018 // Phantom Port
          ▲
          │ candidate mention
028 // Obscura Highrise
```

What does that mean? Very little **so far**.

It means 018 contains the name `Veiled Monolith`, and 028 contains the name `Phantom Port`. That is enough to put two cards on the investigation board. It is not enough to write a Lore Thread claiming that all three share one plot.

When you eventually read them, you may decide:

- the mentions are important and form part of a larger thread;
- one is important and the other is incidental;
- both are merely references;
- a later Episode completely changes the interpretation.

The vault is designed to preserve whichever path the evidence and your reading actually support.

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

### What the agentic skill is for

The `osf-vault` skill is the bridge between casual discovery and structured notes. You should be able to talk to it naturally instead of filling forms.

Examples:

> "I think this Argus thing is an AI or some kind of system."

Expected behavior: find/create `Argus`, classify it only because **you just made that reading judgment**, link the Episode/evidence, preserve your wording where useful, and leave unrelated lore untouched.

> "This place reminds me of Phantom Port, but I'm not sure they're actually connected."

Expected behavior: preserve the observation as a theory/candidate-style research note. Do not manufacture a confirmed relationship.

> "Yeah, after reading this, I'm convinced this connects to Phantom Port because of X."

Expected behavior: record an inferred connection with your reasoning unless the source itself explicitly establishes it.

> "This literally says Terminal (OSF-053)."

Expected behavior: attach the explicit evidence and allow a confirmed connection.

> "These three things feel like the same storyline. Let's call it ___ for now."

Expected behavior: create an emerging Lore Thread containing the discoveries you selected, their evidence states, and your open questions.

The skill should organize **your research process**. It should not impersonate a lore expert.

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

Corpus ingestion continues under the human-owned semantic model described above.

```text
001–010  complete
011–020  complete
021–030  complete
031–040  complete
041–050  complete
051–060  complete
061–070  complete
071–080  complete
081–090  complete
091–100  complete
101–110  complete
111–125  pending
```

Current automated gates:

```text
110/110 ingested Episodes validate
14/14 tests pass
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
