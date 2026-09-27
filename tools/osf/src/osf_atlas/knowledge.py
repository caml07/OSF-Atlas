from __future__ import annotations

from collections.abc import Mapping

from .models import (
    Connection,
    EntityIdentity,
    EpisodeIdentity,
    KnowledgeUpdate,
    ParsedSource,
)


class KnowledgeResolver:
    """Resolve only evidence-backed knowledge; fuzzy lore stays out of this seam."""

    def resolve(
        self,
        parsed: ParsedSource,
        catalog: Mapping[int, EpisodeIdentity],
    ) -> KnowledgeUpdate:
        current_number = parsed.snapshot.episode.number
        current = catalog.get(current_number)
        if current is None:
            raise KeyError(f"Episode {current_number:03d} is missing from the catalog")

        connections: list[Connection] = []
        seen_targets: set[int] = set()
        for reference in parsed.explicit_references:
            target = catalog.get(reference.osf_number)
            if target is None or target.number == current_number:
                continue
            connections.append(
                Connection(
                    source_episode_number=current_number,
                    target_episode=target,
                    status="confirmed",
                    evidence_text=reference.raw_text,
                )
            )
            seen_targets.add(target.number)

        if ":" in current.title:
            base_title = current.title.split(":", 1)[0].strip()
            base = next(
                (
                    identity
                    for identity in catalog.values()
                    if identity.number < current_number and identity.title == base_title
                ),
                None,
            )
            if base is not None and base.number not in seen_targets:
                connections.append(
                    Connection(
                        source_episode_number=current_number,
                        target_episode=base,
                        status="confirmed",
                        evidence_text=f"title-variant: {base_title}",
                    )
                )

        return KnowledgeUpdate(
            primary_entity=EntityIdentity(
                canonical_name=current.title,
                episode_number=current_number,
            ),
            connections=tuple(connections),
        )
