from __future__ import annotations

from pathlib import Path

from .models import EpisodeIdentity, SourceSnapshot, ValidationReport


class Validator:
    """Validate promoted source artifacts and rendered Episode outputs."""

    def validate_source(
        self,
        snapshot: SourceSnapshot,
        revision_dir: Path,
    ) -> ValidationReport:
        revision_dir = Path(revision_dir)
        errors: list[str] = []

        description_path = revision_dir / "description.txt"
        if not description_path.exists():
            errors.append("description.txt")
        elif description_path.read_text(encoding="utf-8") != snapshot.description:
            errors.append("description.txt:mismatch")

        thumbnail_path = revision_dir / f"thumbnail.{snapshot.thumbnail_ext}"
        if not thumbnail_path.exists():
            errors.append(thumbnail_path.name)
        elif thumbnail_path.read_bytes() != snapshot.thumbnail:
            errors.append(f"{thumbnail_path.name}:mismatch")

        for caption in snapshot.captions:
            name = f"captions.{caption.kind}.{caption.language}.{caption.ext}"
            path = revision_dir / name
            if not path.exists():
                errors.append(name)
                continue
            if path.read_text(encoding="utf-8") != caption.content:
                errors.append(f"{name}:mismatch")

        return ValidationReport(ok=not errors, errors=tuple(errors))

    def validate_rendered_episode(
        self,
        vault_root: Path,
        identity: EpisodeIdentity,
        revision_name: str,
        thumbnail_name: str,
    ) -> ValidationReport:
        root = Path(vault_root)
        errors: list[str] = []
        episode_path = root / "01 Episodes" / f"{identity.note_name}.md"
        source_path = root / "05 Sources" / f"{identity.number:03d}" / "source.md"
        thumbnail_path = root / "06 Assets" / "Thumbnails" / thumbnail_name

        for path in (episode_path, source_path, thumbnail_path):
            if not path.exists():
                errors.append(str(path.relative_to(root)))

        if episode_path.exists():
            episode_text = episode_path.read_text(encoding="utf-8")
            if f"source_revision: {revision_name}" not in episode_text:
                errors.append(f"{episode_path.name}:revision-mismatch")
            if "## My Notes" not in episode_text:
                errors.append(f"{episode_path.name}:missing-my-notes")

        if source_path.exists():
            source_text = source_path.read_text(encoding="utf-8")
            if "## YouTube Description" not in source_text:
                errors.append(f"{source_path.name}:missing-description")

        return ValidationReport(ok=not errors, errors=tuple(errors))

    def validate_batch(
        self,
        vault_root: Path,
        identities: tuple[EpisodeIdentity, ...],
    ) -> ValidationReport:
        root = Path(vault_root)
        errors: list[str] = []
        for identity in identities:
            path = root / "01 Episodes" / f"{identity.note_name}.md"
            if not path.exists():
                errors.append(f"{identity.number:03d}:missing-episode-note")
                continue
            text = path.read_text(encoding="utf-8")
            if "ingestion_status: complete" not in text:
                errors.append(f"{identity.number:03d}:ingestion-not-complete")
        return ValidationReport(ok=not errors, errors=tuple(errors))
