---
title: "Audit log"
type: meta
subjects: [family]
status: active
---

# Audit log

Findings from lint runs. The lint skill (`/lint`) appends here. See `.claude/skills/lint/SKILL.md` for checks performed and severity scale.

## Format

```
## Audit — YYYY-MM-DD

- Critical (N): brief list with file paths
- High (N): ...
- Medium (N): ...
- Low (N): ...

### Findings
[detailed list grouped by severity]
```

## Severity scale

- **Critical** — factually wrong, frontmatter that breaks parsing, data loss risk
- **High** — broken links, missing required fields, misfiled pages
- **Medium** — stale drafts, orphans, inconsistent references, filename violations
- **Low** — typos, style nits, minor convention deviations

## Entries

<!-- audit-entries-begin -->

_No audits yet. Run `/lint` (or wait for the 30-day nudge) to populate._

<!-- audit-entries-end -->
