# OSF Tooling

Python collector/parser for the local Obsidian Soundfields Atlas.

## Setup

The project uses the vault-local virtual environment:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e tools/osf
```

## Main command

```bash
.venv/bin/osf --vault . ingest 001-010
```

That performs:

```text
catalog
→ acquire with yt-dlp
→ stage
→ validate
→ immutable Raw Source revision
→ structural parse
→ knowledge resolution
→ Reader Source / Episode / Entity render
→ final validation gate
```

Video and audio are never downloaded.

## Commands

```bash
.venv/bin/osf --vault . ingest 001-010
.venv/bin/osf --vault . check 001-010
.venv/bin/osf --vault . status
.venv/bin/osf --vault . catalog
```

## TDD seams

Tests exercise the five agreed behavioral seams:

1. Collector
2. StructuralParser
3. KnowledgeResolver
4. Renderer
5. Validator

Run:

```bash
.venv/bin/python -m pytest -q tests
```

See [[../../docs/collector|Collector and Parser]] and [[../../docs/plan-v3|Plan v3]].
