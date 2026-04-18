# Upstream updates

This scaffold is a living template. As it improves (better lint checks, new categories, schema refinements, fixed bugs), instantiated family KBs can pull those improvements without clobbering their own content.

This document defines **which files are upstream-tracked** (safe to pull) versus **instance-only** (never overwrite), and how to do the sync — either through the `/sync-scaffold` skill or manually.

## The split

### Upstream-tracked (pull updates)

These files define the *scaffold*. Improvements to them come from upstream and should flow downstream.

- `AGENTS.md` — **except** the region between `<!-- FAMILY_DETAILS_BEGIN -->` and `<!-- FAMILY_DETAILS_END -->`, which is family data and is preserved during sync.
- `AGENTS.local.md.example` — the template copy, not the real `AGENTS.local.md`.
- `PRIVACY.md`, `LICENSE.md`, `CONTRIBUTING.md`, `UPSTREAM.md` — scaffold documentation.
- `.gitignore` — stamp-file exclusions and OS noise.
- `.claude/**` — hooks, skills, settings for Claude Code integration.
- `wiki/children/_template/**` — fictional "Sam" reference subtree.
- `wiki/family/_examples/**` — fictional family reference subtree.
- `wiki/family/*/README.md` — the per-category intros explaining what goes in each family dir.
- `raw/README.md`, `raw/.gitkeep` — drop-zone scaffolding.

### Instance-only (never overwrite)

These files are yours. The sync process never touches them.

- `AGENTS.local.md` — your per-user preferences.
- The `<!-- FAMILY_DETAILS_BEGIN -->` / `<!-- FAMILY_DETAILS_END -->` block inside `AGENTS.md` — your family data.
- `wiki/children/<your-real-child-slug>/**` — per-child directories you added.
- Everything under `wiki/family/**` **except** what's listed in the upstream-tracked section above (i.e., all your real family content, but not `_examples/` or per-category READMEs).
- `wiki/index.md`, `wiki/log.md`, `wiki/audit-log.md`, `wiki/contradictions.md`, `wiki/todo.md`, `wiki/timeline.md` — instance-maintained state.
- `raw/**` — everything except the `README.md` / `.gitkeep` already listed.
- `.agents-*` stamp files (gitignored anyway).
- `README.md` — if you've customized it for your family. If not, it's upstream-tracked.

If you're unsure whether a file is tracked, ask your agent or consult the `/sync-scaffold` skill — it refuses to touch anything outside the tracked list.

## Write-scope rule (for agents)

Agents maintaining this KB must honor this rule:

> **Do not write to an upstream-tracked file without first confirming with the user** that they understand the change will be overwritten on the next `/sync-scaffold` — unless they intend to contribute the change upstream via a PR against the template repo.
>
> Inside `AGENTS.md`, only write between the `<!-- FAMILY_DETAILS_BEGIN -->` / `<!-- FAMILY_DETAILS_END -->` markers. Do not remove or rewrite those markers.

See `AGENTS.md` "Write-scope rule" for the full statement.

## How to sync

### Option A — `/sync-scaffold` skill (recommended)

If you're using Claude Code (or any agent that can discover skills under `.claude/skills/`), invoke:

```
/sync-scaffold
```

The skill:

1. Confirms your working tree is clean.
2. Fetches the upstream template (default: the canonical template URL; override via a one-line `.scaffold-upstream` file at the repo root).
3. Diffs upstream-tracked paths only.
4. Preserves your Family details block in `AGENTS.md` by extracting it before the merge and re-inserting after.
5. Shows you proposed changes before applying.
6. Runs `/lint` after the merge.
7. Offers to commit (respecting `auto_commit` / `auto_push` from your `AGENTS.local.md`).

The skill refuses to touch instance-only paths and refuses to run if the Family-details markers are missing from your local `AGENTS.md`.

### Option B — manual `git remote add upstream`

```bash
git remote add upstream <template-repo-url>
git fetch upstream
```

Then for each upstream-tracked path you want to update:

```bash
git checkout upstream/main -- <path>
```

**Do not `git checkout upstream/main -- AGENTS.md` directly** — it will overwrite your Family details. For `AGENTS.md`, do one of:

- Use the `/sync-scaffold` skill (it handles the merge correctly), or
- Manually: fetch upstream's `AGENTS.md` into a tmp file, copy everything *outside* the `FAMILY_DETAILS_BEGIN/END` markers into your local `AGENTS.md`, leave your Family details block untouched.

Review the diff, run lint, commit.

## What the scaffold URL is

The canonical upstream is https://github.com/jrokeach/when-you-were. That's the public template repo this scaffold is maintained in. If you forked or cloned from a different location, put your preferred upstream URL on a single line in `.scaffold-upstream` at the repo root. If `.scaffold-upstream` is absent, `/sync-scaffold` uses the canonical URL above (and will prompt you to confirm on first run).
