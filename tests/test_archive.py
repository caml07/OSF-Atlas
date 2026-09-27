from __future__ import annotations

from pathlib import Path

from osf_atlas.archive import SourceArchive
from osf_atlas.models import EpisodeRef, SourceSnapshot


def test_successful_preserve_moves_prior_failure_record_to_resolved(tmp_path: Path) -> None:
    failure_dir = tmp_path / ".osf" / "failures"
    failure_dir.mkdir(parents=True)
    prior = failure_dir / "2026-09-27_00-00-00Z-069.json"
    prior.write_text('{"episode": 69}\n', encoding="utf-8")

    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=69, video_id="vid069"),
        title="069 // Final Shore",
        description="exact\r\nsource\n",
        published=None,
        duration_seconds=3600,
        info={"id": "vid069", "description": "exact\r\nsource\n"},
        captions=(),
        thumbnail=b"thumb",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid069",
    )

    SourceArchive(tmp_path).preserve(snapshot)

    assert not prior.exists()
    assert (
        failure_dir
        / "resolved"
        / "2026-09-27_00-00-00Z-069.json"
    ).exists()
