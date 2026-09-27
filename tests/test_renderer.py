from __future__ import annotations

from pathlib import Path

from osf_atlas.models import (
    CaptionSource,
    Connection,
    EntityIdentity,
    EpisodeIdentity,
    EpisodeRef,
    ExplicitReference,
    KnowledgeUpdate,
    ParsedSource,
    SourceSnapshot,
)
from osf_atlas.renderer import Renderer


def test_renderer_rebuild_preserves_human_owned_state_and_notes(tmp_path: Path) -> None:
    vault = tmp_path
    (vault / "01 Episodes").mkdir()
    (vault / "02 Entities" / "Places").mkdir(parents=True)
    (vault / "05 Sources" / "114").mkdir(parents=True)
    (vault / "06 Assets" / "Thumbnails").mkdir(parents=True)

    episode_path = vault / "01 Episodes" / "OSF 114 - The Veiled Monolith Interior.md"
    episode_path.write_text(
        """---
type: episode
osf_number: 114
favorite: true
rating: 9
status: complete
last_read: 2026-09-25T22:10:00-06:00
ingestion_status: pending
---

# 114 // old title

<!-- OSF:GENERATED:START -->
old generated text
<!-- OSF:GENERATED:END -->

## My Notes

<!-- OSF:HUMAN:START -->

This place feels tied to the bigger network.

<!-- OSF:HUMAN:END -->
""",
        encoding="utf-8",
    )

    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=114, video_id="vid114"),
        title="114 // The Veiled Monolith: Interior - 1 Hour Ambient Soundfield",
        description="Terminal OSF-053 remains reachable.",
        published="2026-01-01",
        duration_seconds=3600,
        info={"id": "vid114"},
        captions=(
            CaptionSource("automatic", "en-orig", "vtt", "WEBVTT\n\nauto caption"),
        ),
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
    target = EpisodeIdentity(53, "Terminal", "vid053", "OSF 053 - Terminal")
    knowledge = KnowledgeUpdate(
        primary_entity=EntityIdentity("The Veiled Monolith: Interior", 114),
        connections=(
            Connection(114, target, "confirmed", "Terminal OSF-053"),
        ),
    )
    current = EpisodeIdentity(
        114,
        "The Veiled Monolith: Interior",
        "vid114",
        "OSF 114 - The Veiled Monolith Interior",
    )

    Renderer(vault).render_episode(
        identity=current,
        parsed=parsed,
        knowledge=knowledge,
        source_revision="2026-09-25_05-43-00Z",
        thumbnail_name="114.webp",
    )

    rendered = episode_path.read_text(encoding="utf-8")
    assert "favorite: true" in rendered
    assert "rating: 9" in rendered
    assert "status: complete" in rendered
    assert "last_read: 2026-09-25T22:10:00-06:00" in rendered
    assert "This place feels tied to the bigger network." in rendered
    assert "[[OSF 053 - Terminal|Terminal OSF-053]]" in (
        vault / "05 Sources" / "114" / "source.md"
    ).read_text(encoding="utf-8")
    assert "> [!abstract]- English Automatic Captions" in (
        vault / "05 Sources" / "114" / "source.md"
    ).read_text(encoding="utf-8")
    assert "[[The Veiled Monolith: Interior]]" in rendered
    assert "[[OSF 053 - Terminal]]" in rendered
