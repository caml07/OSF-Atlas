from __future__ import annotations

from osf_atlas.models import EpisodeRef, SourceSnapshot
from osf_atlas.parser import StructuralParser


def test_parser_extracts_only_structural_osf_references_and_incident_labels() -> None:
    description = (
        "Observation continues. Terminal OSF-053 remains reachable.\n\n"
        "Incident Log 07-B // perimeter response\n"
        "A later note references OSF-014. The word terminal alone is not a reference."
    )
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=114, video_id="vid114"),
        title="114 // The Veiled Monolith: Interior - Ambient",
        description=description,
        published=None,
        duration_seconds=3600,
        info={},
        captions=(),
        thumbnail=b"image",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid114",
    )

    parsed = StructuralParser().parse(snapshot)

    assert parsed.description == description
    assert [(ref.raw_text, ref.osf_number) for ref in parsed.explicit_references] == [
        ("Terminal OSF-053", 53),
        ("OSF-014", 14),
    ]
    assert parsed.incident_labels == ("Incident Log 07-B",)


def test_parser_preserves_parenthetical_reference_context() -> None:
    description = (
        "The Veiled Monolith (OSF-014) remains active. "
        "Terminal (OSF-053) emerged later."
    )
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=114, video_id="vid114"),
        title="114 // The Veiled Monolith: Interior - Ambient",
        description=description,
        published=None,
        duration_seconds=3600,
        info={},
        captions=(),
        thumbnail=b"image",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid114",
    )

    parsed = StructuralParser().parse(snapshot)

    assert [(ref.raw_text, ref.osf_number) for ref in parsed.explicit_references] == [
        ("The Veiled Monolith (OSF-014)", 14),
        ("Terminal (OSF-053)", 53),
    ]


def test_parser_extracts_standalone_structural_labels_without_interpreting_them() -> None:
    description = (
        "[VISITOR'S PASS]\n\n"
        "Inside the structure, nothing explains what the pass means.\n"
        "[NOT A LABEL because mixed case]\n"
    )
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=43, video_id="vid043"),
        title="043 // Silent Arbiter: Interior Hall - Ambient",
        description=description,
        published=None,
        duration_seconds=3600,
        info={},
        captions=(),
        thumbnail=b"image",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid043",
    )

    parsed = StructuralParser().parse(snapshot)

    assert parsed.structured_labels == ("[VISITOR'S PASS]",)


def test_parser_extracts_record_and_log_labels_without_interpreting_them() -> None:
    description = (
        "Case Log V-04: residual fraction stabilized briefly.\n"
        "Incident Record GR-09: the corridor failed.\n"
        "Incident ND-037-11: the subject remained still.\n"
        "A case log was mentioned without an identifier.\n"
    )
    snapshot = SourceSnapshot(
        episode=EpisodeRef(number=98, video_id="vid098"),
        title="098 // Afterlight",
        description=description,
        published=None,
        duration_seconds=3600,
        info={},
        captions=(),
        thumbnail=b"image",
        thumbnail_ext="webp",
        url="https://www.youtube.com/watch?v=vid098",
    )

    parsed = StructuralParser().parse(snapshot)

    assert parsed.incident_labels == (
        "Case Log V-04",
        "Incident Record GR-09",
        "Incident ND-037-11",
    )
