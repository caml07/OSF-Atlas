# Sources

Generated per-Episode source material lives here **locally**.

Current shape:

```text
05 Sources/
└── 001/
    ├── source.md
    └── revisions/
        └── 2026-09-25_05-43-00Z/
            ├── description.txt
            ├── captions.en.vtt
            ├── info.json
            ├── thumbnail.webp
            ├── manifest.json
            └── hashes.json
```

- `source.md` is the generated Obsidian Reader Source.
- `revisions/` contains immutable local Raw Source snapshots.
- `source.md` and `revisions/` are intentionally excluded from the public Git repository because they can contain complete upstream OSF descriptions or captions.
- The collector regenerates Reader Source from the preserved local revision.
- No video or audio belongs here.
