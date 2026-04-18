# When You Were

A downloadable scaffold for a family-scoped, LLM-maintained knowledge base about your kids — milestones, memories, quotes, preferences at each age, relationships, creative works — so that years from now, both you and they have a curated history of their childhood to look back on.

Both **practical** (health, education, routines) and **emotional** (quotes, letters, reflections). Works with any LLM agent that reads `AGENTS.md`; has extra integration for Claude Code.

Built on the [LLM wiki pattern](https://gist.github.com/jrokeach/1d21067027d50ec384dcbcb56536ea94): raw sources + LLM-generated wiki pages + a schema document that teaches the agent how to maintain it.

---

## Is this for me?

It is if any of the following is true:

- You have kids and you've noticed how fast their words, fears, fascinations, and friendships drift away.
- You're already taking photos and notes in scattered places (Notes app, camera roll, texts to your partner) and wish it all lived somewhere durable.
- You want both of you *and your kids later* to be able to explore it.
- You're comfortable editing markdown files with an AI agent's help.

## How it works, in one paragraph

You clone this scaffold into a **private** repo. On first use, an AI agent reads `AGENTS.md`, asks you some bootstrap questions about your family, and fills in the Family details section of `AGENTS.md` (family-level data — children, household, tone, sensitive topics). It also creates a local `AGENTS.local.md` for your per-user, per-machine preferences (auto-commit behavior, prompt intervals). From then on, you paste photos, type a quote your kid said at dinner, drop in a report card — and the agent files it into the right places, cross-links it to related pages, and keeps a chronological log. Periodically, it prompts you for what's new and asks to lint the KB for typos, broken links, and stale pages.

## Working with your KB

The scaffold is just markdown + YAML frontmatter + an `AGENTS.md`. That means lots of tools work with it. Pick by what you're trying to do.

### Curating the KB (IDE-style coding agents)

For when you sit down at your computer to ingest a batch of material, lint, or reorganize.

- **Claude Code** — first-class support. `.claude/` ships with a `SessionStart` hook that nudges you on stale captures and lint cycles, plus `/lint` and `/sync-scaffold` skills.
- **OpenAI Codex (CLI)** — reads `AGENTS.md` natively. Works out of the box.
- **GitHub Copilot (chat)** — reads `AGENTS.md` in most integrations; point it at the file if it isn't auto-detected.
- **Cursor** — add a one-liner to `.cursorrules` or project settings referencing `AGENTS.md`.
- **opencode** — open-source TUI. Reads `AGENTS.md`.
- **Any `AGENTS.md`-aware agent** — Zed AI, Windsurf, Aider, and others work as long as they follow the `AGENTS.md` convention.

### Capturing on the go (chat-based personal assistants)

For when a kid says something funny at the park and you want to log it before you forget.

- **[OpenClaw](https://openclaw.ai/)** — personal AI assistant reachable via WhatsApp, Telegram, Discord, etc. Its GitHub and Obsidian integrations let you say "Ava said X at dinner tonight" into a chat and have it ingest the quote into the right page.
- **Claude Cowork** — Anthropic's team-collaboration layer. Reads `AGENTS.md`.
- **Any LLM chat with Git or filesystem access (via MCP)** — if it can read/write your repo, it can capture.

### Reading and browsing the KB

For everyday reference — looking back on what you wrote, pulling up a memory, or (eventually) sharing with the kid.

- **Your git forge of choice** — GitHub, GitLab, Gitea. Renders markdown, follows relative links across pages.
- **Obsidian** — open the repo as a vault. All links work. The Dataview plugin can query `subjects:` frontmatter for cross-child views.
- **iA Writer, Typora, Marked, any markdown viewer** — file-by-file reading.

### Querying the KB

For asking questions of the archive.

- **Ask an agent**: *"What was Ava scared of at age 4?"* — the agent searches `subjects:` frontmatter and page content.
- **Command line**: `grep -l 'subjects:.*ava' wiki/**/*.md` lists every page about Ava, regardless of directory.
- **Obsidian Dataview**: a `dataview` code block with `TABLE date, type FROM "wiki" WHERE contains(subjects, "ava") SORT date` renders a chronological Ava timeline.

## Quickstart

1. **[READ `PRIVACY.md` FIRST.](PRIVACY.md)** This KB will grow to contain deeply personal content about minors. Most families should not host it in a public repo.
2. Clone or download this template into a new **private** repository (or keep it local-only with encrypted backups).
3. Open the project with your AI agent (Claude Code, or any agent that reads `AGENTS.md`).
4. Ask it: *"Help me set this up."* The agent will read `AGENTS.md`, walk you through bootstrap, fill in the Family details section of `AGENTS.md`, and generate your `AGENTS.local.md`.
5. Start capturing. Paste quotes, photos, stories, observations. The agent handles the filing.

## What's in the scaffold

- [`AGENTS.md`](AGENTS.md) — schema, workflow, and operating manual for the agent; also the canonical home of family-specific details (children, household, tone, sensitive topics) once bootstrap has populated them
- [`AGENTS.local.md.example`](AGENTS.local.md.example) — template for **your** user- and machine-specific preferences (auto-commit, auto-push, prompt cadences, personal tone overrides). Different family members can keep different copies; it is not meant to be shared across users.
- [`PRIVACY.md`](PRIVACY.md) — privacy guidance. Read before committing anywhere.
- [`wiki/`](wiki/index.md) — where your knowledge base lives. Start at [`wiki/index.md`](wiki/index.md).
- [`raw/`](raw/) — drop zone for source material (photos, scans, transcripts) the agent can ingest.
- [`.claude/`](.claude/) — Claude Code integration (a `SessionStart` hook + a `/lint` skill). Safe to ignore if you use a different agent.

## Categories covered

The scaffold ships with a rich set of page types — both obvious (firsts, milestones, health, education) and less obvious (quotes, questions, fears, character moments, letters, reflections, aspirations, heroes, routines). See [`wiki/children/_template/`](wiki/children/_template/) for the full per-child menu and [`wiki/family/`](wiki/family/) for whole-family categories. The template is a menu, not a mandate — skip what doesn't fit your family.

## Multi-child support

Multi-child by default. Shared content (family trips, sibling dynamics, a grandparent's funeral) is handled through a **`subjects:`** frontmatter field rather than directory duplication. See the "Shared / cross-child content" section of [`AGENTS.md`](AGENTS.md) for how that works.

## Contributing / forking

This is a scaffold. If you fork it with improvements to the structure, AGENTS.md, or lint skill, PRs welcome — but **never** push a fork that contains your family's actual content. The template itself ships empty; `AGENTS.local.md` and any content under `wiki/children/` or `raw/` should only exist in your private instance.

## Licensing

This scaffold is dual-licensed:

- **PolyForm Noncommercial 1.0.0** — the default license. Free for personal, educational, research, and noncommercial use. Commercial users must contact the author for a separate commercial license.
- **Commercial license** — available upon request. Contact the author to negotiate terms.

The full license text is in [`LICENSE`](LICENSE.md).

This pattern — restrictive first, more permissive later — is intentional. As the sole copyright holder, I retain the ability to relicense to MIT, Apache-2.0, or another open source license in the future if the project gains enough momentum to warrant it. The [DCO notice](CONTRIBUTING.md) in CONTRIBUTING.md ensures any external contributions can be included in a future relicensing.

## Your KB starts here

Once you've instantiated this scaffold, your knowledge base lives at [`wiki/index.md`](wiki/index.md). That's where to navigate from, day-to-day.
