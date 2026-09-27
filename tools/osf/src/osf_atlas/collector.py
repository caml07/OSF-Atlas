from __future__ import annotations

from typing import Protocol

from .models import AcquiredSource, EpisodeRef, SourceSnapshot


class AcquisitionAdapter(Protocol):
    def acquire(self, episode: EpisodeRef) -> AcquiredSource: ...


class Collector:
    """Acquire one Episode while preserving source payloads exactly."""

    def __init__(self, adapter: AcquisitionAdapter) -> None:
        self._adapter = adapter

    def collect(self, episode: EpisodeRef) -> SourceSnapshot:
        acquired = self._adapter.acquire(episode)
        return SourceSnapshot(
            episode=episode,
            title=acquired.title,
            description=acquired.description,
            published=acquired.published,
            duration_seconds=acquired.duration_seconds,
            info=acquired.info,
            captions=acquired.captions,
            thumbnail=acquired.thumbnail,
            thumbnail_ext=acquired.thumbnail_ext,
            url=acquired.url,
        )
