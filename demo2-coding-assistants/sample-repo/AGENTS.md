# Order Service: agent instructions
<!-- Read by Copilot, Codex, Cursor and others. Claude Code reads it via @AGENTS.md in CLAUDE.md. -->

## Commands
- Test: `pytest -q`
- Lint: `ruff check .`

## Conventions
- Money is integer paise, never float.
- Every write endpoint takes an `Idempotency-Key` header.
- New endpoints go in `api/routes/`, one file per resource.
