Model Context Protocol (MCP) extends Claude Code with custom tools and live data sources. MCP servers let Claude interact with external services — databases, APIs, version control platforms, and more.

## What is MCP?

MCP is an open protocol that standardizes how AI models connect to external tools and data. Think of MCP servers as **plugins** that give Claude new capabilities beyond its built-in toolset.

## Why Use MCP?

- Query databases directly during coding sessions
- Access GitHub issues, PRs, and repo data
- Send Slack messages or create Jira tickets
- Integrate with internal company tools and systems
- Add specialized tools like web search or security scanners

## Adding an MCP Server

```bash
# Add via CLI (easiest)
claude mcp add github npx -y @modelcontextprotocol/server-github

# Or configure manually in .claude/settings.json:
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```
## github mcp server usage                                                                               
● With the GitHub MCP server connected, you can interact with GitHub directly from Claude Code without   switching to a browser or running gh CLI commands manually. Here's what's available:               
  Repositories
  - Search repositories, read file contents, list branches/commits                                    
  - Create new repositories or fork existing ones

  Issues
  - List, search, create, update, and close issues
  - Add comments and labels

  Pull Requests
  - List, create, review, merge, and close PRs
  - Add comments, request reviewers, check CI status
  - Get PR diffs and file changes

  Code
  - Search code across GitHub
  - Browse repository file trees
  - Read any file from any public (or authorized private) repo

  Commits & Branches
  - Create branches, list commits, compare refs
  - Push file changes directly via the API

  Notifications & Releases
  - Read notifications, manage releases and tags

  Practical examples for this project:
  - "Create a GitHub issue for a bug I found"
  - "Open a PR for my current branch"
  - "Search for examples of CLAUDE.md files in other repos"
  - "List open PRs on my repo"
  - "Read the README of any GitHub repo"

  The key advantage over gh CLI is that Claude can chain multiple GitHub operations together
  intelligently in a single request, with full context awareness of what you're working on locally.   


> **Security Note:** MCP servers can have significant system access. Only install servers from trusted sources, and review the permissions they request before adding them to your configuration.

## Popular MCP Servers

| Server | Capability |
|--------|-----------|
| `@mcp/github` | Read/write GitHub issues, PRs, and repositories |
| `@mcp/postgres` | Direct SQL queries against your database |
| `@mcp/filesystem` | Extended file operations beyond the project |
| `@mcp/slack` | Send messages to Slack channels |
| `@mcp/brave-search` | Live web search during coding sessions |
| `@mcp/puppeteer` | Control a browser for UI testing |

## Managing Servers

```bash
claude mcp list                  # List all configured servers
claude mcp get <name>            # Get details for a specific server
claude mcp add <name> <command>  # Add a new server
claude mcp remove <name>         # Remove a server
claude mcp serve                 # Run Claude Code itself as an MCP server
```

> **Note:** There is no `claude mcp status` or `claude mcp auth` command.

## Authenticating Remote MCP Servers

Remote servers (like Google Calendar and Gmail) may show **"Needs authentication"** after `mcp list`. To authenticate, use the `/mcp` slash command **inside a Claude Code session**:

```
/mcp
```

This opens an interactive menu — select the server and follow the browser OAuth flow. Tokens are stored securely and refreshed automatically. Use "Clear authentication" in the `/mcp` menu to revoke access.

# Google Calendar and Gmail MCP servers
The Google Calendar and Gmail MCP servers you're seeing (tools prefixed with
  mcp__claude_ai_Google_Calendar__ and mcp__claude_ai_Gmail__) are remote MCP servers hosted by 
  Anthropic, not locally-configured ones. 
                                                                                                      
  They're enabled through your claude.ai account settings, not through local JSON files. The flow is:

  1. Go to claude.ai → Settings → Integrations (or similar)
  2. Enable Google Calendar and Gmail integrations
  3. Claude Code inherits these remote MCP servers automatically when you're authenticated

  Authentication

  Since they use OAuth (not API keys), you authenticate inside a Claude Code session:

  /mcp

  This opens an interactive menu → select the server → browser OAuth flow → tokens stored securely.   

  How They Differ from Local MCP Servers

  ┌─────────────────────────────────────┬──────────────────────────────────┐
  │       Local MCP (like GitHub)       │ Remote MCP (like Gmail/Calendar) │
  ├─────────────────────────────────────┼──────────────────────────────────┤
  │ Configured in .claude/settings.json │ Configured via claude.ai account │
  ├─────────────────────────────────────┼──────────────────────────────────┤
  │ Uses command + args + env           │ Hosted by Anthropic, OAuth-based │
  ├─────────────────────────────────────┼──────────────────────────────────┤
  │ GITHUB_TOKEN in env vars            │ No secrets in local files        │
  ├─────────────────────────────────────┼──────────────────────────────────┤
  │ claude mcp add ...                  │ Enabled through web UI           │
  └─────────────────────────────────────┴──────────────────────────────────┘

  Why claude mcp list Shows Nothing

  The mcp list command only shows locally-configured servers. Remote servers (like these Google ones) 
  don't appear there — they're injected at the session level based on your account.

  The tool name prefix mcp__claude_ai_* is the giveaway — claude_ai means these are Anthropic-hosted
  remote MCP servers, not local processes.

## Building MCP Servers with FastMCP

[FastMCP](https://github.com/jlowin/fastmcp) is a Python framework that makes it easy to build your own MCP servers with minimal boilerplate.

### Install

```bash
pip install fastmcp
```

### Create a Server

```python
from fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.resource("config://settings")
def get_settings() -> str:
    """Return app settings."""
    return "debug=true"

if __name__ == "__main__":
    mcp.run()
```

### Add to Claude Code

```bash
claude mcp add my-tools python path/to/server.py
```

Or in `.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

### Key FastMCP Concepts

| Decorator | Purpose |
|-----------|---------|
| `@mcp.tool()` | Expose a callable function as a tool Claude can invoke |
| `@mcp.resource()` | Expose data at a URI Claude can read |
| `@mcp.prompt()` | Define reusable prompt templates |

FastMCP handles the MCP protocol, schema generation from type hints, and server lifecycle — you just write Python functions.
