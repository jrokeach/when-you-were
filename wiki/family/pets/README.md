---
title: "Pets"
type: meta
subjects: [family]
status: active
---

# Pets

Canonical pages for family pets. For per-kid relationships with a pet, use `children/<slug>/pets/<pet-slug>.md` — those pages link back here rather than duplicating the canonical info.

## How to file

- One page per pet: `<pet-slug>.md`.
- Include: species/breed, dates in the family, origin story, quirks, significant moments, (eventually) end of life.
- `subjects: [family]` plus any kid who had a meaningful relationship with them.

## First-class subjects (optional)

If the pet has a slug declared in `AGENTS.family.md` under `pets:`, the canonical page at `<pet-slug>.md` should list that slug in `subjects:` alongside `family` and any affected kids. Example: `subjects: [biscuit, family]`, or `subjects: [biscuit, ava, noah]` for a pet page that also highlights specific kids' relationships. That way, "show me everything about Biscuit" surfaces every page listing `biscuit` in its subjects, regardless of directory. Pets without a declared slug stay as unstructured context — file as `subjects: [family]` and describe them in prose. See the "Non-child subjects (optional)" section of [`AGENTS.md`](../../../AGENTS.md).

## Reference examples

- [Biscuit](../_examples/pets/biscuit.md) — _fictional; see [`_examples/`](../_examples/README.md)_

## Pages

See [`index.md`](index.md) for what's filed in this directory.
