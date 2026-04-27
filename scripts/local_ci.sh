#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python3 scripts/validate_scaffold.py
bash -n .claude/hooks/*.sh
