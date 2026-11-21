# Demo 1: for engineers building agents

`python3 stale_polaroid.py` (no installs, no API key, works offline on stage)

Shows the four read strategies on the same 7-message history, and why a versioned
facts table beats "add a vector DB". Same finding as the benchmark in the talk:
semantic search finds the new fact but ranks the stale one above it.

## Go further with real repos (scan and star)
| Repo | What it shows | Try |
|------|---------------|-----|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | Memory layer: LLM extracts facts, then ADD / UPDATE / DELETE / NOOP against existing ones | `pip install mem0ai`, quickstart in README |
| [getzep/graphiti](https://github.com/getzep/graphiti) | Temporal knowledge graph: every edge has valid_at / invalid_at | quickstart example |
| [letta-ai/letta](https://github.com/letta-ai/letta) | MemGPT lineage: core memory blocks in context + archival memory the agent pages in; sleep-time agents | `letta` server + ADE |
| [langchain-ai/langmem](https://github.com/langchain-ai/langmem) | Semantic / episodic / procedural memory tools for LangGraph | hot-path vs background extraction |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | Claude API memory tool: the model reads and writes its own `/memories` files | search the repo for "memory" |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | `memory` server: knowledge-graph memory any MCP client can use | add to Claude Desktop config |
