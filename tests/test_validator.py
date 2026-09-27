from __future__ import annotations

from pathlib import Path

from osf_atlas.models import CaptionSource, EpisodeRef, SourceSnapshot
from osf_atlas.validator import Validator


def test_validator_rejects_revision_when_expected_caption_is_missing(tmp_path: Path) -> None:
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=1, video_id="vid001"),
        title="001 // Iron Haven",
        description="exact description\n",
        published=None,
        duration_seconds=3600,
        info={},
        captions=(
            CaptionSource("manual", "en", "vtt", "WEBVTT\n\nmanual"),
        ),
        thumbnail=b"thumb",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid001",
    )
    revision = tmp_path / "revision"
    revision.mkdir()
    (revision / "description.txt").write_text(snapshot.description, encoding="utf-8")
    (revision / "thumbnail.webp").write_bytes(snapshot.thumbnail)

    missing = Validator().validate_source(snapshot, revision)

    assert not missing.ok
    assert "captions.manual.en.vtt" in missing.errors

    (revision / "captions.manual.en.vtt").write_text(
        snapshot.captions[0].content,
        encoding="utf-8",
    )
    complete = Validator().validate_source(snapshot, revision)

    assert complete.ok
    assert complete.errors == ()
