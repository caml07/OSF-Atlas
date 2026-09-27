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


def test_validator_compares_exact_utf8_bytes_without_normalizing_line_endings(tmp_path: Path) -> None:
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=69, video_id="vid069"),
        title="069 // Final Shore",
        description="line one\r\n\nline two\n",
        published=None,
        duration_seconds=3600,
        info={},
        captions=(
            CaptionSource(
                "manual",
                "en",
                "vtt",
                "WEBVTT\r\n\r\n00:00.000 --> 00:01.000\r\nhello\r\n",
            ),
        ),
        thumbnail=b"thumb",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid069",
    )
    revision = tmp_path / "revision"
    revision.mkdir()
    (revision / "description.txt").write_bytes(snapshot.description.encode("utf-8"))
    (revision / "captions.manual.en.vtt").write_bytes(
        snapshot.captions[0].content.encode("utf-8")
    )
    (revision / "thumbnail.webp").write_bytes(snapshot.thumbnail)

    report = Validator().validate_source(snapshot, revision)

    assert report.ok
    assert report.errors == ()
