from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal


CaptionKind = Literal["manual", "automatic"]


@dataclass(frozen=True)
class EpisodeRef:
    number: int
    video_id: str
    title: str | None = None

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"


@dataclass(frozen=True)
class CaptionSource:
    kind: CaptionKind
    language: str
    ext: str
    content: str


@dataclass(frozen=True)
class AcquiredSource:
    title: str
    video_id: str
    url: str
    description: str
    published: str | None
    duration_seconds: int | None
    info: dict[str, Any]
    captions: tuple[CaptionSource, ...]
    thumbnail: bytes
    thumbnail_ext: str


@dataclass(frozen=True)
class SourceSnapshot:
    episode: EpisodeRef
    title: str
    description: str
    published: str | None
    duration_seconds: int | None
    info: dict[str, Any]
    captions: tuple[CaptionSource, ...]
    thumbnail: bytes
    thumbnail_ext: str
    url: str


@dataclass(frozen=True)
class ExplicitReference:
    raw_text: str
    osf_number: int


@dataclass(frozen=True)
class ParsedSource:
    snapshot: SourceSnapshot
    description: str
    explicit_references: tuple[ExplicitReference, ...]
    incident_labels: tuple[str, ...]
    structured_labels: tuple[str, ...] = ()


@dataclass(frozen=True)
class EpisodeIdentity:
    number: int
    title: str
    video_id: str
    note_name: str


@dataclass(frozen=True)
class EntityIdentity:
    canonical_name: str
    episode_number: int


@dataclass(frozen=True)
class Connection:
    source_episode_number: int
    target_episode: EpisodeIdentity
    status: Literal["confirmed", "candidate", "inferred", "rejected", "reopened"]
    evidence_text: str


@dataclass(frozen=True)
class KnowledgeUpdate:
    primary_entity: EntityIdentity
    connections: tuple[Connection, ...]


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    errors: tuple[str, ...]


@dataclass(frozen=True)
class ArchivedRevision:
    revision_name: str
    revision_dir: Path
    thumbnail_name: str
    fingerprint: str
    created: bool


@dataclass(frozen=True)
class IngestResult:
    episode: EpisodeIdentity
    revision: ArchivedRevision | None
    validation: ValidationReport
    error: str | None = None
