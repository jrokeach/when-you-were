---
name: sync-scaffold
description: "Pull upstream improvements from the When You Were scaffold template into this instance, preserving family-specific data. Handles AGENTS.md Family details block protection, refuses to touch instance-only paths, surfaces diffs for user review before applying, runs /lint after. Invoke when the user asks to sync the scaffold, pull updates, or update the template; do not invoke routinely."
---

# sync-scaffold skill

## Purpose

Pull upstream improvements to the scaffold (new lint checks, schema refinements, additional reference categories, bug fixes) into this family's instance **without** overwriting their data.

The split between upstream-tracked and instance-only files is authoritative in [`UPSTREAM.md`](../../../UPSTREAM.md). Consult it before doing anything.

## Write-scope rule

**You must not write to an upstream-tracked file outside of this sync flow** without first asking the user and confirming they understand the change will be overwritten on the next sync. Inside `AGENTS.md`, only the `<!-- FAMILY_DETAILS_BEGIN -->` / `<!-- FAMILY_DETAILS_END -->` block is instance-owned.

The sync process respects these boundaries. Honor them when editing manually too.

## When to run

- User asks (`/sync-scaffold`, "pull scaffold updates", "update the template").
- Before a big schema-dependent task (e.g. adding a new category type) if the user wants the latest scaffold first.

Do **not** run this routinely or on a timer. Updates can change agent-visible behavior; the user should initiate.

## Prerequisites

1. Working tree is clean. If it isn't, refuse and ask the user to commit or stash first. Do not stash silently.
2. `AGENTS.md` contains both `<!-- FAMILY_DETAILS_BEGIN -->` and `<!-- FAMILY_DETAILS_END -->` markers. If either is missing, abort and explain — the user's local `AGENTS.md` has been edited in a way that breaks merging, and they need to restore the markers before sync can run.
3. An upstream URL is available. Source of truth, in order: (a) a one-line `.scaffold-upstream` file at the repo root, (b) the canonical default `https://github.com/jrokeach/when-you-were`, (c) a URL the user provides when prompted to override. If the `upstream` git remote doesn't exist, offer to add it.

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

### 3. Preserve the Family details block

Before any merging, capture the current Family details region from the live `AGENTS.md`:

- Read `AGENTS.md`.
- Extract everything between (and including) `<!-- FAMILY_DETAILS_BEGIN -->` and `<!-- FAMILY_DETAILS_END -->`.
- Store it in memory (or a tmp file).

### 4. Compute diff for upstream-tracked paths only

Upstream-tracked paths (authoritative list in `UPSTREAM.md`):

- `AGENTS.md`
- `AGENTS.local.md.example`
- `PRIVACY.md`, `LICENSE.md`, `CONTRIBUTING.md`, `UPSTREAM.md`
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

### 5. Show the combined diff to the user

Summarize by file: how many files changed, which ones, a short description of each. Include the full diff if small; for large diffs, offer a file-by-file walkthrough.

Wait for user approval before applying anything.

### 6. Apply

For each approved path except `AGENTS.md`:

```bash
git checkout upstream/main -- <path>
```

For `AGENTS.md`:

- `git checkout upstream/main -- AGENTS.md` to get the upstream version into the working tree.
- Locate the `FAMILY_DETAILS_BEGIN/END` markers in the upstream version.
- Replace the upstream's placeholder block with the preserved block captured in step 3.
- If the upstream version removed or renamed the markers, abort and ask the user — this indicates an intentional schema change that needs human review.

### 7. Lint

Run the `/lint` skill against the updated tree. Report any new findings introduced by the sync. The user should see any issues before committing.

### 8. Commit and (optionally) push

Compose a commit message describing what changed, referencing the upstream commit range:

```
Sync scaffold from upstream (<old-sha>..<new-sha>)

Files updated: [list]
Preserved: AGENTS.md Family details block
```

Honor `auto_commit` / `auto_push` from `AGENTS.local.md`:

- If `auto_commit: true` and `privacy_acknowledged: true`, commit.
- Otherwise, stage and show the user the diff; wait for approval.
- If `auto_push: true`, push after committing.

## Safety rails

- Never touch any path not listed as upstream-tracked.
- Never delete instance-only files.
- Never remove the `FAMILY_DETAILS_BEGIN/END` markers; abort if they are missing from local or upstream.
- Never force-push.
- Never run with a dirty working tree.
- If anything is ambiguous (marker renamed upstream, unexpected file in the tracked list, diff shows instance-file changes), stop and escalate to the user.

## What this skill does NOT do

- Does not sync `AGENTS.local.md` (user's per-user preferences — not upstream-tracked).
- Does not touch `wiki/children/<real-slug>/**` or `wiki/family/**` real content.
- Does not resolve merge conflicts inside upstream-tracked files that have been customized locally — if a local customization exists, surface it and let the user decide (keep local / take upstream / hand-merge).
- Does not push without explicit per-repo consent.
