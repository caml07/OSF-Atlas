from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .catalog import discover_catalog, parse_range
from .collector import Collector
from .pipeline import Ingestor
from .validator import Validator
from .yt_dlp_adapter import YtDlpAdapter


def _find_vault(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        context = candidate / "CONTEXT.md"
        if context.exists() and context.read_text(encoding="utf-8").startswith(
            "# Obsidian Soundfields Atlas"
        ):
            return candidate

    default = Path.home() / "Documents" / "Obsidian" / "Obsidian Soundfields"
    if default.exists():
        return default.resolve()
    raise SystemExit("Could not locate the Obsidian Soundfields vault; use --vault")


def _write_catalog(vault: Path, catalog: dict) -> None:
    state_dir = vault / ".osf" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        f"{number:03d}": {
            "number": identity.number,
            "title": identity.title,
            "video_id": identity.video_id,
            "note_name": identity.note_name,
        }
        for number, identity in sorted(catalog.items())
    }
    (state_dir / "catalog.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _select(catalog: dict, raw_range: str):
    start, end = parse_range(raw_range)
    missing = [number for number in range(start, end + 1) if number not in catalog]
    if missing:
        formatted = ", ".join(f"{number:03d}" for number in missing)
        raise SystemExit(f"Missing Episodes in channel catalog: {formatted}")
    return tuple(catalog[number] for number in range(start, end + 1))


def cmd_ingest(args: argparse.Namespace) -> int:
    vault = _find_vault(args.vault)
    catalog = discover_catalog()
    _write_catalog(vault, catalog)
    identities = _select(catalog, args.range)
    ingestor = Ingestor(vault, catalog, Collector(YtDlpAdapter()))

    failures = 0
    for identity in identities:
        print(f"[{identity.number:03d}] {identity.title}")
        result = ingestor.ingest(identity)
        if result.validation.ok and result.revision is not None:
            action = "new revision" if result.revision.created else "unchanged"
            print(
                f"  OK  {action}: {result.revision.revision_name} "
                f"({result.revision.fingerprint[:12]})"
            )
        else:
            failures += 1
            details = "; ".join(result.validation.errors) or result.error or "unknown failure"
            print(f"  FAIL  {details}")

    batch = Validator().validate_batch(vault, identities)
    if not batch.ok:
        failures += 1
        print("Batch gate: FAIL")
        for error in batch.errors:
            print(f"  - {error}")
    else:
        print(f"Batch gate: PASS ({len(identities)}/{len(identities)})")

    return 1 if failures else 0


def cmd_check(args: argparse.Namespace) -> int:
    vault = _find_vault(args.vault)
    catalog = discover_catalog()
    _write_catalog(vault, catalog)
    identities = _select(catalog, args.range)
    report = Validator().validate_batch(vault, identities)
    if report.ok:
        print(f"PASS ({len(identities)}/{len(identities)})")
        return 0
    print("FAIL")
    for error in report.errors:
        print(f"- {error}")
    return 1


def cmd_status(args: argparse.Namespace) -> int:
    vault = _find_vault(args.vault)
    episode_dir = vault / "01 Episodes"
    source_dir = vault / "05 Sources"
    episodes = sorted(episode_dir.glob("OSF *.md"))
    revisions = sum(
        len(list(path.glob("revisions/*")))
        for path in source_dir.iterdir()
        if path.is_dir()
    ) if source_dir.exists() else 0
    failures = len(list((vault / ".osf" / "failures").glob("*.json")))

    print(f"Vault: {vault}")
    print(f"Episode notes: {len(episodes)}")
    print(f"Source revisions: {revisions}")
    print(f"Failed extraction records: {failures}")
    return 0


def cmd_catalog(args: argparse.Namespace) -> int:
    vault = _find_vault(args.vault)
    catalog = discover_catalog()
    _write_catalog(vault, catalog)
    print(f"Cataloged {len(catalog)} numbered Episodes")
    for number in sorted(catalog):
        identity = catalog[number]
        print(f"{number:03d}\t{identity.video_id}\t{identity.title}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="osf")
    parser.add_argument("--vault", help="Path to the OSF vault")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Fetch, preserve, parse, render, and validate Episodes")
    ingest.add_argument("range", help="Episode number or range, e.g. 001-010")
    ingest.set_defaults(func=cmd_ingest)

    check = sub.add_parser("check", help="Run the batch validation gate")
    check.add_argument("range", help="Episode number or range")
    check.set_defaults(func=cmd_check)

    status = sub.add_parser("status", help="Show local archive status")
    status.set_defaults(func=cmd_status)

    catalog = sub.add_parser("catalog", help="Refresh and print the channel catalog")
    catalog.set_defaults(func=cmd_catalog)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
