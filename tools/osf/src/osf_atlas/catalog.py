from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Iterable

from .models import EpisodeIdentity, EpisodeRef


_TITLE_RE = re.compile(r"^(?P<number>\d{3})\s*//\s*(?P<title>.+?)\s+-\s+.+$")
_FORBIDDEN_NOTE_CHARS = re.compile(r'[\\/:*?"<>|#^\[\]]+')


def _safe_note_title(title: str) -> str:
    cleaned = _FORBIDDEN_NOTE_CHARS.sub("", title)
    return re.sub(r"\s+", " ", cleaned).strip()


def identity_from_playlist_entry(entry: dict) -> EpisodeIdentity | None:
    full_title = entry.get("title") or ""
    match = _TITLE_RE.match(full_title)
    if not match:
        return None

    number = int(match.group("number"))
    title = match.group("title").strip()
    video_id = str(entry.get("id") or "").strip()
    if not video_id:
        return None

    note_title = _safe_note_title(title)
    return EpisodeIdentity(
        number=number,
        title=title,
        video_id=video_id,
        note_name=f"OSF {number:03d} - {note_title}",
    )


def discover_catalog(
    channel_url: str = "https://www.youtube.com/@OBSIDIANSOUNDFIELDS/videos",
) -> dict[int, EpisodeIdentity]:
    proc = subprocess.run(
        ["yt-dlp", "--flat-playlist", "-J", channel_url],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(proc.stdout)
    identities = [
        identity
        for entry in payload.get("entries", [])
        if (identity := identity_from_playlist_entry(entry)) is not None
    ]
    return {identity.number: identity for identity in sorted(identities, key=lambda item: item.number)}


def refs_for_range(
    catalog: dict[int, EpisodeIdentity],
    start: int,
    end: int,
) -> tuple[EpisodeRef, ...]:
    missing = [number for number in range(start, end + 1) if number not in catalog]
    if missing:
        missing_text = ", ".join(f"{number:03d}" for number in missing)
        raise KeyError(f"Missing Episodes from catalog: {missing_text}")
    return tuple(
        EpisodeRef(
            number=number,
            video_id=catalog[number].video_id,
            title=catalog[number].title,
        )
        for number in range(start, end + 1)
    )


def parse_range(value: str) -> tuple[int, int]:
    raw = value.strip()
    if "-" in raw:
        left, right = raw.split("-", 1)
        start, end = int(left), int(right)
    else:
        start = end = int(raw)
    if start < 1 or end < start:
        raise ValueError(f"Invalid Episode range: {value}")
    return start, end
