# Demo 2: for people using Copilot, Claude Code, Cursor, Tabnine at work

First run `bash sample-repo/setup.sh` once (it creates the hidden `.claude/rules/api.md` and `.github/copilot-instructions.md`). Then open `sample-repo/` in Claude Code and run:
1. `/memory`: shows every file loaded into context (user CLAUDE.md, project CLAUDE.md, imported AGENTS.md) and the auto-memory folder.
2. Ask: "add a refunds endpoint". It uses integer paise and an Idempotency-Key without being told, and `.claude/rules/api.md` loads only once it touches `api/`.
3. Correct it once ("refunds over ₹10,000 need manager approval"). Start a fresh session and ask again: auto memory brought it back.
4. Open the same folder in VS Code with Copilot: it reads `.github/copilot-instructions.md` and AGENTS.md.

## How each tool gets context (as documented, Nov 2026)
| Tool | Instructions you write | Memory it writes | How it finds code |
|------|------------------------|------------------|-------------------|
| Claude Code | `CLAUDE.md` (managed → `~/.claude` → project → `CLAUDE.local.md`, concatenated), `@imports`, `.claude/rules/` with `paths` globs | Auto memory: `~/.claude/projects/<repo>/memory/MEMORY.md`, first 200 lines / 25 KB loaded each session, topic files on demand | Agentic search: grep / glob / read on demand, no vector index |
| GitHub Copilot | `.github/copilot-instructions.md`, `*.instructions.md` with `applyTo`, `AGENTS.md` | Copilot Memory: repo-scoped facts with citations to code; re-validated before use; unused ones expire after 28 days | Remote semantic code index + agentic tools |
| Cursor | `.cursor/rules/*.mdc`, `AGENTS.md` | (rules are the persistent layer) | Merkle tree of file hashes → syntax-aware chunks → embeddings; re-indexes only changed branches; reuses teammates' index (~92% similar clones) |
| Tabnine | Admin-set guidelines | Context Engine: indexes connected remote repos, optional agentic pre-processing into summaries, services, dependencies | Exposed to the agent through MCP tools; local workspace first |

Takeaway: two retrieval philosophies. Index everything up front (Cursor, Copilot, Tabnine) or let the agent search like a developer would (Claude Code). Both still need a human-written instructions file, because the index tells the agent *where* the code is, not *why* it is that way.
