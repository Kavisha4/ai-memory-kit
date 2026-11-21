#!/usr/bin/env bash
# Creates the two hidden config files for the demo (.claude/rules and .github).
set -e
cd "$(dirname "$0")"
mkdir -p .claude/rules .github
cat > .claude/rules/api.md <<'RULE'
---
paths:
  - "api/**/*.py"
---
# API rules (load only when Claude touches api/)
- Return 409 on a repeated Idempotency-Key with a different body.
- Log the order_id on every error.
RULE
cat > .github/copilot-instructions.md <<'RULE'
Follow AGENTS.md at the repository root. Money is integer paise. Write endpoints need an Idempotency-Key header.
RULE
echo "Created .claude/rules/api.md and .github/copilot-instructions.md"
