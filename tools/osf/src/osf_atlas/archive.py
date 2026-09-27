from __future__ import annotations

import hashlib
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .models import ArchivedRevision, SourceSnapshot
from .validator import Validator


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fingerprint(snapshot: SourceSnapshot) -> tuple[str, dict[str, str]]:
    artifact_hashes: dict[str, str] = {}
    artifact_hashes["description.txt"] = _sha256(snapshot.description.encode("utf-8"))
    for caption in snapshot.captions:
        name = f"captions.{caption.kind}.{caption.language}.{caption.ext}"
        artifact_hashes[name] = _sha256(caption.content.encode("utf-8"))
    thumbnail_name = f"thumbnail.{snapshot.thumbnail_ext}"
    artifact_hashes[thumbnail_name] = _sha256(snapshot.thumbnail)

    digest = hashlib.sha256()
    digest.update(snapshot.episode.video_id.encode("utf-8"))
    digest.update(b"\0")
    for name in sorted(artifact_hashes):
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(artifact_hashes[name].encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest(), artifact_hashes


class SourceArchive:
    """Persist immutable Source Revisions with staging and atomic promotion."""

    def __init__(self, vault_root: Path, validator: Validator | None = None) -> None:
        self._root = Path(vault_root)
        self._validator = validator or Validator()

    def preserve(self, snapshot: SourceSnapshot) -> ArchivedRevision:
        episode_dir = self._root / "05 Sources" / f"{snapshot.episode.number:03d}"
        revisions_dir = episode_dir / "revisions"
        revisions_dir.mkdir(parents=True, exist_ok=True)

        fingerprint, artifact_hashes = _fingerprint(snapshot)
        existing = self._find_fingerprint(revisions_dir, fingerprint)
        if existing is not None:
            thumbnail_name = self._publish_current_thumbnail(snapshot, existing)
            self._resolve_failure_records(snapshot.episode.number)
            return ArchivedRevision(
                revision_name=existing.name,
                revision_dir=existing,
                thumbnail_name=thumbnail_name,
                fingerprint=fingerprint,
                created=False,
            )

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%SZ")
        revision_name = self._unique_revision_name(revisions_dir, timestamp)
        staging = (
            self._root
            / ".osf"
            / "staging"
            / f"{snapshot.episode.number:03d}-{uuid.uuid4().hex[:10]}"
        )
        staging.mkdir(parents=True, exist_ok=False)

        try:
            self._write_snapshot(
                snapshot=snapshot,
                directory=staging,
                revision_name=revision_name,
                fingerprint=fingerprint,
                artifact_hashes=artifact_hashes,
            )
            validation = self._validator.validate_source(snapshot, staging)
            if not validation.ok:
                self._record_failure(
                    snapshot,
                    f"Source validation failed: {', '.join(validation.errors)}",
                    staging,
                )
                raise RuntimeError(
                    f"Source validation failed for {snapshot.episode.number:03d}: "
                    + ", ".join(validation.errors)
                )

            destination = revisions_dir / revision_name
            staging.replace(destination)
            thumbnail_name = self._publish_current_thumbnail(snapshot, destination)
            self._resolve_failure_records(snapshot.episode.number)
            return ArchivedRevision(
                revision_name=revision_name,
                revision_dir=destination,
                thumbnail_name=thumbnail_name,
                fingerprint=fingerprint,
                created=True,
            )
        except Exception:
            raise

    def record_failure(self, snapshot_or_number: SourceSnapshot | int, message: str) -> None:
        if isinstance(snapshot_or_number, SourceSnapshot):
            snapshot = snapshot_or_number
            staging = None
        else:
            snapshot = None
            staging = None
        number = (
            snapshot.episode.number
            if snapshot is not None
            else int(snapshot_or_number)
        )
        self._record_failure_number(number, message, staging)

    def _write_snapshot(
        self,
        *,
        snapshot: SourceSnapshot,
        directory: Path,
        revision_name: str,
        fingerprint: str,
        artifact_hashes: dict[str, str],
    ) -> None:
        (directory / "description.txt").write_text(
            snapshot.description,
            encoding="utf-8",
            newline="",
        )
        for caption in snapshot.captions:
            name = f"captions.{caption.kind}.{caption.language}.{caption.ext}"
            (directory / name).write_text(
                caption.content,
                encoding="utf-8",
                newline="",
            )

        thumbnail_name = f"thumbnail.{snapshot.thumbnail_ext}"
        (directory / thumbnail_name).write_bytes(snapshot.thumbnail)
        (directory / "info.json").write_text(
            json.dumps(snapshot.info, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (directory / "hashes.json").write_text(
            json.dumps(artifact_hashes, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        manifest = {
            "episode": snapshot.episode.number,
            "video_id": snapshot.episode.video_id,
            "revision": revision_name,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "fingerprint": fingerprint,
            "description": "description.txt",
            "captions": [
                {
                    "kind": caption.kind,
                    "language": caption.language,
                    "ext": caption.ext,
                    "file": f"captions.{caption.kind}.{caption.language}.{caption.ext}",
                }
                for caption in snapshot.captions
            ],
            "thumbnail": thumbnail_name,
        }
        (directory / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _find_fingerprint(self, revisions_dir: Path, fingerprint: str) -> Path | None:
        if not revisions_dir.exists():
            return None
        for revision in sorted(revisions_dir.iterdir(), reverse=True):
            manifest_path = revision / "manifest.json"
            if not manifest_path.exists():
                continue
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if manifest.get("fingerprint") == fingerprint:
                return revision
        return None

    def _unique_revision_name(self, revisions_dir: Path, base: str) -> str:
        candidate = base
        counter = 1
        while (revisions_dir / candidate).exists():
            candidate = f"{base}_{counter:02d}"
            counter += 1
        return candidate

    def _publish_current_thumbnail(
        self,
        snapshot: SourceSnapshot,
        revision_dir: Path,
    ) -> str:
        name = f"{snapshot.episode.number:03d}.{snapshot.thumbnail_ext}"
        destination = self._root / "06 Assets" / "Thumbnails" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(revision_dir / f"thumbnail.{snapshot.thumbnail_ext}", destination)
        return name

    def _record_failure(
        self,
        snapshot: SourceSnapshot,
        message: str,
        staging: Path | None,
    ) -> None:
        self._record_failure_number(snapshot.episode.number, message, staging)

    def _record_failure_number(
        self,
        number: int,
        message: str,
        staging: Path | None,
    ) -> None:
        failure_dir = self._root / ".osf" / "failures"
        failure_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%SZ")
        payload = {
            "episode": number,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "staging": str(staging.relative_to(self._root)) if staging else None,
        }
        path = failure_dir / f"{timestamp}-{number:03d}.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _resolve_failure_records(self, number: int) -> None:
        failure_dir = self._root / ".osf" / "failures"
        if not failure_dir.exists():
            return

        records = sorted(failure_dir.glob(f"*-{number:03d}.json"))
        if not records:
            return

        resolved_dir = failure_dir / "resolved"
        resolved_dir.mkdir(parents=True, exist_ok=True)
        for record in records:
            destination = resolved_dir / record.name
            counter = 1
            while destination.exists():
                destination = resolved_dir / f"{record.stem}_{counter:02d}{record.suffix}"
                counter += 1
            record.replace(destination)
