# Overlay contract

This document is the public contract for host applications that layer product
or environment behavior on top of the When You Were scaffold.

The public scaffold must work without an overlay. A host application may add a
private, gitignored `AGENTS.overlay.md` at setup time to refine tone,
capabilities, local defaults, and host-specific instructions. The overlay is
layer 2 in the AGENTS chain:

1. `AGENTS.md` — public scaffold contract
2. `AGENTS.overlay.md` — optional private host layer
3. `AGENTS.family.md` — family data
4. `AGENTS.local.md` — per-user and per-machine preferences

## Public vs. private

The public repo may contain:

- generic schema and path contracts,
- examples of valid overlay fields,
- extension-point documentation,
- validation scripts that protect scaffold portability.

The public repo must not contain:

- product personality prompts,
- commercial strategy,
- provider credentials,
- platform storage bucket names,
- customer data,
- host-specific agent instructions that are not generally useful.

Use `AGENTS.overlay.md.example` to document field shape. Put real product
content in `AGENTS.overlay.md`, which is ignored by git.

## Required host behavior

A host application that installs an overlay should:

- copy or generate `AGENTS.overlay.md` from the public shape in
  `AGENTS.overlay.md.example`,
- set `overlay_name`, `overlay_version`, `notes`, and `downstream:
  "AGENTS.family.md"`,
- keep the overlay gitignored and refreshable by the host application,
- write family data only to `AGENTS.family.md`,
- write per-user consent and personal settings only to `AGENTS.local.md`,
- respect `UPSTREAM.manifest.yml` when syncing scaffold updates,
- keep product storage tooling outside the public scaffold unless it is generic
  and non-proprietary.

An overlay cannot bypass core safety gates: public-repo warnings,
privacy acknowledgment, fail-closed commit/push rules, and the upstream vs.
instance write boundary remain controlled by `AGENTS.md`.

## Extension paths

Agent-agnostic extensions belong under:

- `.agents/skills.overlay/`
- `.agents/hooks.overlay/`
- `.agents/settings.local.json`

Claude Code compatibility extensions may also use:

- `.claude/skills.overlay/`
- `.claude/hooks.overlay/`
- `.claude/settings.local.json`

All of these paths are instance-only and gitignored. They may be installed by a
host app, but `/sync-scaffold` must never overwrite them.

## Storage overlays

The public scaffold supports Git-only and hybrid storage through the raw
manifest convention in `STORAGE.md`. A host application may add object storage
uploaders, resolvers, signed URL generation, access control, lifecycle cleanup,
and export tooling. Those product implementations should consume the public
`schema/raw-manifest.schema.json` contract and preserve the `sources:`
frontmatter shape.

## Compatibility

Host applications should read `UPSTREAM.manifest.yml` before syncing or
customizing paths. The manifest exposes:

- upstream-tracked paths that may be replaced from the public template,
- template seed files that become instance state downstream,
- ignored private paths,
- overlay extension paths,
- sync exclusions.

If a host customizes an upstream-tracked path, it should list that path in
`AGENTS.overlay.md` under `instance_protected_paths` so sync tooling can skip it
and surface the drift to the user.

