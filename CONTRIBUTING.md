# Contributing

Pull requests to improve the scaffold (AGENTS.md, directory structure, lint skill) are welcome.

## What not to contribute

- Never push a fork that contains your family's actual content. The template ships empty.
- `AGENTS.local.md` and `AGENTS.overlay.md` are gitignored so they won't accidentally travel with a fork. `AGENTS.family.md` is **not** gitignored (it belongs in the user's private repo alongside their `wiki/` content) but must never appear in an upstream PR — only its `.example` counterpart travels upstream.
- Real content under `wiki/children/<slug>/` and `raw/` — including your family data in `AGENTS.family.md` — stays in your private instance only.

## Developing the scaffold itself

The scaffold ships with a `PreToolUse` hook (`.claude/hooks/pre-git-guard.sh`) that blocks `git commit` / `git push` unless `AGENTS.local.md` grants explicit permission. That file is gitignored and absent in a fresh checkout — which is correct for real family-KB instances (forces the Bootstrap flow) but prevents agent-driven commits during scaffold development.

**Escape hatch for contributors:** set `AGENT_GIT_APPROVED=1` in the shell *before* launching Claude Code (or your agent of choice):

```bash
export AGENT_GIT_APPROVED=1
claude   # or codex, cursor, etc.
```

The hook reads this variable from its own environment (the shell that launched the agent), so agents cannot set it inline via `AGENT_GIT_APPROVED=1 git commit` — that would only set the variable for the subshell running the git command, not for the hook process that fires beforehand.

**Do not set this variable in a real family-KB instance.** The hook exists to catch the failure mode where an agent assumes commit consent it wasn't given; bypassing it defeats the defense.

## DCO and Relicensing

By contributing to this project, you:

1. Represent that you have the right to contribute the code
2. Grant the project owner an irrevocable, perpetual, royalty-free license to use your contribution in this project, in any current or future license
3. Agree that you retain no copyright or other ownership claim to your contribution

This ensures the project can be relicensed to a more permissive license in the future if desired, without requiring individual contributor consent for each relicensing.