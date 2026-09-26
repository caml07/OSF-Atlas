# Vault Agent Skill

Status: initial skill implemented as `osf-vault` in the user's CamSkills collection

## Intent

Provide an OpenCode/Codex-compatible agent skill that understands the OSF Atlas domain rather than treating every Markdown file as a generic note.

The skill should let agentic research create useful notes anywhere in the vault while preserving the distinction between Episodes, Entities, Lore Threads, Raw/Reader Sources, and personal research notes.

## Required domain awareness

The skill must understand at least:

- Episode ≠ Entity
- Reader Source ≠ Raw Source
- Confirmed ≠ Inferred ≠ Candidate
- machine-owned ≠ human-owned
- a personal research note can link any combination of Episodes, Entities, and Lore Threads without being forced into an Episode file

## Capabilities

Examples to explore later:

- “Take notes about what I'm reading in 114.”
- “Create a theory note connecting these three Entities.”
- “Mark this candidate as confirmed/inferred/rejected.”
- “I finished reading 090.”
- “This reference actually matches Terminal; reopen/confirm it.”
- “Show me everything related to this Entity.”
- “Capture this thought but don't classify it as canon.”

The skill does not force personal thoughts into rigid opinion/theory/question
categories. A standalone thought is normally captured as a flexible
`type: research-note` under `04 My Notes/Research/`, preserving the user's
Spanish/English/Spanglish voice and linking any relevant Episodes, Entities, or
Lore Threads.

Short notes explicitly intended for one Episode may still live inside that
Episode's `My Notes` area.

## Human-owned reading state

The skill may update:

- `favorite: true|false`
- `rating: 1..10`
- `status: unread|reading|complete`
- `last_read`

It refreshes `last_read` during explicit agentic reading/review and when the
user says they finished an Episode. A factual lookup by itself does not count as
reading.

## Safety/invariants

The skill must never:

- modify Raw Source;
- silently upgrade an inferred relationship to confirmed;
- collapse Episode and Entity into one note;
- overwrite personal prose while regenerating machine-owned sections;
- create low-value Entity nodes for every noun.

## Git behavior

The vault remains a local Git repository even while public hosting is out of
scope.

After successfully capturing or updating human-owned notes/state, `osf-vault`
may create a local commit automatically. It stages only exact paths from the
current note task, skips auto-commit when a touched path was already dirty before
the task, and never pushes unless the user explicitly asks.

## Boundary with ingestion

`osf-vault` remains strictly a knowledge/note-taking layer. It does not call
`yt-dlp`, run `osf ingest`, or mutate Raw Source. The collector/parser remains
the ingestion authority.

Rejected/reopened Connection Decisions are handled through the implemented
knowledge schema when available. Until that schema exists, the skill records the
user's interpretation in a Research Note rather than inventing storage.
