# raw/

Drop zone for source material the agent can ingest into the wiki.

## What goes here

- Scans of artwork, report cards, doctor's notes, greeting cards
- Photos and screenshots worth referencing from a memory or milestone page
- Voice memo transcripts (drop the text; discard the audio if you don't want to keep it)
- Copies of emails, texts, or messages worth preserving (export them, paste as markdown)
- Anything external that a wiki page should cite via `sources:`

## What does NOT go here

- Generated wiki content (that lives in `wiki/`)
- Configuration (AGENTS.md / AGENTS.local.md)
- Original media you don't want to commit — if photos live in your photo library, reference them by path/timestamp rather than copying them here

## Conventions

- Organize by category and month: `raw/<category>/<YYYY-MM>/descriptive-filename.ext`
- Keep filenames descriptive: `2024-03-ava-first-drawing-of-noah.jpg` not `IMG_0482.jpg`
- Once a raw source is ingested and cited in a wiki page, leave it in place — wiki pages reference it forever via `sources:` frontmatter

## Examples

```
raw/
├── artwork/
│   └── 2024-03/
│       └── ava-first-drawing-of-noah.jpg
├── report-cards/
│   └── 2024-06/
│       └── ava-kindergarten-eoy.pdf
├── quotes/
│   └── 2024-08/
│       └── ava-dinner-table-quotes.md
└── voice-memos/
    └── 2024-09/
        └── noah-first-sentence-transcript.md
```

The agent treats files under `raw/` as immutable sources. It reads them, cites them, and never rewrites them.
