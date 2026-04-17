---
title: "Index"
type: meta
subjects: [family]
status: active
---

# Index

Entry point for this knowledge base. If you're coming here for the first time, read the top of `AGENTS.md` for the philosophy and then browse this page.

---

## Children

_The agent populates this section when you add children during bootstrap. Each entry links to that child's `profile.md` and summarizes their top-level categories._

<!-- children-index-begin -->

Example (remove when real entries are added):

```
- **Ava** — born YYYY-MM-DD — [profile](children/ava/profile.md)
- **Noah** — born YYYY-MM-DD — [profile](children/noah/profile.md)
```

For an instantiated example of what a per-child directory looks like, see [the _template/ reference](children/_template/profile.md).

<!-- children-index-end -->

### Finding everything about one child

Per-child directories are a placement convention, not the full scope of a child's content. To find everything about a given child, search the `subjects:` frontmatter field across the entire wiki:

```bash
grep -l 'subjects:.*ava' wiki/**/*.md
```

Or ask the agent: *"Show me everything about Ava."*

---

## Family

Content that belongs to the whole family or to relationships between kids rather than any one child:

- [Homes](family/homes/README.md) — places the family has lived
- [Caregivers](family/caregivers/README.md) — nannies, teachers, coaches, other regular adults
- [Traditions](family/traditions/README.md) — holiday rituals, weekly rhythms, family traditions
- [Lore](family/lore/README.md) — stories the family tells about the kids
- [Trips](family/trips/README.md) — family trips (individual kids cross-link their own moments)
- [Relatives](family/relatives/README.md) — extended family
- [Pets](family/pets/README.md) — family pets (per-kid relationships live in `children/<slug>/pets/`)
- [Shared memories](family/shared-memories/README.md) — discrete shared events
- [Shared firsts](family/shared-firsts/README.md) — firsts for the family unit
- [Shared milestones](family/shared-milestones/README.md) — moves, new siblings, other family-level milestones
- [Sibling dynamics](family/sibling-dynamics/README.md) — relationships and patterns between siblings

---

## Per-child categories

Each child's directory (`children/<slug>/`) contains these subdirectories. See [the template](children/_template/profile.md) for the canonical shape of each page type.

**Emotional-texture categories:**

- `quotes/` — kid-isms, mispronunciations, things they say
- `questions/` — profound or funny things they've asked
- `fears/` — what scared them at each age
- `character-moments/` — moments of kindness, courage, honesty
- `letters/` — letters from family *to* them
- `reflections/` — your observations over time
- `aspirations/` — what they want to be when they grow up, year over year
- `heroes/` — who they look up to

**Practical-but-usually-lost categories:**

- `physical/` — height, weight, shoe size, distinguishing features over time
- `routines/` — bedtime, lovies, daily rhythms at ages
- `friends/` — who they're closest to at each age
- `pets/` — their relationships with family pets
- `gifts/` — significant gifts, who gave them, why they mattered

**Standard:**

- `firsts/`, `milestones/`, `memories/`, `preferences/`, `health/`, `education/`, `interests/`, `travel/`, `achievements/`, `creative-works/`, `losses/`

---

## Meta pages

- [Change log](log.md) — append-only record of what's been ingested and when
- [Audit log](audit-log.md) — findings from lint runs
- [Contradictions](contradictions.md) — documented disputes between sources
- [TODO](todo.md) — living task list
- [Timeline](timeline.md) — chronological view across all children

---

## Conventions (quick reference)

- **Subject field** — every content page has `subjects:` listing kid slugs or `family`. See `AGENTS.md` "Shared / cross-child content".
- **Links** — standard markdown links with relative paths: `[label](relative/path.md)`. Works in both Obsidian and GitHub.
- **Filenames** — kebab-case. Date-prefixed for events: `2024-03-<slug>.md`.
- **No duplication** — one canonical page per event; cross-reach via `subjects:` and links.
