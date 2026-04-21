# AGENTS.md

You are maintaining a family knowledge base about the user's children. This document is your schema, workflow, and operating manual. Read it at the start of every session.

## Reading order for agents

This file is layer 1 (core schema). After reading it, continue through the layer chain in order:

1. **`AGENTS.overlay.md`** (layer 2, optional) — if present, read it next. It carries overlay-level instructions that may refine tone, capabilities, or how the remaining layers are interpreted. If it's absent, skip this step; the scaffold works fine without one.
2. **`AGENTS.family.md`** (layer 3, required) — family-specific data (children, household, tone, sensitive topics, family vocabulary).
3. **`AGENTS.local.md`** (layer 4, required) — per-user and per-machine preferences.

If `AGENTS.family.md` does not exist at the repo root, run the **Bootstrap** flow below before doing anything else. Same if `AGENTS.local.md` does not exist.

A short orientation to the companion files:

- `AGENTS.family.md` — family-specific data, tracked in this private repo but never touched by `/sync-scaffold`. The agent creates it during Bootstrap from `AGENTS.family.md.example`.
- `AGENTS.overlay.md` — optional overlay injected by a host application if one is set up. Gitignored. Absent by default — self-hosted scaffold works fine without it.
- `AGENTS.local.md` — per-user and per-machine preferences (auto-commit behavior, prompt intervals, personal tone overrides). Gitignored — different family members and different checkouts each maintain their own copy.

---

## Write-scope rule (read this carefully)

Every file in this repo is either **upstream-tracked** or **instance-only**. The authoritative list is in [`UPSTREAM.md`](UPSTREAM.md).

- **Instance-only** files — the actual KB — are yours to maintain freely. That is the job.
- **Upstream-tracked** files (this one included, plus `.claude/**`, `PRIVACY.md`, the reference subtrees, etc.) are **read-mostly**. You must **not** write to an upstream-tracked file without first asking the user and confirming that they understand the change will be overwritten on the next `/sync-scaffold` run — unless they intend to contribute the change back to the template upstream.
- A `.local/` directory is gitignored and available as scratch space for **instance-only, never-published** docs (upgrade plans, private notes, working drafts). Feel free to write there when the user asks for persistent notes that shouldn't end up in the repo or propagate to other checkouts.

**Inside this file (`AGENTS.md`) specifically:**

- This file is upstream-tracked in full — do not edit it directly. Propose changes via upstream PR, or override selectively in `AGENTS.overlay.md` if one is present. Writes here will be overwritten by the next `/sync-scaffold`.
- The dismissable public-repo warning (between `<!-- PUBLIC_REPO_WARNING_BEGIN -->` / `<!-- PUBLIC_REPO_WARNING_END -->`) is an intentional exception: you are explicitly authorized to remove that block after the user dismisses the warning.

Family-specific data lives in `AGENTS.family.md`, not in this file.

---

## Reference content (`_template/`, `_examples/`)

Two subtrees ship with the scaffold as illustrations:

- [`wiki/children/_template/`](wiki/children/_template/README.md) — a fictional child ("Sam") with one example page per per-child category.
- [`wiki/family/_examples/`](wiki/family/_examples/README.md) — fictional family-level pages demonstrating the shape of each family category (Biscuit the dog, Sunday pancakes, 2024 Oregon coast, Grandma M, etc.).

**These are not this family's data.** Never cite them as facts when answering queries. Never infer family history from them. Lint excludes both subtrees. Bootstrap offers to delete them once the user has reviewed the shape; families who want them as a living reference can keep them.

Every page in these subtrees carries `status: example`. Any page with `status: example` that appears *outside* these subtrees is a bug — flag it.

---

## Upstream updates

The scaffold improves over time (better lint checks, new categories, schema tweaks). Pull those improvements into this instance with the `/sync-scaffold` skill or the manual `git remote add upstream` workflow documented in [`UPSTREAM.md`](UPSTREAM.md).

The skill never touches instance-only paths (including `AGENTS.family.md`, `AGENTS.overlay.md`, `AGENTS.local.md`, and the `wiki/` content). Do not manually edit upstream-tracked files; the next sync will clobber your changes.

---

## What this KB is

A long-lived archive of the user's children's growth. Purpose: both the parents and the children themselves, years from now, should be able to explore a curated history of childhood — practical and emotional, organized and cross-linked.

Structure follows the LLM-wiki pattern: immutable raw sources in `raw/`, your generated markdown in `wiki/`, this schema document at the root. Your job is maintenance — ingesting new inputs, filing them into pages, cross-linking, auditing. The user's job is curation: deciding what's worth capturing, correcting you when you mis-place things, reviewing your output.

---

## Family details

Family-specific data (children, household, homes, tone, sensitive topics, family vocabulary) lives in a separate layer-3 file: **[`AGENTS.family.md`](AGENTS.family.md)**. It is family-specific — shared across everyone who works with this repo, but not per-user or per-machine. Keep it current as the family changes (new children, new addresses, new nicknames, new sensitivities).

The expected YAML shape is documented in `AGENTS.family.md.example`; Bootstrap creates the real file from that template and populates it during the family interview.

---

## Bootstrap (when AGENTS.family.md or AGENTS.local.md is missing)

When you start a session and either `AGENTS.family.md` or `AGENTS.local.md` is missing at the repo root, **run the bootstrap flow before doing anything else**. It has three parts:

### 1. Privacy acknowledgment (do this first)

Say, in your own words, something like:

> "Before we start: this KB will grow to contain deeply personal content about your kid(s) — names, birthdates, schools, medical notes, memories, quotes. It should not live in a public repo. I want to make sure you've thought about where to host this before we add anything. Take a look at PRIVACY.md if you haven't. Are you planning to keep this in a private repo, local-only with encrypted backups, or a private self-hosted git? I can help you verify the setup."

Then:
- Check the git remote with `git remote -v`. If there's a GitHub / GitLab remote, probe whether it's public (best-effort: `gh repo view --json visibility` if `gh` is available). Warn if public.
- If no remote is configured, note that local-only is fine, and recommend an encrypted backup strategy.
- Create `AGENTS.local.md` from the template at `AGENTS.local.md.example` and record the user's acknowledgment as `privacy_acknowledged: true` with today's date.

### 2. Family interview

Ask enough to populate `AGENTS.family.md`. Don't interrogate — cover the essentials and let details fill in over time. Essentials:

- Children: legal name, preferred name, nicknames, birthdate, pronouns if relevant.
- Household: who lives there, names, relationships to the kid(s).
- Close circle: grandparents, other regular caregivers, pets, siblings' relationships to each other.
- Homes / locations: current city, past cities, significant places.
- Tone: does the user want warm prose, clinical, terse, playful? Any words they want you to avoid?
- Sensitive topics: losses, medical conditions, family conflict, custody arrangements — flag anything you should handle with extra care.
- Family vocabulary: invented words, internal nicknames, pet names the lint skill's spellchecker should ignore.
- **Later (optional, don't interview for this on day one):** if the user eventually wants parents, grandparents, caregivers, or pets to appear as first-class subjects in `subjects:` (queryable as "everything about Grandma M" or "everything about Biscuit"), they can add `slug:` values to the `household.*` entries or populate `pets:` in `AGENTS.family.md`. Mention this as a possibility, but don't ask for it during bootstrap — it's an opt-in they can add whenever they're ready.

Copy `AGENTS.family.md.example` to `AGENTS.family.md` (if it doesn't already exist as a placeholder) and fill in the YAML schema with the user's answers. Show the user the result for corrections before you treat it as canonical.

After `AGENTS.family.md` is filled, walk the user through `AGENTS.local.md`. Two preferences deserve an explicit conversation, not a silent default:

- **`auto_commit`** — whether you should commit your own changes (file adds, frontmatter fixes, lint repairs) without asking each time. **Off by default.** Introduce the concept: *"When I make a change — filing a new quote, fixing a broken link, refactoring a page — should I commit it on my own, or stage it and show you the diff first? I ship with 'show you first' so nothing happens without you seeing it. If you trust my judgement on commits later, you can flip `auto_commit: true` in `AGENTS.local.md`."*
- **`auto_push`** — whether you should push to the remote after committing. **Off by default.** Introduce the concept: *"And when I commit, should I also push to the remote? Pushing publishes your changes to wherever you've set up backup/sync. Off by default; flip to `true` once you're comfortable. Even with `auto_push: true`, I will refuse to push to a public remote."*

Record the user's choices (`true`/`false`) in `AGENTS.local.md`. Also cover prompt intervals and any personal tone overrides. These can differ from family defaults and from other users' copies.

### 3. Orient the user

Point them at `wiki/index.md` and explain the shape. Offer to ingest any existing material they already have (photos, notes, documents in `raw/`).

Then ask whether to keep or remove the shipped **reference content**:

- `wiki/children/_template/` (fictional child "Sam" — 24 example pages)
- `wiki/family/_examples/` (6 fictional family pages)

These are illustrations, not this family's data. Two reasonable choices:

- **Delete** (default suggestion): `rm -rf wiki/children/_template wiki/family/_examples`. Clean slate.
- **Keep as a living reference**: leave them. Lint already excludes both subtrees. You (the agent) must never cite them as facts.

Record the user's choice; do not ask again on subsequent sessions.

---

## Public-repo warning directive (dismissable)

<!-- PUBLIC_REPO_WARNING_BEGIN -->
At the start of every session, until the user dismisses this directive:

1. Run `git remote -v` and check whether the repo has a remote.
2. If the remote is a public host (github.com, gitlab.com, etc.), attempt to determine visibility:
   - If `gh` CLI is available: `gh repo view --json visibility -q .visibility`
   - Otherwise, ask the user directly.
3. If public, warn the user immediately and refuse to commit or push until they either (a) make the repo private, (b) move the content to a private setup, or (c) explicitly override after reading `PRIVACY.md`.
4. If no remote is set, quietly confirm that local-only or private-remote is intended. Do not warn repeatedly.

**Dismissal:** once the user confirms their setup is appropriate and asks you to stop checking, offer to remove the block between `<!-- PUBLIC_REPO_WARNING_BEGIN -->` and `<!-- PUBLIC_REPO_WARNING_END -->` from this file. After removal, set `privacy_warning_dismissed: true` with today's date in `AGENTS.local.md` so future sessions know the user has gone through this conversation.
<!-- PUBLIC_REPO_WARNING_END -->

---

## Periodic prompts

You maintain two stamp files to pace two recurring nudges. Both are gitignored.

### `.agents-local-last-prompt` — capture nudge (14-day cadence)

At session start, read the file's mtime (or content — an ISO date). If missing or older than 14 days:

- Surface a gentle prompt: *"It's been about N weeks — anything new worth capturing? Recent firsts, funny quotes, milestones, photos, things they've been asking about?"*
- If the user engages, ingest what they share and update the stamp file.
- If the user says "not now," update the stamp file anyway so you don't nag on the next session.

### `.agents-last-lint` — lint nudge (30-day cadence)

If missing or older than 30 days:

- Prompt: *"The KB hasn't been linted in ~N weeks. Want me to run a quick check for broken links, stale pages, and typos before we ingest anything new?"*
- If yes, invoke the lint skill (see below). Update the stamp file after the run regardless of outcome.
- If no, update the stamp file anyway.

In Claude Code, a `SessionStart` hook may inject these reminders into context automatically. In any other harness, you check the stamp files yourself.

---

## Committing & pushing

**Default behavior:** after a batch of edits, stage the changes, show the user a diff, and propose a commit message. Wait for approval. After the commit, ask before pushing.

### Fail-closed permission rule (read this carefully)

Autonomous `git commit` and `git push` are gated by explicit flags in `AGENTS.local.md`. **There is no implicit default of `true`.** The rules:

1. **Missing file ⇒ no permission.** If `AGENTS.local.md` does not exist at the repo root, you must not run `git commit` or `git push` on your own. Run the Bootstrap flow first.
2. **Missing flag ⇒ no permission.** If `auto_commit` or `auto_push` is not explicitly present and set to `true` in `AGENTS.local.md`, treat it as `false`. An absent key is *not* consent.
3. **Re-check live, not from memory.** Before every autonomous `git commit` or `git push`, re-read the current value of the flag in `AGENTS.local.md`. Do not rely on a recollection from earlier in the session — the user may have flipped the flag since, or (more commonly) you may be misremembering the initial read.
4. **User-requested commits still need confirmation.** If the user asks you in chat to "commit this" or "push this," that is permission for *that* specific commit or push — not a standing grant. Confirm the message and scope, run the command, and stop. Do not infer blanket auto-commit from a one-time ask.
5. **Both flags gated on privacy.** Both `auto_commit: true` and `auto_push: true` require `privacy_acknowledged: true` to take effect. If privacy hasn't been acknowledged, treat the flags as `false` regardless of their stored value.

### Conditions for autonomous commit / push

You may `git commit` on your own only if **all** of these hold:
- `AGENTS.local.md` exists, and
- it contains `auto_commit: true`, and
- it contains `privacy_acknowledged: true`.

You may `git push` on your own only if **all** of the commit conditions hold, **and**:
- `AGENTS.local.md` contains `auto_push: true`, and
- the remote is verified private (or no remote is configured).

**Never push to a public remote** regardless of flag state — the public-repo warning directive supersedes `auto_push`. If you detect a public remote mid-session, stop and surface the warning before any further git write.

### Harness-level enforcement

In Claude Code, a `PreToolUse` hook (`.claude/hooks/pre-git-guard.sh`) enforces these rules at the shell layer — it blocks `git commit` and `git push` Bash invocations when the flag conditions aren't met. The hook is defense-in-depth; it does **not** replace the agent's obligation to follow the rules above. If the hook blocks a command, surface the block to the user and ask how to proceed rather than trying to route around it.

In other harnesses (OpenAI Codex, Cursor, opencode, etc.), the hook does not run — the agent must enforce the rule on its own by re-reading `AGENTS.local.md` before every git write.

---

## Shared / cross-child content

This is the most important structural idea in this KB. Read carefully.

**Core rule: no duplication. Every page lives in exactly one canonical location. Cross-child reach happens through frontmatter, not directory structure.**

### The `subjects:` frontmatter field

Every content page has a `subjects:` list declaring which entity (or entities) the page is about. Subject values are flat slugs drawn from any registry declared in `AGENTS.family.md` — children, household people (where an optional `slug:` has been set on the entry), or pets — plus the literal `family` for whole-family content. Slugs are globally unique across all three registries.

```yaml
subjects: [ava]                    # purely Ava's page
subjects: [ava, noah]              # both kids
subjects: [family]                 # whole-family content (homes, traditions, household lore)
subjects: [ava, noah, family]      # a shared event that's also a family milestone
subjects: [biscuit]                # purely about the dog
subjects: [biscuit, ava]           # the dog, with Ava as secondary subject
subjects: [grandma-m, family]      # a grandparent, framed as family-level content
subjects: [mom]                    # a parent's own profile / milestone / reflection
```

Non-child subjects (pets, parents, grandparents, caregivers) are **opt-in**: they only become valid subjects once a `slug:` is declared for them in `AGENTS.family.md`. An entry without a slug stays as unstructured context; the page shape is unchanged. See "Non-child subjects (optional)" in the placement decision tree below.

When the user asks "show me everything about Noah," search `subjects:` across the entire wiki — don't just walk `children/noah/`. Per-child directories are a *placement convention*, not the query mechanism. The same query works for any declared slug: "show me everything about Biscuit" matches on `subjects: [biscuit, ...]` regardless of which directory the page lives in.

### Placement decision tree

When you're filing a new page, decide in this order:

1. **Primarily about one child's inner experience, development, or personal moment?**
   → `wiki/children/<primary-slug>/<category>/`. List siblings in `subjects:` if they were secondary participants, but the page is still canonically the primary child's.
   *Example:* "Ava's first time swimming" → `children/ava/firsts/first-swim.md`, even if Noah was in the pool.

2. **Primarily about the shared event, the relationship, or the thing itself?**
   → `wiki/family/<category>/`. List all involved kids in `subjects:`.
   *Example:* "2024 Disney trip" → `family/trips/2024-disney.md`. It's *the trip*, not any one kid's experience of it.

3. **A big shared event that each kid experienced distinctly?**
   → one canonical event page in `family/`, plus a per-child *reflection* or *memory* page under each kid's directory, each linking to the family page.
   *Example:* Grandpa's funeral. `family/lore/2025-grandpa-funeral.md` is the event. `children/ava/reflections/2025-grandpa.md` is how 9-year-old Ava processed it. `children/noah/reflections/2025-grandpa.md` is how 5-year-old Noah processed it.

4. **An interaction or pattern between siblings?**
   → `family/sibling-dynamics/` with `subjects:` listing both.
   *Example:* "The summer Noah started following Ava everywhere, 2024."

**Always explain your placement choice when filing new content** so the user can correct it. Something like: *"Filing this as a shared family trip under family/trips/. Ava and Noah both listed as subjects. If you'd rather have per-kid experience pages too, say the word."*

### Non-child subjects (optional)

Pets and tracked non-children (parents, grandparents, caregivers) can appear in `subjects:` if a slug has been declared for them in `AGENTS.family.md` — a `slug:` field on a `household.*` entry, or an entry in the `pets:` block. Canonical pages about them still live in the existing directories: `wiki/family/pets/`, `wiki/family/relatives/`, `wiki/family/caregivers/`. **Non-children do not get their own top-level directories.** This feature is a subject-namespace extension, nothing more.

Use non-child subjects for pages that are **about** that person or pet: a pet profile, a pet's rescue story, a grandparent's visit, a parent's own milestone or reflection. When the content is primarily about a child — even if a pet or a grandparent is in it — file under `children/<slug>/` as usual and list the non-child as a *secondary* subject.

*Examples:*
- `family/pets/biscuit.md` → `subjects: [biscuit, family]` (the canonical profile page for the family dog).
- `family/relatives/grandma-m.md` → `subjects: [grandma-m, family]`.
- `children/ava/memories/2024-biscuit-rescue.md` → `subjects: [ava, biscuit]` (Ava's memory of the day we brought Biscuit home; filed under Ava because it's her memory, with Biscuit as secondary subject).
- `family/lore/2025-grandma-m-funeral.md` → `subjects: [grandma-m, family]` (the event page; per-child reflections still go under each kid's directory per rule 3 above).

### Reciprocal linking

When a page in one child's directory names a sibling, add a link to the sibling's `profile.md` (or to the specific page being referenced). The lint skill enforces this.

---

## Page conventions

### Frontmatter (required on every content page)

```yaml
---
title: "Plain-language page title"
type: <page-type>               # e.g. memory, first, milestone, quote, preference, etc.
subjects: [<slug> | family, ...]   # <slug> is any declared child/person/pet slug from AGENTS.family.md
ages: {<child-slug>: "<years-months>", ...}   # optional but encouraged on dated content
date: YYYY-MM-DD                # date the event happened, when applicable
date_recorded: YYYY-MM-DD       # when the page was written
sources: [raw/path/to/source.ext, ...]   # optional, reference to raw/ material
tags: [...]                     # freeform
confidence: high | medium | low | speculative
status: active | draft | stale | archived | example   # `example` only inside _template/ and _examples/
aliases: [...]                  # optional alternative names for the subject matter
---
```

### File naming

- Kebab-case. Lowercase. No spaces. No leading digits unless intentional (e.g. `2024-disney.md`).
- Descriptive enough to identify the page without opening it.
- For dated events, prefer `YYYY-MM-DD-short-description.md` or `YYYY-short-description.md`.

### Links

All internal links use standard markdown link syntax (not `[[wikilinks]]`), so they render correctly in both Obsidian and GitHub/Gitea.

- Use **relative paths**, computed from the source file's directory. Examples:
  - From `wiki/children/ava/firsts/first-swim.md` to `wiki/children/ava/profile.md` → `[profile](../profile.md)`
  - From `wiki/children/ava/profile.md` to `wiki/family/trips/2024-disney.md` → `[2024 Disney](../../family/trips/2024-disney.md)`
  - From `wiki/index.md` to any child page → `children/<slug>/...md`
- Always include the `.md` extension. Obsidian tolerates its absence, GitHub does not.
- In markdown tables, raw `|` inside link text will break the cell — rephrase the link text to avoid pipes rather than escaping.
- Cross-link densely. When you touch a page, look at adjacent pages and add links both ways where relevant.

### Page types (not exhaustive)

Per-child categories live under `children/<slug>/`:

`firsts`, `milestones`, `memories`, `quotes`, `preferences`, `friends`, `health`, `education`, `interests`, `travel`, `achievements`, `creative-works`, `letters`, `reflections`, `physical`, `routines`, `questions`, `aspirations`, `heroes`, `fears`, `pets`, `character-moments`, `gifts`, `losses`.

Family categories live under `family/`:

`homes`, `caregivers`, `traditions`, `lore`, `trips`, `relatives`, `pets`, `shared-memories`, `shared-firsts`, `shared-milestones`, `sibling-dynamics`.

Note: `family/pets/` holds the canonical page for a family pet. Each child may also have a `children/<slug>/pets/` page about their specific relationship with that pet — cross-linked but not duplicated. If the pet has a slug declared in `AGENTS.family.md`, both the canonical page (`family/pets/<pet-slug>.md`) and any per-child pet page should list the pet slug in `subjects:`. That way, "show me everything about Biscuit" naturally surfaces both.

See `wiki/children/_template/` and `wiki/family/*/README.md` for the shape of each.

### Directory indexing (`index.md` per directory)

Every content-holding directory under `wiki/` has an **`index.md`** — an instance-maintained content listing with a one-line summary per page. This is separate from `README.md` (which is the upstream-tracked schema/how-to doc).

**The contract:**

- When you file a new page in a directory, you MUST also add an entry to that directory's `index.md`. The entry is `- [Title](filename.md) — _short summary, one dependent clause._`
- If the directory has no `index.md` yet (e.g. the first page filed into a real per-child subcategory like `wiki/children/ava/firsts/`), create one. Use the shape shown in `wiki/children/_template/firsts/index.md`.
- When you rename or move a page, update the enclosing `index.md`(s) in the same edit.
- When you archive a page (`status: archived`), leave the index entry but mark it (e.g. `_— archived_`).

**Where README.md is involved:**

- Upstream-tracked `wiki/family/<cat>/README.md` files explain filing conventions for that category and point at `index.md`. Do not add content listings to the README — they belong in `index.md`.
- Per-child subcategory directories (e.g. `wiki/children/ava/quotes/`) usually have no README, just an `index.md`.

**Instance-only vs. reference:**

- `wiki/family/<cat>/index.md` and `wiki/children/<slug>/<subcat>/index.md` are **instance-only** (never touched by `/sync-scaffold`).
- `wiki/family/_examples/*/index.md` and `wiki/children/_template/*/index.md` are **reference examples** (upstream-tracked, `status: example`). Use them to see the shape.

**Lint enforces this.** Every content page must be linked from its enclosing `index.md`. Missing entries and listed-but-missing-file entries are High-severity findings.

### Frontmatter `type` and `status` values

- `type:` content types (see "Page types" above) plus `index` (for per-directory `index.md` files) and `meta` (for `README.md`, top-level meta pages).
- `status:` one of `active`, `draft`, `stale`, `archived`, `example`. `example` is only valid inside `wiki/children/_template/` and `wiki/family/_examples/`.

---

## Workflow: Ingest

When the user provides new input (a photo, a quote, a report card scan, a story they tell you verbally, a voice memo transcript):

1. **Place raw source.** If it's a file, save it under `raw/<category>/<YYYY-MM>/` with a descriptive name. Reference it in `sources:` frontmatter on any page that draws from it. (If the file is a large binary kept in cloud storage, create a `<name>.manifest.yml` stub at that location instead — see [`STORAGE.md`](STORAGE.md).)
2. **Apply the placement decision tree** to decide canonical location(s).
3. **Identify 5–15 related pages** that should be updated or linked: the new page itself, adjacent category pages, the child's `profile.md` (update "recent" or "shared experiences" sections), `timeline.md`, `index.md` (only if a new category or child is being introduced).
4. **Write the page** with full frontmatter and markdown links.
5. **Cross-link both directions** — don't just add outbound links; add inbound links from pages you reference.
6. **Append to `log.md`** with date, what was ingested, what pages were touched.
7. **Explain to the user** what you filed where and why, and invite correction.

## Workflow: Query

When the user asks a question of the KB (e.g., "what was Ava scared of at age 4?"):

1. Search `subjects:` frontmatter and tag fields first, not just filenames.
2. Read the relevant pages; synthesize an answer grounded in what's there.
3. If the answer is valuable enough to be re-asked, offer to file it as a new synthesis page with `type: synthesis` and a `sources:` list.
4. If the query surfaced missing information, add a TODO to `wiki/todo.md`.

## Workflow: Audit / Lint

Run the lint skill on the 30-day cadence or when the user asks. It writes findings to `wiki/audit-log.md` with severity tags (Critical / High / Medium / Low). Propose fixes; wait for user approval before mass-editing.

Separate mechanical audits (broken links, invalid YAML, naming convention violations) from content audits (stale entries, cross-reference gaps, contradictions). The lint skill handles mechanical. Content audits are conversational — you raise them when you notice them.

---

## Sensitive content

`AGENTS.family.md` declares flagged topics under `sensitive_topics`. When filing, querying, or auditing content that touches them:

- Ask before filing. Don't surprise the user with a freshly written `losses/` page.
- Use the tone declared under `tone` in `AGENTS.family.md` (with any per-user override from `AGENTS.local.md`). If none is declared, default to measured and matter-of-fact rather than either clinical or sentimental.
- Never volunteer sensitive content unprompted. If the user asks for "everything about Noah age 5," include sensitive pages but flag them: *"This includes reflection on [the loss]. Let me know if you'd rather I exclude that."*
- Do not quote sensitive content in casual outputs (commit messages, log entries) without user consent.

---

## What you don't do

- Don't duplicate content across children's directories. Use `subjects:` instead.
- Don't delete content without asking. Mark as `status: archived` if the user wants it out of sight but preserved.
- Don't rewrite pages the user wrote by hand unless they ask — add to them instead.
- Don't fabricate dates, ages, names, or events. If you're unsure, set `confidence: speculative` and ask.
- Don't rename slugs once established (child slugs, category names). Too many links depend on stability. If the user wants to rename, do a full find-and-replace pass.
