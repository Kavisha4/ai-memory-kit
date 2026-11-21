# Agent Memory Kit

Companion repo for the talk **"The Memory Problem: Why Your AI Agent Forgets"** by Kavisha Mathur ([ChaoTech](https://chaotech.in)), DevFest Bengaluru 2026.

## Start here: the Memory Capsule (2 minutes, no code)

Every new chat with an AI starts as a stranger. The Memory Capsule is one block of text that holds what the AI should know about you. You own it, and it works in Claude, ChatGPT and Gemini.

**ChatGPT, Gemini, or Claude without skills**
1. Copy [`demo3-chat-users/memory-capsule-prompt.txt`](demo3-chat-users/memory-capsule-prompt.txt).
2. Paste it where it loads every time. ChatGPT: Settings → Personalization → Custom instructions, or a Project's instructions. Claude: a Project's instructions. Gemini: Saved info.
3. Talk normally. Say "remember …" for anything that should stick, "forget …" to remove it.
4. At the end, say **"save memory"**. Paste the capsule it prints into your next chat.

**Claude, as a skill (loads by itself)**
1. Download [`demo3-chat-users/memory-notebook.zip`](demo3-chat-users/memory-notebook.zip).
2. Claude → Settings → Capabilities → Skills → Upload skill (code execution must be on).
3. Claude Code: copy [`demo3-chat-users/memory-notebook/`](demo3-chat-users/memory-notebook) into `~/.claude/skills/`.

**Before:** "Book a team dinner near me" → "Which city are you in, how many people, any dietary needs?"
**After:** "Here are three pure-vegetarian places in Pune for tonight. I skipped anywhere that cooks with peanuts."

## Go deeper: the three demos from the talk

| You are… | Go to | What you get |
|----------|-------|--------------|
| Using Claude or ChatGPT | [`demo3-chat-users/`](demo3-chat-users) | The memory-notebook skill and the capsule prompt above. |
| Using Copilot, Claude Code, Cursor or Tabnine at work | [`demo2-coding-assistants/`](demo2-coding-assistants) | A sample repo with AGENTS.md, CLAUDE.md, Copilot instructions and path-scoped rules, and how each tool remembers. |
| Building AI agents | [`demo1-agent-builders/`](demo1-agent-builders) | `python3 stale_polaroid.py`: semantic vs time-based vs hybrid vs write-back retrieval, offline, zero installs. |

Each demo also has a click-through visual in its `visual/index.html` (open it in a browser).
How each one works under the hood (where memory lives, latency, caching, what breaks, how big it gets) is in [`ARCHITECTURE.md`](ARCHITECTURE.md).

## The 4 types, in one line each
- **Working**: what is in the context window for this call.
- **Episodic**: what happened, with a timestamp.
- **Semantic**: what is true now, versioned when it changes.
- **Procedural**: how to act (rules, skills, instructions files).

## License
MIT
