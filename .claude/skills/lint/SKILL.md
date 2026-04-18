---
name: lint
description: "Lint the When You Were wiki: check frontmatter validity, link resolution, filename conventions, typos, stale pages, orphans, and cross-child consistency. Writes findings to wiki/audit-log.md with severity tags, proposes fixes, waits for user approval before mass-editing. Invoke when the user asks to lint, when the 30-day lint nudge fires, or before a big ingest."
---

# When You Were Lint Skill

## Purpose

A periodic health check on the wiki. Finds the kinds of entropy that creep into a maintained KB: broken links after renames, typos in proper nouns, frontmatter that drifted from the schema, pages nobody links to anymore, inconsistencies between sibling pages about the same shared event.

## When to run

- User asks (`/lint`, "lint the wiki", "check the KB for problems").
- The 30-day periodic nudge fires (see AGENTS.md "Periodic prompts").
- Before a big batch ingest, if the last lint is stale.
- After a rename or reorganization.

## Severity scale

- **Critical** — factually wrong content, frontmatter that breaks parsing, data loss risks.
- **High** — broken links, missing required frontmatter fields, misfiled pages (e.g. `children/ava/` page that doesn't list `ava` in `subjects:`).
- **Medium** — stale drafts, orphan pages, inconsistent references across sibling pages, violated filename conventions.
- **Low** — typos, style nits, minor convention deviations.

## Process

Run checks in this order. Stop and ask the user if any Critical issues are found before proceeding.

### 1. Frontmatter validity

For every `.md` file under `wiki/`:

- Parses as valid YAML frontmatter.
- Required fields present: `title`, `type`, `subjects`, `status`.
- `subjects:` entries match either a known child slug (from the **Family details** section of `AGENTS.md`) or the literal `family`.
- `status` ∈ {active, draft, stale, archived, example}.
- `confidence` (if present) ∈ {high, medium, low, speculative}.
- Dates parse as ISO-8601 (YYYY-MM-DD).

### 2. Placement / subject consistency

- Pages under `wiki/children/<slug>/` MUST include `<slug>` in `subjects:`. Flag as High.
- Pages under `wiki/family/` MUST have `subjects:` with at least one child slug or `[family]`. Flag as High.
- Pages whose title or body names a child by preferred name or nickname but does not list that child in `subjects:` → Medium warning.
- Pages outside `wiki/children/_template/` and `wiki/family/_examples/` must NOT have `status: example`. Flag as High — the `example` status is reserved for the reference subtrees only.

### 3. Link resolution

- Every markdown link `[label](relative/path.md)` inside `wiki/` resolves to a real file.
- Links must be relative to the source file's directory and include the `.md` extension.
- Flag unresolved links as High.
- Flag absolute or vault-root-style paths (`[[wikilinks]]`, leading `/`, or `wiki/...` prefixes when the source is itself under `wiki/`) as Low — convention deviation.

### 4. Filename conventions

- Kebab-case: lowercase, hyphens, no spaces, no underscores.
- No leading digits unless the page is date-prefixed (`YYYY-...` or `YYYY-MM-DD-...`).
- Flag violations as Medium.

### 5. Reciprocal linking

- For every page under `children/<slug>/` that mentions a sibling's preferred name, check for a link to that sibling's `profile.md` or to the specific page referenced. Flag missing reciprocal links as Medium.
- For every `family/` event page that lists multiple subjects, check that each child's `profile.md` "Shared experiences" section links back. Flag gaps as Low.

### 6. Orphans

- Pages with zero inbound links from `index.md`, any `profile.md`, or any other content page.
- Flag as Medium. Orphans are not always bugs (fresh pages) but are worth a human eye.

### 7. Stale content

- `status: draft` with `date_recorded` older than 90 days → Medium.
- `status: active` with no file modifications in 365 days AND no `sources:` added in that time → Low ("is this still current?").

### 8. Duplicate event detection

- Pages with overlapping dates, overlapping subjects, and highly similar titles may describe the same event twice. Flag as Medium. Do NOT auto-merge — ask the user.

### 9. Typos (prose only)

- Run a spellcheck over prose body (skip frontmatter, code blocks, link targets, and tables).
- Whitelist all entries from the `family_vocabulary:` list in `AGENTS.md`'s Family details, plus `avoid_words` and custom vocab from the current user's `AGENTS.local.md` `tone_override`, plus all child slugs / preferred names / nicknames.
- Flag possible misspellings as Low.

### 10. Cross-child consistency

- For a shared event (same title pattern and overlapping dates across sibling pages), verify:
  - Each page `subjects:` list is consistent with the others' cross-references.
  - Ages listed for each kid are consistent (e.g., siblings' ages should match their birthdates and the event date).
- Flag inconsistencies as Medium.

## Output

Append a dated section to `wiki/audit-log.md`:

```markdown
## Audit — YYYY-MM-DD

- **Critical** (N): [brief list with file paths]
- **High** (N): ...
- **Medium** (N): ...
- **Low** (N): ...

### Findings

[Detailed list grouped by severity. For each finding: file path, description, proposed fix.]
```

Then:

- **Report to the user** with counts by severity.
- **Propose fixes** for clearly mechanical issues (fixing a broken link after a rename, filling a missing required field, normalizing a filename). Batch them for a single approval.
- **Ask before content-level fixes** (merging duplicates, resolving contradictions, renaming slugs).
- **Update `.agents-last-lint`** with today's date regardless of outcome.

## Scope / exclusions

The skill scans `wiki/**/*.md` with these exclusions:

- `wiki/children/_template/` — reference structure (fictional "Sam"). Its `subjects: [_template]` / `status: example` markers are intentional; do not flag.
- `wiki/family/_examples/` — reference structure for family-category pages (fictional Biscuit, Sunday pancakes, etc.). Same treatment.
- Anything explicitly marked `status: archived` — reported in a summary line only, not linted in detail.

## What the skill does NOT do

- Does not silently rewrite prose for style.
- Does not merge pages without explicit user approval.
- Does not delete orphans.
- Does not rename slugs (too many links depend on stability).
- Does not touch `AGENTS.md`, `AGENTS.local.md`, raw sources, or files outside `wiki/`.
