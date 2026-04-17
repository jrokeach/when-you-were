#!/usr/bin/env bash
# SessionStart hook for kids-kb.
#
# Emits gentle reminders to the agent when:
#   - AGENTS.local.md does not yet exist  (run bootstrap)
#   - .agents-local-last-prompt is missing or older than 14 days (capture nudge)
#   - .agents-last-lint is missing or older than 30 days (lint nudge)
#
# Output to stdout is injected into the agent's session context.
# Silent exit with no output means "nothing to remind about".

set -u

# Portable "is file older than N days?" check.
# Returns 0 (true) if file missing OR mtime older than $1 days.
is_stale() {
  local path="$1"
  local days="$2"
  if [[ ! -f "$path" ]]; then
    return 0
  fi
  # macOS and GNU find both support -mtime.
  if find "$path" -mtime +"$days" -print 2>/dev/null | grep -q .; then
    return 0
  fi
  return 1
}

REMINDERS=()

if [[ ! -f "AGENTS.local.md" ]]; then
  REMINDERS+=("AGENTS.local.md does not exist — run the Bootstrap flow from AGENTS.md before anything else (privacy acknowledgment, family interview, orient the user).")
else
  if is_stale ".agents-local-last-prompt" 14; then
    REMINDERS+=("Capture nudge due: it has been >14 days (or never) since the last capture prompt. After greeting the user, gently ask whether there is anything new to capture — firsts, milestones, quotes, photos, things the kid(s) have been asking about. Update .agents-local-last-prompt afterward regardless of outcome.")
  fi

  if is_stale ".agents-last-lint" 30; then
    REMINDERS+=("Lint nudge due: it has been >30 days (or never) since the last lint. Offer to run the /lint skill before ingesting new content. Update .agents-last-lint afterward regardless of outcome.")
  fi
fi

if (( ${#REMINDERS[@]} == 0 )); then
  exit 0
fi

echo "[kids-kb session reminders]"
for r in "${REMINDERS[@]}"; do
  echo "- $r"
done
