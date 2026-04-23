#!/usr/bin/env bash
# PreToolUse hook for When You Were — git commit / git push guard.
#
# Enforces the fail-closed permission rule from AGENTS.md "Committing & pushing":
#
#   - `git commit` is blocked unless `auto_commit: true` AND
#     `privacy_acknowledged: true` are in effect.
#   - `git push` is blocked unless the commit conditions are met AND
#     `auto_push: true` is also in effect.
#
# Layer precedence (core ← overlay ← family ← local):
#   - `auto_commit` / `auto_push` — if AGENTS.local.md sets the key (to true
#     OR false), local wins. If local is silent on the key, AGENTS.overlay.md
#     is consulted as a fallback. If neither sets it, the fail-closed default
#     (false) applies.
#   - `privacy_acknowledged` — AGENTS.local.md only. The overlay cannot grant
#     per-user consent on behalf of the user. If AGENTS.local.md is absent,
#     commit/push are blocked regardless of overlay state.
#
# The hook runs before every Bash tool call. If the command contains
# `git commit` or `git push` and the conditions aren't met, it exits with
# status 2 and writes a message to stderr — Claude Code blocks the tool
# call and surfaces the message to the agent.
#
# Escape hatch for scaffold contributors:
#   Set AGENT_GIT_APPROVED=1 in the shell BEFORE launching Claude Code.
#   This bypass exists for developing the scaffold itself, where
#   AGENTS.local.md is intentionally absent. Do not set this in a
#   real family-KB instance.
#
# Why this hook exists: agents have been observed assuming auto_commit
# without checking AGENTS.local.md. The prose rule in AGENTS.md tells
# agents to re-check; this hook makes the re-check mechanical.

set -u

# -----------------------------------------------------------------------------
# Shell-level escape hatch for scaffold contributors.
# -----------------------------------------------------------------------------
# Inherited from the environment the user launched Claude Code from. The
# agent cannot set this inline (inline env prefixes apply to the tool
# command's subshell, not to the hook's process).
if [[ "${AGENT_GIT_APPROVED:-}" == "1" ]]; then
  exit 0
fi

# -----------------------------------------------------------------------------
# Parse Claude Code hook payload (JSON on stdin).
# -----------------------------------------------------------------------------
INPUT_JSON="$(cat)"

TOOL_NAME=""
COMMAND=""
if command -v jq >/dev/null 2>&1; then
  TOOL_NAME="$(printf '%s' "$INPUT_JSON" | jq -r '.tool_name // empty' 2>/dev/null || true)"
  COMMAND="$(printf '%s' "$INPUT_JSON"  | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
else
  # Best-effort fallback if jq isn't installed. The payload shape is stable;
  # the agent is told to install jq in the contributor docs.
  TOOL_NAME="$(printf '%s' "$INPUT_JSON" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*:[[:space:]]*"//; s/"$//')"
  COMMAND="$(printf '%s' "$INPUT_JSON"  | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"'   | head -1 | sed 's/.*:[[:space:]]*"//; s/"$//')"
fi

# Only guard Bash tool calls.
if [[ "$TOOL_NAME" != "Bash" ]]; then
  exit 0
fi

# -----------------------------------------------------------------------------
# Detect git commit / git push in the command string.
# -----------------------------------------------------------------------------
# Broad substring match. False positives on literal strings like
# `echo "git commit"` are accepted — blocking those is harmless.
is_commit=0
is_push=0
case "$COMMAND" in
  *"git commit"*) is_commit=1 ;;
esac
case "$COMMAND" in
  *"git push"*) is_push=1 ;;
esac

if (( is_commit == 0 && is_push == 0 )); then
  exit 0
fi

# -----------------------------------------------------------------------------
# Check flag values from AGENTS.local.md (primary) and AGENTS.overlay.md
# (fallback for auto_commit / auto_push only).
# -----------------------------------------------------------------------------
LOCAL="AGENTS.local.md"
OVERLAY="AGENTS.overlay.md"

if [[ ! -f "$LOCAL" ]]; then
  {
    echo "BLOCKED: git $( (( is_commit == 1 )) && echo commit || echo push ) attempted, but AGENTS.local.md does not exist."
    echo ""
    echo "This repo has not completed the Bootstrap flow. Do not commit or push on the"
    echo "user's behalf until they have:"
    echo "  1. copied AGENTS.local.md.example to AGENTS.local.md,"
    echo "  2. acknowledged privacy (privacy_acknowledged: true),"
    echo "  3. explicitly set auto_commit: true (and auto_push: true if pushing)."
    echo ""
    echo "privacy_acknowledged is per-user consent and must live in AGENTS.local.md —"
    echo "an overlay cannot grant it on the user's behalf. If the user just asked you"
    echo "to make this commit, stage the changes and ask them to run 'git commit'"
    echo "themselves. Do NOT re-run with a workaround — the block exists to catch the"
    echo "exact failure mode where an agent assumes consent it wasn't given."
    echo ""
    echo "(Scaffold contributor? Set AGENT_GIT_APPROVED=1 in your shell before launching"
    echo "Claude Code. Do not set this in a real family-KB instance.)"
  } >&2
  exit 2
fi

# True if FILE contains a line of the form `<key>: true` (any indentation).
grep_true_in() {
  local file="$1"; local key="$2"
  [[ -f "$file" ]] || return 1
  grep -Eq "^[[:space:]]*${key}:[[:space:]]*true([[:space:]]|#|$)" "$file"
}

# True if FILE mentions `<key>:` at all (any value). Used to detect whether
# a layer is explicit on a key vs. silent — explicit local wins over overlay
# regardless of value.
grep_key_set_in() {
  local file="$1"; local key="$2"
  [[ -f "$file" ]] || return 1
  grep -Eq "^[[:space:]]*${key}:" "$file"
}

# Layered flag resolution for auto_commit / auto_push.
# Local wins if it's explicit. Otherwise overlay is consulted. Otherwise false.
resolve_flag() {
  local key="$1"
  if grep_key_set_in "$LOCAL" "$key"; then
    grep_true_in "$LOCAL" "$key" && return 0 || return 1
  fi
  grep_true_in "$OVERLAY" "$key" && return 0 || return 1
}

# privacy_acknowledged is local-only — no overlay fallback.
priv_ok=0;   grep_true_in "$LOCAL" "privacy_acknowledged" && priv_ok=1
commit_ok=0; resolve_flag "auto_commit" && commit_ok=1
push_ok=0;   resolve_flag "auto_push"   && push_ok=1

# Dump an effective-state line for a key, showing which file (if any) set it.
# Usage: show_effective_state <key> <file1> [<file2> ...]
show_effective_state() {
  local key="$1"; shift
  local f
  for f in "$@"; do
    if [[ -f "$f" ]] && grep -Eq "^[[:space:]]*${key}:" "$f"; then
      local value
      # Trim leading whitespace + "<key>:" and trailing whitespace, leaving just the value.
      value="$(grep -E "^[[:space:]]*${key}:" "$f" | head -1 | sed -E "s/^[[:space:]]*${key}:[[:space:]]*//; s/[[:space:]]*$//")"
      [[ -z "$value" ]] && value="(empty)"
      echo "  ${key}: ${value} (from ${f})"
      return 0
    fi
  done
  echo "  ${key}: (unset in AGENTS.local.md${2:+ and AGENTS.overlay.md})"
}

# Commit gate.
if (( is_commit == 1 )); then
  if (( commit_ok != 1 || priv_ok != 1 )); then
    {
      echo "BLOCKED: git commit attempted, but the layered config does not grant autonomous commit."
      echo ""
      echo "Effective state:"
      show_effective_state "auto_commit" "$LOCAL" "$OVERLAY"
      show_effective_state "privacy_acknowledged" "$LOCAL"
      echo ""
      echo "auto_commit must resolve to 'true' (from AGENTS.local.md, or from"
      echo "AGENTS.overlay.md if local is silent), AND privacy_acknowledged must be"
      echo "'true' in AGENTS.local.md. See AGENTS.md \"Committing & pushing\" and"
      echo "\"Interpreting the overlay\" for precedence details."
      echo ""
      echo "If the user asked for this specific commit: stage the changes, show them the"
      echo "diff, and have them run 'git commit' themselves. Do not ask them to flip the"
      echo "flag just to unblock a one-off commit."
    } >&2
    exit 2
  fi
fi

# Push gate.
if (( is_push == 1 )); then
  if (( push_ok != 1 || priv_ok != 1 )); then
    {
      echo "BLOCKED: git push attempted, but the layered config does not grant autonomous push."
      echo ""
      echo "Effective state:"
      show_effective_state "auto_push" "$LOCAL" "$OVERLAY"
      show_effective_state "privacy_acknowledged" "$LOCAL"
      echo ""
      echo "auto_push must resolve to 'true' (from AGENTS.local.md, or from"
      echo "AGENTS.overlay.md if local is silent), AND privacy_acknowledged must be"
      echo "'true' in AGENTS.local.md. See AGENTS.md \"Committing & pushing\"."
      echo ""
      echo "Never push to a public remote regardless of flag state."
    } >&2
    exit 2
  fi
fi

exit 0
