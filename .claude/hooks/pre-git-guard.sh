#!/usr/bin/env bash
# PreToolUse hook for When You Were — git commit / git push guard.
#
# Enforces the fail-closed permission rule from AGENTS.md "Committing & pushing":
#
#   - `git commit` is blocked unless AGENTS.local.md exists AND contains both
#     `auto_commit: true` and `privacy_acknowledged: true`.
#   - `git push` is blocked unless the commit conditions are met AND
#     `auto_push: true` is also set.
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
# Check AGENTS.local.md flags.
# -----------------------------------------------------------------------------
LOCAL="AGENTS.local.md"

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
    echo "If the user just asked you to make this commit, stage the changes and ask them"
    echo "to run 'git commit' themselves. Do NOT re-run with a workaround — the block"
    echo "exists to catch the exact failure mode where an agent assumes consent it"
    echo "wasn't given."
    echo ""
    echo "(Scaffold contributor? Set AGENT_GIT_APPROVED=1 in your shell before launching"
    echo "Claude Code. Do not set this in a real family-KB instance.)"
  } >&2
  exit 2
fi

# Grep for flag values. Accept `key: true` with flexible whitespace.
grep_flag() {
  local key="$1"
  grep -Eq "^[[:space:]]*${key}:[[:space:]]*true([[:space:]]|#|$)" "$LOCAL"
}

priv_ok=0; grep_flag "privacy_acknowledged" && priv_ok=1
commit_ok=0; grep_flag "auto_commit"          && commit_ok=1
push_ok=0;   grep_flag "auto_push"            && push_ok=1

# Commit gate.
if (( is_commit == 1 )); then
  if (( commit_ok != 1 || priv_ok != 1 )); then
    {
      echo "BLOCKED: git commit attempted, but AGENTS.local.md does not grant autonomous commit."
      echo ""
      echo "Current state:"
      echo "  auto_commit:          $(grep -E '^[[:space:]]*auto_commit:' "$LOCAL" | head -1 || echo '(unset)')"
      echo "  privacy_acknowledged: $(grep -E '^[[:space:]]*privacy_acknowledged:' "$LOCAL" | head -1 || echo '(unset)')"
      echo ""
      echo "Both auto_commit and privacy_acknowledged must be explicitly 'true' before you"
      echo "may run git commit on your own. See AGENTS.md \"Committing & pushing\"."
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
      echo "BLOCKED: git push attempted, but AGENTS.local.md does not grant autonomous push."
      echo ""
      echo "Current state:"
      echo "  auto_push:            $(grep -E '^[[:space:]]*auto_push:' "$LOCAL" | head -1 || echo '(unset)')"
      echo "  privacy_acknowledged: $(grep -E '^[[:space:]]*privacy_acknowledged:' "$LOCAL" | head -1 || echo '(unset)')"
      echo ""
      echo "Both auto_push and privacy_acknowledged must be explicitly 'true' before you"
      echo "may run git push on your own. See AGENTS.md \"Committing & pushing\"."
      echo ""
      echo "Never push to a public remote regardless of flag state."
    } >&2
    exit 2
  fi
fi

exit 0
