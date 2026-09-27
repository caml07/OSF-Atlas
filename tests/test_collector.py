from __future__ import annotations

from dataclasses import dataclass

from osf_atlas.collector import Collector
from osf_atlas.models import AcquiredSource, CaptionSource, EpisodeRef


@dataclass
class FakeAdapter:
    payload: AcquiredSource

    def acquire(self, episode: EpisodeRef) -> AcquiredSource:
        assert episode.number == 1
        return self.payload


def test_collector_preserves_exact_description_and_original_english_tracks() -> None:
    description = "Line one.\n\nTerminal text — kept exactly.\n"
    thumbnail = b"\x00WEBP\xff"

    payload = AcquiredSource(
        title="001 // Iron Haven - 1 Hour Industrial Ambient Soundfield",
        video_id="video001",
        url="https://www.youtube.com/watch?v=video001",
        description=description,
        published="2024-03-22",
        duration_seconds=3600,
        info={"id": "video001", "view_count": 999},
        captions=(
            CaptionSource(kind="manual", language="en", ext="vtt", content="WEBVTT\n\nmanual"),
            CaptionSource(kind="automatic", language="en-orig", ext="vtt", content="WEBVTT\n\nauto"),
        ),
        thumbnail=thumbnail,
        thumbnail_ext="webp",
    )

    collector = Collector(FakeAdapter(payload))
    result = collector.collect(EpisodeRef(number=1, video_id="video001"))

    assert result.description == description
    assert result.thumbnail == thumbnail
    assert [(c.kind, c.language, c.content) for c in result.captions] == [
        ("manual", "en", "WEBVTT\n\nmanual"),
        ("automatic", "en-orig", "WEBVTT\n\nauto"),
    ]
