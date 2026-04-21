---
title: "Caregivers"
type: meta
subjects: [family]
status: active
---

# Caregivers

Teachers, nannies, au pairs, babysitters, coaches, instructors, daycare providers — any adult who spent meaningful time with your kid(s). These are the people they often won't remember the names of later, which is exactly why to capture them.

## How to file

- One page per caregiver (or per caregiver-role-era if the same person had multiple stints).
- Filename: `descriptive-slug.md` (e.g. `kindergarten-teacher-2024.md`, `nanny-2019-to-2021.md`).
- `subjects:` lists every kid they cared for.

## First-class subjects (optional)

If a caregiver has a slug declared in `AGENTS.family.md` (a `slug:` field on their `household.close_circle` or `other_members` entry), the canonical page at `<slug>.md` should include that slug in `subjects:` alongside the kids they cared for. Example: `subjects: [ms-patel-2024, ava]`. Caregivers without a declared slug stay as prose — most families won't want to track every babysitter as a first-class subject, which is fine. See the "Non-child subjects (optional)" section of [`AGENTS.md`](../../../AGENTS.md).

## Reference examples

- [Kindergarten teacher, 2024](../_examples/caregivers/kindergarten-teacher-2024.md) — _fictional; see [`_examples/`](../_examples/README.md)_

## Pages

See [`index.md`](index.md) for what's filed in this directory.
