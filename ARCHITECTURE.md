# Under the hood: where memory lives in each demo

Times are typical orders of magnitude, not guarantees. Measure your own.

## Demo 1 · An agent you build

```
Your app server  ──►  Memory store (cloud DB)  ──►  Model API (GPU data centre)
 read path            facts table + vectors          prompt in, answer out,
 write path (async)   + raw event log                 keeps nothing after the call
```

| | |
|---|---|
| **Where it lives** | Postgres facts table (`valid_from` / `valid_to`), a vector index (pgvector, Pinecone) for episodes, and a raw event log. The model stores nothing. |
| **Retrieval time** | Facts lookup by index: about 1 ms. In-process vector top-k: about 10 ms (my benchmark). A hosted vector DB adds a network hop. The LLM call (0.5 to 2 s to first token) is the slow hop. |
| **Cached?** | The stable prefix (system prompt + user profile) can hit the provider's prompt cache (Anthropic: 5 minutes by default, 1 hour option). Retrieved memories change every call, so put them after the stable part. |
| **What breaks** | A stale fact outranks the new one (Demo 1). The async extraction lags, so a read right after a write sees the old fact. Changing the embedding model means re-embedding everything. A query not scoped by `user_id` leaks memories across users. |
| **How big** | One memory is about 200 bytes of text but about 6 KB as a 1,536-dimension float32 embedding, roughly 30 times bigger. 1 million users × 1,000 memories ≈ 6 TB of vectors, before the index. |

## Demo 2 · Coding assistants

```
Your laptop  ──►  Every request (HTTPS)  ──►  Model API
 AGENTS.md, CLAUDE.md,     instructions + rules +       reads it all, writes code,
 .claude/rules/, MEMORY.md first 200 lines of MEMORY.md  forgets it
```

| | |
|---|---|
| **Where it lives** | In the repo: `AGENTS.md`, `CLAUDE.md`, `.claude/rules/`. On your laptop only: `~/.claude/projects/<repo>/memory/MEMORY.md` and session transcripts. Cursor keeps code embeddings in its cloud index. Copilot Memory keeps repo facts on GitHub's side. |
| **Retrieval time** | Reading the files at session start takes under a millisecond. The cost is that their text is re-sent with every request. |
| **Cached?** | Yes. The stable start of the prompt (system prompt + CLAUDE.md) hits the prompt cache, so re-sending it is cheaper and faster. Change the start of the prompt and the cache misses. |
| **What breaks** | MEMORY.md grows past 200 lines and the rest is not auto-loaded. Two instruction files disagree. Rules go stale after a refactor. A long session compacts and drops early instructions. Auto memory is per laptop, so teammates don't get it: commit the rules that matter to `AGENTS.md`. |
| **How big** | The files are a few KB, but a 4 KB CLAUDE.md is about 1,000 tokens on every single request. Local transcripts can reach hundreds of MB; Claude Code deletes them after 30 days by default (`cleanupPeriodDays`). |

## Demo 3 · Claude and ChatGPT

```
Your phone / browser  ──►  Your account (provider cloud)  ──►  Model (GPU data centre)
 the app, and your          every chat, saved memories,          saved memory + capsule +
 capsule in Notes           project files                        chat → answer
```

| | |
|---|---|
| **Where it lives** | Not on your phone. Every chat (until you delete it), your saved memories and your project files live in your account, in the provider's cloud. The capsule lives wherever you keep it. |
| **Retrieval time** | Saved memory is added to the start of every chat. "Reference chat history" searches past chats before answering, which adds a retrieval step. The capsule needs no retrieval: it is already text in your prompt. |
| **Cached?** | Saved memory and instructions sit at the start of every prompt, so they can be prefix-cached. Your chats are stored, not cached. |
| **What breaks** | Memory fills up or the summary drops details. A wrong memory is trusted every time. Temporary chats skip memory. Deleting a chat does not always delete what was learned from it. Switch apps and you start from zero. |
| **How big** | One chat is about 10 to 50 KB of text. 2,000 chats is about 50 to 100 MB per account, plus every photo and PDF you uploaded. Across hundreds of millions of users, that is petabytes. Your capsule is under 3 KB. |
