from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .models import AcquiredSource, CaptionSource, EpisodeRef


_ENGLISH_MANUAL = re.compile(r"^en(?:$|[-_](?:US|GB|CA|AU|NZ|IE))", re.IGNORECASE)


def _download_bytes(url: str) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read()


def _best_format(formats: list[dict]) -> dict | None:
    if not formats:
        return None
    for preferred in ("vtt", "ttml", "srv3", "json3"):
        for item in formats:
            if item.get("ext") == preferred and item.get("url"):
                return item
    return next((item for item in formats if item.get("url")), None)


def _thumbnail_ext(url: str, content_type: str | None = None) -> str:
    suffix = Path(urlparse(url).path).suffix.lower().lstrip(".")
    if suffix in {"jpg", "jpeg", "png", "webp"}:
        return "jpg" if suffix == "jpeg" else suffix
    if content_type:
        lowered = content_type.lower()
        if "webp" in lowered:
            return "webp"
        if "png" in lowered:
            return "png"
    return "jpg"


class YtDlpAdapter:
    """Acquire exact source payloads exposed by YouTube without video/audio."""

    def acquire(self, episode: EpisodeRef) -> AcquiredSource:
        proc = subprocess.run(
            ["yt-dlp", "-J", "--skip-download", episode.url],
            check=True,
            capture_output=True,
            text=True,
        )
        info = json.loads(proc.stdout)

        description = info.get("description")
        if description is None:
            raise RuntimeError(f"Episode {episode.number:03d} has no description payload")

        captions = tuple(self._english_caption_sources(info))
        thumbnail_url = self._best_thumbnail_url(info)
        if not thumbnail_url:
            raise RuntimeError(f"Episode {episode.number:03d} has no thumbnail URL")
        thumbnail = _download_bytes(thumbnail_url)
        thumbnail_ext = _thumbnail_ext(thumbnail_url)

        upload_date = info.get("upload_date")
        published = None
        if isinstance(upload_date, str) and len(upload_date) == 8:
            published = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

        duration = info.get("duration")
        duration_seconds = int(duration) if duration is not None else None

        return AcquiredSource(
            title=str(info.get("title") or episode.title or f"OSF {episode.number:03d}"),
            video_id=str(info.get("id") or episode.video_id),
            url=str(info.get("webpage_url") or episode.url),
            description=description,
            published=published,
            duration_seconds=duration_seconds,
            info=info,
            captions=captions,
            thumbnail=thumbnail,
            thumbnail_ext=thumbnail_ext,
        )

    def _english_caption_sources(self, info: dict) -> list[CaptionSource]:
        result: list[CaptionSource] = []

        subtitles = info.get("subtitles") or {}
        for language in sorted(subtitles):
            if not _ENGLISH_MANUAL.match(language):
                continue
            selected = _best_format(subtitles.get(language) or [])
            if selected is None:
                continue
            content = _download_bytes(selected["url"]).decode("utf-8")
            result.append(
                CaptionSource(
                    kind="manual",
                    language=language,
                    ext=selected.get("ext") or "vtt",
                    content=content,
                )
            )

        automatic = info.get("automatic_captions") or {}
        auto_languages: list[str] = []
        if "en-orig" in automatic:
            auto_languages = ["en-orig"]
        elif "en" in automatic and self._english_is_original(info, automatic["en"]):
            auto_languages = ["en"]

        for language in auto_languages:
            selected = _best_format(automatic.get(language) or [])
            if selected is None:
                continue
            content = _download_bytes(selected["url"]).decode("utf-8")
            result.append(
                CaptionSource(
                    kind="automatic",
                    language=language,
                    ext=selected.get("ext") or "vtt",
                    content=content,
                )
            )

        return result

    def _english_is_original(self, info: dict, formats: list[dict]) -> bool:
        language = str(info.get("language") or "").lower()
        if language.startswith("en"):
            return True
        for item in formats:
            name = str(item.get("name") or "").lower()
            if "english" in name and "original" in name:
                return True
        return False

    def _best_thumbnail_url(self, info: dict) -> str | None:
        candidates = [thumb for thumb in (info.get("thumbnails") or []) if thumb.get("url")]
        if not candidates:
            return info.get("thumbnail")

        def score(thumb: dict) -> tuple[int, int]:
            width = int(thumb.get("width") or 0)
            height = int(thumb.get("height") or 0)
            preference = int(thumb.get("preference") or 0)
            return (width * height, preference)

        return max(candidates, key=score)["url"]
