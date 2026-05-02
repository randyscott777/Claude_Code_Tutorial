# Claude Code Plugins

Plugins are a bundle of extension (skills, MCP, commands, and hooks).
Plugins extend Claude Code with new tools, data sources, and capabilities. The primary plugin system is **MCP (Model Context Protocol)** — an open standard that lets any external service expose tools to Claude.

---

## How Plugins Work

When Claude Code starts, it connects to any configured MCP servers. Each server registers a set of **tools** that Claude can call during a conversation — just like the built-in tools (Read, Edit, Bash, etc.). From Claude's perspective, an MCP tool and a built-in tool are identical.

```
Your prompt
    │
    ▼
Claude decides which tool to call
    │
    ├─ Built-in tool  →  Claude Code handles it locally
    │
    └─ MCP tool  →  Sent to the MCP server process  →  Result returned
```

The server runs as a **subprocess** (or remote HTTP service) that speaks the MCP protocol. Claude Code launches it, keeps it alive for the session, and communicates over stdio or SSE.

---

## Plugin Types

| Type | What it is | Example |
|------|-----------|---------|
| **MCP server** | External process that adds tools/resources | GitHub, Postgres, Slack |
| **Skill** | Local markdown prompt that teaches Claude a workflow | `/explain-code`, `/create-a-list` |
| **Hook** | Shell command that fires on Claude Code events | Auto-lint, toast notifications |

Skills and hooks are covered in their own sections. This page focuses on MCP plugins.

---

## Finding Plugins

### Official MCP Registry

Anthropic maintains a curated list of MCP servers:

```
https://github.com/modelcontextprotocol/servers
```

Popular servers include:

| Plugin | What it adds |
|--------|-------------|
| `@modelcontextprotocol/server-github` | GitHub issues, PRs, code search |
| `@modelcontextprotocol/server-postgres` | Query PostgreSQL databases |
| `@modelcontextprotocol/server-filesystem` | Controlled file system access |
| `@modelcontextprotocol/server-brave-search` | Real-time web search |
| `@modelcontextprotocol/server-slack` | Post messages, read channels |
| `@modelcontextprotocol/server-google-maps` | Location search and directions |
| `@modelcontextprotocol/server-sqlite` | Read/write SQLite databases |

### Community Plugins

Search npm for `@modelcontextprotocol` or browse:

- `https://github.com/punkpeye/awesome-mcp-servers` — community-curated list
- `https://glama.ai/mcp/servers` — searchable MCP directory

---

## Installing a Plugin

### Step 1 — Add via CLI

```bash
claude mcp add github npx -y @modelcontextprotocol/server-github
```

This writes the server config to `.claude/settings.json` automatically.

### Step 2 — Or configure manually

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

### Step 3 — Verify it loaded

```
claude mcp list
```

Tools registered by each server appear in Claude's tool list when the session starts.

---

## Scope: Global vs. Project

| Scope | Config file | When to use |
|-------|-------------|-------------|
| **Global** | `~/.claude/settings.json` | Plugins you want in every project (GitHub, search) |
| **Project** | `.claude/settings.json` | Plugins specific to this repo (project database, internal APIs) |
| **Local** | `.claude/settings.local.json` | Personal overrides not committed to git |

---

## How Claude Uses Plugin Tools

Once an MCP server is connected, Claude automatically knows about its tools through the session context. You don't need to prefix your request — just ask naturally:

```
> What open issues are assigned to me on the repo?
```

Claude sees the `list_issues` tool from the GitHub MCP server and calls it. Results come back as structured data that Claude can reason about and summarize.

---

## Writing Your Own Plugin

An MCP server can be written in any language. The TypeScript SDK is the simplest starting point:

```bash
npm install @modelcontextprotocol/sdk
```

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "my-plugin", version: "1.0.0" });

server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "greet",
    description: "Greet a person by name",
    inputSchema: {
      type: "object",
      properties: { name: { type: "string" } },
      required: ["name"]
    }
  }]
}));

server.setRequestHandler("tools/call", async (req) => {
  const { name } = req.params.arguments as { name: string };
  return { content: [{ type: "text", text: `Hello, ${name}!` }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

Register it in `settings.json`:

```json
{
  "mcpServers": {
    "my-plugin": {
      "command": "node",
      "args": ["path/to/my-plugin/index.js"]
    }
  }
}
```

### Python MCP Servers

The `fastmcp` library makes Python servers easy:

```bash
pip install fastmcp
```

```python
from fastmcp import FastMCP

mcp = FastMCP("my-plugin")

@mcp.tool()
def greet(name: str) -> str:
    """Greet a person by name"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

---

## Plugin Security

MCP servers run with the permissions of your local user. Before installing a plugin:

- **Review the source** — check the npm package or GitHub repo
- **Scope the env vars** — give the minimum permissions needed (read-only tokens where possible)
- **Use project scope** for sensitive plugins so they only run in the right repo
- **Never commit secrets** — put tokens in `settings.local.json` (gitignored) or environment variables

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Server not showing in tool list | Run `claude mcp list` to check it registered; check for npm install errors |
| Tools not being called | Try `/mcp` in the session to see server status |
| Auth errors | Verify env vars are set; check token scopes |
| Server crashes on start | Run the server command manually to see its error output |

```bash
# Test a server manually before adding it to Claude
npx -y @modelcontextprotocol/server-github
```

---

## This Repo's Active Plugins

This tutorial project uses these MCP servers (see `.claude/settings.local.json`):

- **gdrive-local** — Google Drive, Gmail, Google Calendar
- **github** — GitHub integration
- **fastMCP-server** — demo server (add/multiply tools)
- **sequential-thinking** — structured reasoning tool

# Speech-to-text plugins
### from Marketplace
- ?
