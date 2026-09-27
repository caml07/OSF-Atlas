from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import EpisodeIdentity, KnowledgeUpdate


class KnowledgeStore:
    """Persist canonical machine knowledge independently from rendered Markdown."""

    def __init__(self, vault_root: Path) -> None:
        self._root = Path(vault_root)
        self._knowledge_dir = self._root / ".osf" / "knowledge"
        self._decision_dir = self._root / ".osf" / "decisions"
        self._knowledge_dir.mkdir(parents=True, exist_ok=True)
        self._decision_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, identity: EpisodeIdentity, update: KnowledgeUpdate) -> None:
        payload = {
            "episode": identity.number,
            "episode_note": identity.note_name,
            "primary_entity": update.primary_entity.canonical_name,
            "connections": [
                {
                    "status": connection.status,
                    "target_episode": connection.target_episode.number,
                    "target_note": connection.target_episode.note_name,
                    "evidence_text": connection.evidence_text,
                }
                for connection in update.connections
            ],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        path = self._knowledge_dir / f"{identity.number:03d}.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        for connection in update.connections:
            self._write_decision(identity, connection)

    def _write_decision(self, identity: EpisodeIdentity, connection) -> None:
        target = connection.target_episode
        filename = (
            f"{identity.number:03d}-to-{target.number:03d}-"
            f"{connection.status}.md"
        )
        path = self._decision_dir / filename
        now = datetime.now(timezone.utc).isoformat()
        safe_evidence = connection.evidence_text.replace('"', "'")
        path.write_text(
            "---\n"
            "type: connection-decision\n"
            f"connection_status: {connection.status}\n"
            f'from_note: "[[{identity.note_name}]]"\n'
            f'to_note: "[[{target.note_name}]]"\n'
            f'evidence_episode: "[[{identity.note_name}]]"\n'
            f'evidence_source: "{safe_evidence}"\n'
            f"updated: {now}\n"
            "tags: [osf, lore-review]\n"
            "---\n\n"
            f"# {identity.number:03d} ↔ {target.number:03d}\n\n"
            "## Evidence\n\n"
            f"- Explicit source reference: '{connection.evidence_text}'\n\n"
            "## Decision\n\n"
            f"- **{connection.status}**\n",
            encoding="utf-8",
        )
