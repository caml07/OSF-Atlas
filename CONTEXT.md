# Obsidian Soundfields Atlas

A local knowledge-vault project for preserving, reading, and connecting the numbered Obsidian Soundfields series as a navigable lore graph.

## Language

**Episode**:
One numbered Obsidian Soundfields video and its corresponding vault note.
_Avoid_: Entry, item, record

**Location Record**:
The narrative/lore material associated with an Episode, usually exposed in the video's description and sometimes supplemented by captions.
_Avoid_: Transcript when referring only to the description

**Raw Source**:
An unmodified local snapshot of source material retrieved for an Episode before any parsing or interpretation.
_Avoid_: Parsed text, cleaned text

**Source Revision**:
A preserved version of an Episode's Raw Source captured at a specific retrieval time. New upstream text creates a new revision instead of replacing an older one.
_Avoid_: Overwrite, latest-only copy

**Reader Source**:
A generated Markdown projection of a Source Revision for comfortable reading in Obsidian. It may add safe wiki-link annotations, but the Raw Source remains the authority for exact wording and characters.
_Avoid_: Raw Source, canonical source

**Episode Note**:
The Markdown note used for reading an Episode inside Obsidian. It presents source material, metadata, links, and derived lore structure.
_Avoid_: Raw Source

**Entity**:
A named thing with independent identity inside OSF lore, such as a place, organization, system, phenomenon, or person, that deserves its own graph node. A primary Episode subject may be seeded as an unclassified Entity, but its semantic type must not be guessed automatically.
_Avoid_: Tag when the concept has independent lore identity

**Lore Thread**:
A research trail representing a recurring narrative relationship discovered across multiple Episodes or Entities. It should emerge from reviewed evidence/connections rather than being generated as an authoritative storyline in advance.
_Avoid_: Category, topic

**Confirmed Connection**:
A relationship between Episodes or Entities explicitly supported by OSF source material.
_Avoid_: Theory

**Candidate Connection**:
A concrete machine-detected clue worth reviewing that has not yet been accepted as either Confirmed or Inferred. Exact canonical Episode-name mentions may become candidates; fuzzy semantic similarity must not.
_Avoid_: Confirmed Connection

**Connection Decision**:
A persisted review outcome for a Candidate Connection: confirmed, inferred, rejected, or reopened for review.
_Avoid_: Ephemeral parser result

**Inferred Connection**:
A relationship suggested by interpretation, naming, visuals, chronology, or other indirect evidence but not explicitly established by OSF material.
_Avoid_: Confirmed Connection

**Batch**:
A chronological ingestion unit of up to ten Episodes used to research, verify, parse, and integrate the series incrementally.
_Avoid_: Release

**Ingestion Status**:
The archival state of an Episode or Batch: whether retrieval, preservation, rendering, and validation completed successfully.
_Avoid_: Lore review status

**Lore Review Status**:
The review state of semantic relationships and Candidate Connections after ingestion is already valid.
_Avoid_: Ingestion status

**Failed Extraction**:
A retrieval attempt that did not produce a complete promotable Source Revision. It is recorded for diagnosis while the last valid revision remains current.
_Avoid_: Partial revision

**Source Coverage**:
The known availability and extraction state of Raw Source material for an Episode.
_Avoid_: Reading status

**Reading Status**:
The user's personal progress through an Episode Note.
_Avoid_: Source Coverage

**Machine-Owned Content**:
Derived or retrieved material that the collector may regenerate, such as metadata, source embeds, thumbnails, and generated analysis.
_Avoid_: Personal notes

**Human-Owned Content**:
User-authored state that automation must preserve, including favorites, reading progress, personal notes, theories, and manually reviewed relationship decisions.
_Avoid_: Generated content
