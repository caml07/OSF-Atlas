from __future__ import annotations

import re
from pathlib import Path

from .models import EpisodeIdentity, KnowledgeUpdate, ParsedSource


_HUMAN_KEYS = ("favorite", "rating", "status", "last_read")
_HUMAN_BLOCK = re.compile(
    r"<!-- OSF:HUMAN:START -->\s*(?P<body>.*?)\s*<!-- OSF:HUMAN:END -->",
    re.DOTALL,
)


class Renderer:
    """Render Obsidian projections while preserving human-owned state."""

    def __init__(self, vault_root: Path) -> None:
        self._root = Path(vault_root)

    def render_episode(
        self,
        *,
        identity: EpisodeIdentity,
        parsed: ParsedSource,
        knowledge: KnowledgeUpdate,
        source_revision: str,
        thumbnail_name: str,
    ) -> None:
        episode_path = self._root / "01 Episodes" / f"{identity.note_name}.md"
        source_dir = self._root / "05 Sources" / f"{identity.number:03d}"
        source_dir.mkdir(parents=True, exist_ok=True)

        previous = episode_path.read_text(encoding="utf-8") if episode_path.exists() else ""
        human_lines = self._human_frontmatter(previous)
        human_notes = self._human_notes(previous)

        reader = self._render_reader_source(
            identity=identity,
            parsed=parsed,
            knowledge=knowledge,
            source_revision=source_revision,
        )
        (source_dir / "source.md").write_text(reader, encoding="utf-8")

        entity_name = knowledge.primary_entity.canonical_name
        entity_path = self._root / "02 Entities" / "Places" / f"{entity_name}.md"
        entity_path.parent.mkdir(parents=True, exist_ok=True)
        self._upsert_entity(entity_path, entity_name, identity)

        episode_path.parent.mkdir(parents=True, exist_ok=True)
        episode_path.write_text(
            self._render_episode_note(
                identity=identity,
                parsed=parsed,
                knowledge=knowledge,
                source_revision=source_revision,
                thumbnail_name=thumbnail_name,
                human_lines=human_lines,
                human_notes=human_notes,
            ),
            encoding="utf-8",
        )

    def _human_frontmatter(self, previous: str) -> dict[str, str]:
        defaults = {
            "favorite": "false",
            "rating": "",
            "status": "unread",
            "last_read": "",
        }
        if not previous.startswith("---\n"):
            return defaults

        end = previous.find("\n---", 4)
        if end < 0:
            return defaults

        for line in previous[4:end].splitlines():
            key, sep, value = line.partition(":")
            if sep and key.strip() in _HUMAN_KEYS:
                defaults[key.strip()] = value.strip()
        return defaults

    def _human_notes(self, previous: str) -> str:
        match = _HUMAN_BLOCK.search(previous)
        if match:
            return match.group("body").strip() or "-"
        return "-"

    def _render_reader_source(
        self,
        *,
        identity: EpisodeIdentity,
        parsed: ParsedSource,
        knowledge: KnowledgeUpdate,
        source_revision: str,
    ) -> str:
        description = parsed.description
        for connection in knowledge.connections:
            if connection.status != "confirmed":
                continue
            replacement = (
                f"[[{connection.target_episode.note_name}|{connection.evidence_text}]]"
            )
            description = description.replace(connection.evidence_text, replacement)
        description = "\n".join(line.rstrip() for line in description.splitlines())

        manual = [c for c in parsed.snapshot.captions if c.kind == "manual"]
        automatic = [c for c in parsed.snapshot.captions if c.kind == "automatic"]

        return (
            "---\n"
            "type: reader-source\n"
            f'episode: "[[{identity.note_name}]]"\n'
            f"osf_number: {identity.number}\n"
            f"source_revision: {source_revision}\n"
            "schema_version: 1\n"
            "parser_version: 1\n"
            "tags: [osf, source]\n"
            "cssclasses: [osf-reader-source]\n"
            "---\n\n"
            f"# Source — {identity.number:03d} // {identity.title}\n\n"
            "> [!info] Reader projection\n"
            f"> Generated from Source Revision '{source_revision}'.<br>\n"
            "> Raw source files are preserved unchanged. Confirmed wiki-link "
            "annotations may be added here for Obsidian navigation.\n\n"
            "## YouTube Description\n\n"
            f"{description}\n\n"
            f"{self._caption_callout('English Manual Captions', manual)}\n\n"
            f"{self._caption_callout('English Automatic Captions', automatic)}\n"
        )

    def _caption_callout(self, title: str, tracks: list) -> str:
        if not tracks:
            return f"> [!abstract]- {title}\n> _Not available for this Episode._"
        lines = [f"> [!abstract]- {title}"]
        for track in tracks:
            lines.append(f"> **{track.language} · {track.ext}**")
            for line in track.content.splitlines():
                lines.append(f"> {line}")
        return "\n".join(lines)

    def _render_episode_note(
        self,
        *,
        identity: EpisodeIdentity,
        parsed: ParsedSource,
        knowledge: KnowledgeUpdate,
        source_revision: str,
        thumbnail_name: str,
        human_lines: dict[str, str],
        human_notes: str,
    ) -> str:
        entity = knowledge.primary_entity.canonical_name
        confirmed = [
            c.target_episode.note_name
            for c in knowledge.connections
            if c.status == "confirmed"
        ]
        candidates = [
            c.target_episode.note_name
            for c in knowledge.connections
            if c.status == "candidate"
        ]
        cover = f"[[06 Assets/Thumbnails/{thumbnail_name}]]"
        thumbnail_rel = f"../06%20Assets/Thumbnails/{thumbnail_name}"
        safe_title = identity.title.replace('"', "'")

        frontmatter = [
            "---",
            "type: episode",
            f"osf_number: {identity.number}",
            f'title: "{safe_title}"',
            f"youtube_id: {identity.video_id}",
            f"youtube_url: {parsed.snapshot.url}",
            f"published: {parsed.snapshot.published or ''}",
            f"duration_seconds: {parsed.snapshot.duration_seconds or ''}",
            f'cover: "{cover}"',
            f"source_revision: {source_revision}",
            "source_status: complete",
            "ingestion_status: complete",
            "lore_review_status: pending",
            "schema_version: 1",
            "parser_version: 1",
            self._human_frontmatter_line("favorite", human_lines["favorite"]),
            self._human_frontmatter_line("rating", human_lines["rating"]),
            self._human_frontmatter_line("status", human_lines["status"]),
            self._human_frontmatter_line("last_read", human_lines["last_read"]),
            f'entities: ["[[{entity}]]"]',
            "confirmed_connections: ["
            + ", ".join(f'"[[{name}]]"' for name in confirmed)
            + "]",
            "candidate_connections: ["
            + ", ".join(f'"[[{name}]]"' for name in candidates)
            + "]",
            "inferred_connections: []",
            "tags: [osf, episode]",
            "cssclasses: [osf-episode]",
            "---",
        ]

        confirmed_body = (
            "\n".join(f"- [[{name}]]" for name in confirmed)
            if confirmed
            else "_No confirmed connections yet._"
        )
        candidate_body = (
            "\n".join(f"- [[{name}]]" for name in candidates)
            if candidates
            else "_No candidate connections yet._"
        )

        return (
            "\n".join(frontmatter)
            + "\n\n"
            + f"# {identity.number:03d} // {identity.title}\n\n"
            + "<!-- OSF:GENERATED:START -->\n\n"
            + f"[![{identity.number:03d} // {identity.title}]({thumbnail_rel})]"
            + f"({parsed.snapshot.url})\n\n"
            + "> [!info] Episode\n"
            + f"> **OSF:** {identity.number:03d}<br>\n"
            + f"> **Published:** {parsed.snapshot.published or 'Unknown'}<br>\n"
            + f"> **Current source revision:** {source_revision}<br>\n"
            + f"> [Watch on YouTube]({parsed.snapshot.url})\n\n"
            + "## Source\n\n"
            + f"![[05 Sources/{identity.number:03d}/source]]\n\n"
            + "## Lore Overview\n\n"
            + "_Semantic lore summary will grow from evidence-backed parsing and review._\n\n"
            + "## Entities\n\n"
            + f"- [[{entity}]]\n\n"
            + "## Connections\n\n"
            + "### Confirmed\n\n"
            + confirmed_body
            + "\n\n### Candidates\n\n"
            + candidate_body
            + "\n\n"
            + "### Inferred\n\n_No inferred connections yet._\n\n"
            + "<!-- OSF:GENERATED:END -->\n\n"
            + "## My Notes\n\n"
            + "<!-- OSF:HUMAN:START -->\n\n"
            + human_notes
            + "\n\n<!-- OSF:HUMAN:END -->\n"
        )

    def _human_frontmatter_line(self, key: str, value: str) -> str:
        return f"{key}: {value}" if value else f"{key}:"

    def _upsert_entity(
        self,
        path: Path,
        canonical_name: str,
        identity: EpisodeIdentity,
    ) -> None:
        episode_link = f"[[{identity.note_name}]]"
        if path.exists():
            current = path.read_text(encoding="utf-8")
            if episode_link in current:
                return
            marker = "## Appears In\n"
            if marker in current:
                current = current.replace(
                    marker,
                    marker + f"\n- {episode_link}\n",
                    1,
                )
                path.write_text(current, encoding="utf-8")
                return

        safe_name = canonical_name.replace('"', "'")
        path.write_text(
            "---\n"
            "type: entity\n"
            f'canonical_name: "{safe_name}"\n'
            "entity_type: place\n"
            "aliases: []\n"
            f"first_seen: {identity.number}\n"
            "tags: [osf, entity]\n"
            "cssclasses: [osf-entity]\n"
            "---\n\n"
            f"# {canonical_name}\n\n"
            "## Overview\n\n"
            f"Primary location/entity associated with [[{identity.note_name}]].\n\n"
            "## Evidence\n\n"
            f"- Primary subject of [[{identity.note_name}]].\n\n"
            "## Appears In\n\n"
            f"- {episode_link}\n\n"
            "## Connections\n\n"
            "### Confirmed\n\n-\n\n"
            "### Inferred\n\n-\n\n"
            "## My Notes\n\n-\n",
            encoding="utf-8",
        )
