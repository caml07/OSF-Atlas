from __future__ import annotations

import re

from .models import ExplicitReference, ParsedSource, SourceSnapshot


_EXPLICIT_OSF_REFERENCE = re.compile(
    r"(?:"
    r"(?P<label_paren>[A-Z][A-Za-z0-9'’:-]*(?:\s+[A-Z][A-Za-z0-9'’:-]*){0,3})"
    r"\s+\(OSF[-\s]?(?P<number_paren>\d{3})\)"
    r"|"
    r"(?:(?P<label>[A-Z][A-Za-z0-9'’:-]*(?:\s+[A-Z][A-Za-z0-9'’:-]*){0,3})\s+)?"
    r"OSF[-\s]?(?P<number>\d{3})"
    r")"
)
_INCIDENT_LABEL = re.compile(r"\bIncident Log\s+[A-Za-z0-9-]+\b", re.IGNORECASE)
_STRUCTURED_LABEL = re.compile(
    r"(?m)^\[[A-Z][A-Z0-9'’ -]{1,64}\][ \t]*$"
)


class StructuralParser:
    """Parse source syntax without making semantic lore judgments."""

    def parse(self, snapshot: SourceSnapshot) -> ParsedSource:
        references: list[ExplicitReference] = []
        for match in _EXPLICIT_OSF_REFERENCE.finditer(snapshot.description):
            number = int(match.group("number_paren") or match.group("number"))
            references.append(
                ExplicitReference(raw_text=match.group(0), osf_number=number)
            )

        incident_labels = tuple(
            dict.fromkeys(match.group(0) for match in _INCIDENT_LABEL.finditer(snapshot.description))
        )
        structured_labels = tuple(
            dict.fromkeys(
                match.group(0).strip()
                for match in _STRUCTURED_LABEL.finditer(snapshot.description)
            )
        )

        return ParsedSource(
            snapshot=snapshot,
            description=snapshot.description,
            explicit_references=tuple(references),
            incident_labels=incident_labels,
            structured_labels=structured_labels,
        )
