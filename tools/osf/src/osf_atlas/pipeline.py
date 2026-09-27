from __future__ import annotations

from pathlib import Path

from .archive import SourceArchive
from .collector import Collector
from .knowledge import KnowledgeResolver
from .models import EpisodeIdentity, EpisodeRef, IngestResult, ValidationReport
from .parser import StructuralParser
from .renderer import Renderer
from .state import KnowledgeStore
from .validator import Validator


class Ingestor:
    """Compose the five public seams into one Episode ingestion workflow."""

    def __init__(
        self,
        vault_root: Path,
        catalog: dict[int, EpisodeIdentity],
        collector: Collector,
    ) -> None:
        self._root = Path(vault_root)
        self._catalog = catalog
        self._collector = collector
        self._validator = Validator()
        self._archive = SourceArchive(self._root, self._validator)
        self._parser = StructuralParser()
        self._resolver = KnowledgeResolver()
        self._renderer = Renderer(self._root)
        self._knowledge = KnowledgeStore(self._root)

    def ingest(self, identity: EpisodeIdentity) -> IngestResult:
        episode_ref = EpisodeRef(
            number=identity.number,
            video_id=identity.video_id,
            title=identity.title,
        )
        try:
            snapshot = self._collector.collect(episode_ref)
            revision = self._archive.preserve(snapshot)
            parsed = self._parser.parse(snapshot)
            knowledge = self._resolver.resolve(parsed, self._catalog)
            self._knowledge.persist(identity, knowledge)
            self._renderer.render_episode(
                identity=identity,
                parsed=parsed,
                knowledge=knowledge,
                source_revision=revision.revision_name,
                thumbnail_name=revision.thumbnail_name,
            )
            validation = self._validator.validate_rendered_episode(
                self._root,
                identity,
                revision.revision_name,
                revision.thumbnail_name,
            )
            if not validation.ok:
                self._archive.record_failure(
                    snapshot,
                    "Rendered Episode validation failed: " + ", ".join(validation.errors),
                )
                self._mark_episode_failed(identity)
                return IngestResult(
                    episode=identity,
                    revision=revision,
                    validation=validation,
                    error="render-validation",
                )

            return IngestResult(
                episode=identity,
                revision=revision,
                validation=validation,
            )
        except Exception as exc:
            self._archive.record_failure(identity.number, str(exc))
            return IngestResult(
                episode=identity,
                revision=None,
                validation=ValidationReport(ok=False, errors=(str(exc),)),
                error=str(exc),
            )

    def _mark_episode_failed(self, identity: EpisodeIdentity) -> None:
        path = self._root / "01 Episodes" / f"{identity.note_name}.md"
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "ingestion_status: complete",
            "ingestion_status: failed",
            1,
        )
        path.write_text(text, encoding="utf-8")
