from __future__ import annotations

from osf_atlas.knowledge import KnowledgeResolver
from osf_atlas.models import (
    EpisodeIdentity,
    EpisodeRef,
    ExplicitReference,
    ParsedSource,
    SourceSnapshot,
)


def test_resolver_confirms_numbered_reference_and_keeps_primary_entity_separate() -> None:
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=114, video_id="vid114"),
        title="114 // The Veiled Monolith: Interior - 1 Hour Ambient Soundfield",
        description="Terminal OSF-053 is explicitly referenced. A terminal remains nearby.",
        published=None,
        duration_seconds=3600,
        info={},
        captions=(),
        thumbnail=b"image",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid114",
    )
    parsed = ParsedSource(
        snapshot=snapshot,
        description=snapshot.description,
        explicit_references=(ExplicitReference("Terminal OSF-053", 53),),
        incident_labels=(),
    )
    catalog = {
        53: EpisodeIdentity(
            number=53,
            title="Terminal",
            video_id="vid053",
            note_name="OSF 053 - Terminal",
        ),
        114: EpisodeIdentity(
            number=114,
            title="The Veiled Monolith: Interior",
            video_id="vid114",
            note_name="OSF 114 - The Veiled Monolith Interior",
        ),
    }

    update = KnowledgeResolver().resolve(parsed, catalog)

    assert update.primary_entity.canonical_name == "The Veiled Monolith: Interior"
    assert update.primary_entity.episode_number == 114
    assert len(update.connections) == 1
    connection = update.connections[0]
    assert connection.status == "confirmed"
    assert connection.target_episode == catalog[53]
    assert connection.evidence_text == "Terminal OSF-053"


def test_resolver_confirms_exact_colon_title_variant_to_base_episode() -> None:
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=43, video_id="vid043"),
        title="043 // Silent Arbiter: Interior Hall - 1 Hour Ambient Soundfield",
        description="Interior observation continues.",
        published=None,
        duration_seconds=3600,
        info={},
        captions=(),
        thumbnail=b"image",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid043",
    )
    parsed = ParsedSource(
        snapshot=snapshot,
        description=snapshot.description,
        explicit_references=(),
        incident_labels=(),
    )
    catalog = {
        16: EpisodeIdentity(16, "Silent Arbiter", "vid016", "OSF 016 - Silent Arbiter"),
        43: EpisodeIdentity(
            43,
            "Silent Arbiter: Interior Hall",
            "vid043",
            "OSF 043 - Silent Arbiter Interior Hall",
        ),
    }

    update = KnowledgeResolver().resolve(parsed, catalog)

    assert len(update.connections) == 1
    assert update.connections[0].target_episode == catalog[16]
    assert update.connections[0].status == "confirmed"
    assert update.connections[0].evidence_text == "title-variant: Silent Arbiter"


def test_resolver_marks_exact_canonical_title_mention_as_candidate() -> None:
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=18, video_id="vid018"),
        title="018 // Phantom Port - Ambient",
        description=(
            "Like the legendary Veiled Monolith, it uses clandestine technology "
            "to cloak itself in mist."
        ),
        published=None,
        duration_seconds=3600,
        info={},
        captions=(),
        thumbnail=b"image",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid018",
    )
    parsed = ParsedSource(snapshot, snapshot.description, (), ())
    catalog = {
        14: EpisodeIdentity(
            14,
            "The Veiled Monolith",
            "vid014",
            "OSF 014 - The Veiled Monolith",
        ),
        18: EpisodeIdentity(18, "Phantom Port", "vid018", "OSF 018 - Phantom Port"),
    }

    update = KnowledgeResolver().resolve(parsed, catalog)

    assert len(update.connections) == 1
    connection = update.connections[0]
    assert connection.target_episode == catalog[14]
    assert connection.status == "candidate"
    assert connection.evidence_text == "Veiled Monolith"
