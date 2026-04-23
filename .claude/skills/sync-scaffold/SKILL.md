---
name: sync-scaffold
description: "Pull upstream improvements from the When You Were scaffold template into this instance, preserving family-specific data. Refuses to touch instance-only paths (AGENTS.family.md, AGENTS.overlay.md, AGENTS.local.md, wiki content), surfaces diffs for user review before applying, runs /lint after. Invoke when the user asks to sync the scaffold, pull updates, or update the template; do not invoke routinely."
---

# sync-scaffold skill

## Purpose

Pull upstream improvements to the scaffold (new lint checks, schema refinements, additional reference categories, bug fixes) into this family's instance **without** overwriting their data.

The split between upstream-tracked and instance-only files is authoritative in [`UPSTREAM.md`](../../../UPSTREAM.md). Consult it before doing anything.

## Write-scope rule

**You must not write to an upstream-tracked file outside of this sync flow** without first asking the user and confirming they understand the change will be overwritten on the next sync. Family-specific data lives in `AGENTS.family.md` (instance-only), and any host-application overlay lives in `AGENTS.overlay.md` (instance-only, gitignored) — neither is touched by this flow.

The sync process respects these boundaries. Honor them when editing manually too.

## When to run

- User asks (`/sync-scaffold`, "pull scaffold updates", "update the template").
- Before a big schema-dependent task (e.g. adding a new category type) if the user wants the latest scaffold first.

Do **not** run this routinely or on a timer. Updates can change agent-visible behavior; the user should initiate.

## Prerequisites

1. Working tree is clean. If it isn't, refuse and ask the user to commit or stash first. Do not stash silently.
2. An upstream URL is available. Source of truth, in order: (a) a one-line `.scaffold-upstream` file at the repo root, (b) the canonical default `https://github.com/jrokeach/when-you-were`, (c) a URL the user provides when prompted to override. If the `upstream` git remote doesn't exist, offer to add it.

## Process

### 1. Read the upstream URL

```bash
cat .scaffold-upstream 2>/dev/null
```

If the file exists, use its contents. If not, fall back to the canonical default `https://github.com/jrokeach/when-you-were` — surface it to the user and ask whether to proceed with that URL or override. Offer to save the chosen URL as `.scaffold-upstream` so future syncs don't prompt.

### 2. Configure and fetch

```bash
git remote get-url upstream 2>/dev/null || git remote add upstream <url>
git fetch upstream
```

Confirm the upstream default branch (usually `main`). The rest of this doc assumes `upstream/main`.

### 2.5. Read the overlay's `instance_protected_paths` (if any)

Before computing the diff, check whether `AGENTS.overlay.md` exists at the repo root. If it does, parse its YAML and read the `instance_protected_paths:` list. This is the host application's declaration of upstream-tracked files it has customized and wants sync to **skip**. Typical entries: `README.md`, per-category `README.md` files the host has rebranded, or other scaffold-shipped user-facing documents.

- If the list is absent or empty, proceed normally.
- If the list contains paths, remember them and skip them in step 5 below. In step 4, surface the skip list to the user: "The overlay asks me to skip N paths on sync: [list]. I'll show you upstream changes to those paths but will not apply them — you can hand-merge later if you want."
- Paths outside the upstream-tracked list are ignored (can't protect something that isn't synced in the first place; surface that as a warning: "overlay declared `foo.md` as protected but it isn't upstream-tracked; nothing to protect").

### 3. Compute diff for upstream-tracked paths only

Upstream-tracked paths (authoritative list in `UPSTREAM.md`):

- `AGENTS.md`
- `AGENTS.family.md.example`
- `AGENTS.overlay.md.example`
- `AGENTS.local.md.example`
- `PRIVACY.md`, `LICENSE.md`, `CONTRIBUTING.md`, `UPSTREAM.md`, `STORAGE.md`
- `.gitignore`
- `.claude/**`
- `wiki/children/_template/**`
- `wiki/family/_examples/**`
- `wiki/family/*/README.md`
- `raw/README.md`, `raw/.gitkeep`

For each:

```bash
git diff HEAD upstream/main -- <path>
```

If the diff is empty, skip. Otherwise collect it.

**Never include any path outside this list.** If `git diff upstream/main` shows changes to an instance-only file, that means the upstream drifted from this instance in a way that touches your real content — report it to the user and stop; do not apply.

### 4. Show the combined diff to the user

Summarize by file: how many files changed, which ones, a short description of each. Include the full diff if small; for large diffs, offer a file-by-file walkthrough.

Wait for user approval before applying anything.

### 5. Apply

For each approved path **not** in the overlay's `instance_protected_paths` list from step 2.5:

```bash
git checkout upstream/main -- <path>
```

For each path that **is** in `instance_protected_paths`: **skip** the checkout. Do not apply upstream changes to protected paths. After the apply step, report: "Skipped N instance-protected paths: [list]. Upstream changes to those paths are visible in the diff above — hand-merge if desired."

`AGENTS.md` has no protected region — it is upstream-tracked in full. Family-specific data lives in `AGENTS.family.md` (instance-only, never included in the diff), so the sync is a straight file replacement.

If `AGENTS.family.md` does not exist locally but the upstream scaffold expects it, that is a bootstrap state — surface it to the user rather than auto-creating the file.

### 6. Lint

Run the `/lint` skill against the updated tree. Report any new findings introduced by the sync. The user should see any issues before committing.

### 7. Commit and (optionally) push

Compose a commit message describing what changed, referencing the upstream commit range:

```
Sync scaffold from upstream (<old-sha>..<new-sha>)

Files updated: [list]
```

Honor `auto_commit` / `auto_push` from `AGENTS.local.md`:

- If `auto_commit: true` and `privacy_acknowledged: true`, commit.
- Otherwise, stage and show the user the diff; wait for approval.
- If `auto_push: true`, push after committing.

## Safety rails

- Never touch any path not listed as upstream-tracked.
- Never delete instance-only files.
- Never force-push.
- Never run with a dirty working tree.
- If anything is ambiguous (unexpected file in the tracked list, diff shows instance-file changes, schema change that affects the layer chain), stop and escalate to the user.

Explicit "never touch" paths (instance-only; the skill refuses to include these in any diff or apply step):

- `AGENTS.family.md` (instance-only; user's family data).
- `AGENTS.overlay.md` (instance-only + gitignored; optional overlay injected by a host application).
- `AGENTS.local.md` (gitignored; per-user preferences).
- `.claude/skills.overlay/**` (gitignored; host-app-injected skills).
- `.claude/hooks.overlay/**` (gitignored; host-app-injected hook scripts).
- `.claude/settings.local.json` (gitignored; Claude Code's per-user / overlay settings layer).
- `.local/**` (gitignored; instance-only scratch/upgrade notes).
- `wiki/family/*/index.md` (per-category content listings — `*` means real category dirs like `pets/`, `relatives/`, `caregivers/`, etc. `_examples/index.md` and `_template/index.md` are part of the reference subtrees and ARE upstream-tracked). Scaffold ships initial placeholders for real categories; instance maintains thereafter — same class as `wiki/index.md`.
- `wiki/children/<real-slug>/**/index.md` (lazy-created per-subcat indexes in real child directories).
- `wiki/index.md`, `wiki/log.md`, `wiki/audit-log.md`, `wiki/contradictions.md`, `wiki/todo.md`, `wiki/timeline.md`.
- Plus any paths listed in `AGENTS.overlay.md`'s `instance_protected_paths:` field (host-declared; see step 2.5).

The `.example` counterparts (`AGENTS.family.md.example`, `AGENTS.overlay.md.example`, `AGENTS.local.md.example`) are upstream-tracked schema templates and ARE synced.

## What this skill does NOT do

- Does not sync `AGENTS.family.md`, `AGENTS.overlay.md`, or `AGENTS.local.md` (instance-only).
- Does not touch `wiki/children/<real-slug>/**` or `wiki/family/**` real content.
- Does not overwrite per-directory `index.md` files in real (non-`_examples/`, non-`_template/`) content directories. Those are instance-maintained — the scaffold ships initial placeholders and the instance takes it from there.
- Does not resolve merge conflicts inside upstream-tracked files that have been customized locally — if a local customization exists, surface it and let the user decide (keep local / take upstream / hand-merge).
- Does not push without explicit per-repo consent.
