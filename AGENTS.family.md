# AGENTS.family.md

**Family-specific data** for this knowledge base. The agent reads this file at the start of every session to learn which children exist, who's in the household, tone defaults, sensitive-topic flags, and the spellchecker's family-vocabulary whitelist.

_(Not yet filled in — run the Bootstrap flow from `AGENTS.md`. The expected shape is below; replace this placeholder with the real values.)_

## Reading order

This is layer 3 of the 4-layer AGENTS stack:

1. `AGENTS.md` (core schema)
2. `AGENTS.overlay.md` (optional; if present, read before this file)
3. **`AGENTS.family.md`** ← you are here
4. `AGENTS.local.md` (per-user preferences — next in the chain)

---

## Family details (YAML)

```yaml
children:
  - slug: ava                         # kebab-case; used as directory name — DO NOT rename after content exists
    legal_name: "Ava Full-Name"
    preferred_name: "Ava"
    nicknames: ["Avocado", "Bug"]
    pronouns: "she/her"
    birthdate: YYYY-MM-DD
    notes: ""                         # anything you want the agent to know up front

household:
  parents:
    - name: ""
      relationship: ""                # "mom", "dad", "step-parent", etc.
  other_members:
    - name: ""
      relationship: ""                # "grandparent", "sibling", "au pair", etc.
  close_circle:
    - name: ""
      relationship: ""                # "grandma (mom's side)", "babysitter 2022-2024", etc.

homes:                                # places the family has lived, most recent first
  - location: "City, State/Country"
    dates: "YYYY — present"           # or "YYYY — YYYY"
    notes: ""

tone:                                 # default voice for agent-written prose
  register: ""                        # "warm", "clinical", "terse", "playful", "literary"
  pov: ""                             # "parent", "neutral third-person", "journal-style"
  avoid_words: []
  preferred_quirks: ""                # anything distinctive to preserve

sensitive_topics:                     # handle with extra care
  - topic: ""                         # e.g. "grandparent's death, 2025"
    handling: ""                      # "ask before filing", "measured tone only", etc.

family_vocabulary:                    # spellchecker allowlist: names, nicknames, invented words
  - ""
```

---

## Notes section (freeform)

_None yet._
