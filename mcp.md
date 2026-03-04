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
claude mcp list              # List all configured servers
(shows Google Calendar and Gmail - both needing authentication)

claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem   
(this updates the /users/randy/.claude,json file)

claude mcp remove filesystem     # Remove the specified server

claude mcp status            # unknow ????? Check server health and connectivity
```
