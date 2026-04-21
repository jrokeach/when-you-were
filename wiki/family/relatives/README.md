---
title: "Relatives"
type: meta
subjects: [family]
status: active
---

# Relatives

Extended family — grandparents, aunts, uncles, cousins. One page per person. Think of these as mini-biographies from your family's perspective, with a focus on their relationship to your kid(s).

## How to file

- One page per person: `slug.md` (e.g. `grandma-m.md`, `uncle-t.md`).
- `subjects:` usually `[family]` plus whichever kids have meaningful relationships with them.
- When a relative passes, the page stays active — add a section documenting it, and cross-link to any `family/lore/` or `children/<slug>/losses/` pages.

## First-class subjects (optional)

If a relative has a slug declared in `AGENTS.family.md` (a `slug:` field on their `household.*` entry), the canonical page at `<slug>.md` should include that slug in `subjects:`. Example: `subjects: [grandma-m, family]`. That makes queries like "show me everything about Grandma M" reach across the wiki — her profile here, her page in `family/lore/`, per-child reflections, and any mention in trips or shared memories. Relatives without a declared slug remain unstructured context — file as `subjects: [family]` and describe the relationship in prose. See the "Non-child subjects (optional)" section of [`AGENTS.md`](../../../AGENTS.md).

## Related examples

A `grandma-m.md` page here would pair with [the lore example](../_examples/lore/2024-grandma-m-death.md).

## Pages

See [`index.md`](index.md) for what's filed in this directory.
