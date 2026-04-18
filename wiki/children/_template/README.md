---
title: "Child template"
type: meta
subjects: [_template]
status: example
---

# `_template/` — reference structure for a child

This directory is **not real content**. It's a reference showing the shape of a per-child subdirectory, with one example page per category so you know what frontmatter and links look like in practice.

## How to use it

- **Read through it** once to understand the structure.
- **Don't edit these pages** — they're documentation.
- When you want to add a new child, ask the agent: *"Set up a new child directory for \<name\>."* The agent will copy this structure and replace placeholders.
- The lint skill is configured to skip `_template/` — its `subjects: [_template]` placeholder entries will not be flagged.

## The fictional "template" child

To make the examples concrete, pages here use a fictional child:

- **Name:** Sam (short for Samira or Samuel — ambiguous on purpose)
- **Slug:** `_template`
- **Pronouns:** they/them
- **Birthdate:** 2019-06-15 (so the examples have a plausible age arc)

Examples reference a fictional sibling "Robin" and a fictional family pet "Biscuit" where shared-content examples are useful.

## What's in here

- [`profile.md`](profile.md) — top-level page per child
- One example page in each of the 24 category directories:
  - **Emotional-texture:** [quotes](quotes/), [questions](questions/), [fears](fears/), [character-moments](character-moments/), [letters](letters/), [reflections](reflections/), [aspirations](aspirations/), [heroes](heroes/)
  - **Practical-but-usually-lost:** [physical](physical/), [routines](routines/), [friends](friends/), [pets](pets/), [gifts](gifts/), [caregivers (family-level)](../../family/caregivers/)
  - **Standard:** [firsts](firsts/), [milestones](milestones/), [memories](memories/), [preferences](preferences/), [health](health/), [education](education/), [interests](interests/), [travel](travel/), [achievements](achievements/), [creative-works](creative-works/), [losses](losses/)
