# Upstream updates

This scaffold is a living template. As it improves (better lint checks, new categories, schema refinements, fixed bugs), instantiated family KBs can pull those improvements without clobbering their own content.

This document explains **which files are upstream-tracked** (safe to pull) versus **instance-only** (never overwrite), and how to do the sync — either through the `/sync-scaffold` skill or manually.

The machine-readable source of truth for tooling is [`UPSTREAM.manifest.yml`](UPSTREAM.manifest.yml). If this prose and the manifest ever disagree, stop and fix both before syncing.

## Reading order

Agents reading this repo walk a four-layer chain at session start:

1. **`AGENTS.md`** — core schema and operating manual. Upstream-tracked in full.
2. **`AGENTS.overlay.md`** — optional layer injected by a host application. Instance-only + gitignored. If absent, skip.
3. **`AGENTS.family.md`** — family-specific data (children, household, tone, etc.). Instance-only.
4. **`AGENTS.local.md`** — per-user and per-machine preferences. Instance-only + gitignored.

Each layer's `.example` counterpart is the schema template and is upstream-tracked.

## The split

### Upstream-tracked (pull updates)

These files define the *scaffold*. Improvements to them come from upstream and should flow downstream.

- `AGENTS.md` — core schema. Upstream-tracked **in full** (no protected region).
- `AGENTS.family.md.example` — schema template for family-level data.
- `AGENTS.overlay.md.example` — schema template for the optional overlay layer.
- `AGENTS.local.md.example` — schema template for per-user preferences.
- `PRIVACY.md`, `LICENSE.md`, `CONTRIBUTING.md`, `UPSTREAM.md`, `UPSTREAM.manifest.yml`, `OVERLAY_CONTRACT.md`, `STORAGE.md` — scaffold documentation and contracts.
- `README.md` — scaffold introduction. Upstream-tracked by default. If you've rebranded or customized it for your family, list it under `instance_protected_paths:` in `AGENTS.overlay.md` (see [`AGENTS.overlay.md.example`](AGENTS.overlay.md.example)) so `/sync-scaffold` skips it on future pulls.
- `.gitignore` — stamp-file exclusions, OS noise, and the `AGENTS.local.md` / `AGENTS.overlay.md` / `.local/` ignore rules themselves. Downstream instances pick up new ignore rules via sync.
- `schema/**`, `scripts/validate_scaffold.py`, `.github/workflows/validate.yml` — public validation and machine-readable schemas for the scaffold.
- `.agents/skills/**` — agent-agnostic scaffold skills.
- `.claude/**` — hooks, skills, settings for Claude Code integration.
- `wiki/children/_template/**` (including `**/index.md` reference examples) — fictional "Sam" reference subtree.
- `wiki/family/_examples/**` (including `**/index.md` reference examples) — fictional family reference subtree.
- `wiki/family/*/README.md` — the per-category intros explaining what goes in each family dir (scaffold schema doc).
- `raw/README.md`, `raw/.gitkeep` — drop-zone scaffolding.

### Instance-only (never overwrite)

These files are yours. The sync process never touches them.

- `AGENTS.family.md` — your family data, populated at bootstrap. Tracked in your private repo (not gitignored), but never touched by sync. Stays out of upstream PRs; only the `.example` counterpart travels upstream.
- `AGENTS.overlay.md` — gitignored. Optional overlay layer injected by a host application if you use one. Absent for self-hosted users — scaffold works fine without it.
- `AGENTS.local.md` — your per-user preferences (gitignored; each checkout has its own).
- `.agents/skills.overlay/**` — gitignored. Host-app-injected skills that sit alongside the upstream-tracked `.agents/skills/**`. Absent by default.
- `.agents/hooks.overlay/**` — gitignored. Host-app-injected hook scripts or descriptors. Absent by default.
- `.agents/settings.local.json` — gitignored. Per-user / overlay settings for generic host tooling.
- `.claude/skills.overlay/**` — gitignored. Claude Code compatibility host-app skills. Absent by default.
- `.claude/hooks.overlay/**` — gitignored. Claude Code compatibility host-app hook scripts. Absent by default.
- `.claude/settings.local.json` — gitignored. Claude Code's built-in per-user / overlay settings layer; Claude Code merges it on top of `.claude/settings.json` (upstream-tracked) automatically. Use this file — not `settings.json` — for overlay hook registrations and local tweaks.
- `wiki/children/<your-real-child-slug>/**` — per-child directories you added (including lazy-created `<subcat>/index.md` files).
- Everything under `wiki/family/**` **except** what's listed in the upstream-tracked section above (i.e., all your real family content, but not `_examples/` or per-category READMEs).
- `wiki/family/*/index.md` — per-category content listings. The scaffold ships initial placeholders; you maintain them as you file pages.
- `wiki/index.md`, `wiki/log.md`, `wiki/audit-log.md`, `wiki/contradictions.md`, `wiki/todo.md`, `wiki/timeline.md` — instance-maintained state.
- `raw/**` — everything except the `README.md` / `.gitkeep` already listed.
- `.agents-*` stamp files (gitignored anyway).
- `.scaffold-upstream` — optional per-instance upstream URL override for `/sync-scaffold`.
- `.local/` — gitignored scratch space for instance-only docs (upgrade notes, private plans). Never synced, never published.

### README vs. index inside `wiki/family/<cat>/`

Each shipped family-category directory has both:

- `README.md` — the scaffold's **schema/how-to doc** (upstream-tracked). Explains what goes in the directory, filename conventions, and references the `index.md`. Do not edit — the next sync will overwrite your changes.
- `index.md` — your **content listing** (instance-only). Lists each page in the directory with a one-line summary. Agents update this whenever they file a new page.

The same split applies to per-child subcategory directories: once a real `wiki/children/<slug>/<subcat>/` contains content, its `index.md` is instance-only.

If you're unsure whether a file is tracked, ask your agent or consult `UPSTREAM.manifest.yml` — `/sync-scaffold` refuses to touch anything outside the tracked list.

## Write-scope rule (for agents)

Agents maintaining this KB must honor this rule:

> **Do not write to an upstream-tracked file without first confirming with the user** that they understand the change will be overwritten on the next `/sync-scaffold` — unless they intend to contribute the change upstream via a PR against the template repo.
>
> `AGENTS.md` has no protected region; it is upstream-tracked in full. Family-specific data belongs in `AGENTS.family.md` (instance-only), not in `AGENTS.md`.

See `AGENTS.md` "Write-scope rule" for the full statement.

## How to sync

### Option A — `/sync-scaffold` skill (recommended)

If you're using an agent that can discover skills under `.agents/skills/` or Claude Code's compatibility `.claude/skills/`, invoke:

```
/sync-scaffold
```

The skill:

1. Confirms your working tree is clean.
2. Fetches the upstream template (default: the canonical template URL; override via a one-line `.scaffold-upstream` file at the repo root).
3. Reads `UPSTREAM.manifest.yml` and diffs upstream-tracked paths only.
4. Shows you proposed changes before applying.
5. Runs `/lint` after the merge.
6. Offers to commit (respecting `auto_commit` / `auto_push` from your `AGENTS.local.md`).

The skill refuses to touch instance-only paths (`AGENTS.family.md`, `AGENTS.overlay.md`, `AGENTS.local.md`, your real `wiki/` content, and so on).

### Option B — manual `git remote add upstream`

```bash
git remote add upstream <template-repo-url>
git fetch upstream
```

Then for each upstream-tracked path from `UPSTREAM.manifest.yml` you want to update:

```bash
git checkout upstream/main -- <path>
```

`AGENTS.md` is safe to `git checkout upstream/main -- AGENTS.md` — it has no protected region. Your family data lives in `AGENTS.family.md` (instance-only), which is never in the diff.

Review the diff, run lint, commit.

## What the scaffold URL is

The canonical upstream is https://github.com/jrokeach/when-you-were. That's the public template repo this scaffold is maintained in. If you forked or cloned from a different location, put your preferred upstream URL on a single line in `.scaffold-upstream` at the repo root. If `.scaffold-upstream` is absent, `/sync-scaffold` uses the canonical URL above (and will prompt you to confirm on first run).
