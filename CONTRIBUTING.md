# Contributing

Pull requests to improve the scaffold (AGENTS.md, directory structure, lint skill) are welcome.

## What not to contribute

- Never push a fork that contains your family's actual content. The template ships empty.
- `AGENTS.local.md` and `AGENTS.overlay.md` are gitignored so they won't accidentally travel with a fork. `AGENTS.family.md` is **not** gitignored (it belongs in the user's private repo alongside their `wiki/` content) but must never appear in an upstream PR — only its `.example` counterpart travels upstream.
- Real content under `wiki/children/<slug>/` and `raw/` — including your family data in `AGENTS.family.md` — stays in your private instance only.

## DCO and Relicensing

By contributing to this project, you:

1. Represent that you have the right to contribute the code
2. Grant the project owner an irrevocable, perpetual, royalty-free license to use your contribution in this project, in any current or future license
3. Agree that you retain no copyright or other ownership claim to your contribution

This ensures the project can be relicensed to a more permissive license in the future if desired, without requiring individual contributor consent for each relicensing.