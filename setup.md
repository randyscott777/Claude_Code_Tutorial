Getting Claude Code running takes just a few minutes. You need Node.js and either an Anthropic API key or a Claude.ai subscription (Pro or Max).

### Prerequisites

- **Node.js 18+** — verify with `node --version`
- **npm** — comes bundled with Node.js
- **Anthropic Account** — for API key or Claude.ai subscription

### Step 1: Install Claude Code

```
npm install -g @anthropic-ai/claude-code
```

This installs the `claude` command globally on your system.

### Step 2: Authenticate

Run `claude` for the first time and choose your authentication method:

```bash
# Option A: Claude.ai subscription (recommended — no API key needed)
claude
# → Opens your browser for OAuth login

# Option B: Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-api03-...
claude
```

### Step 3: Verify Everything Works

```bash
claude --version   # Check installed version
claude /doctor     # Run a full health check
```

### Configuration Files

Claude Code uses three settings locations:

- `~/.claude/settings.json` — global config for all projects
- `.claude/settings.json` — project-specific config (commit this)
- `.claude/settings.local.json` — local personal overrides (do not commit)

#### Global Config (`~/.claude/settings.json`)

Machine-wide defaults that apply to every project:

```json
{
  "theme": "dark",
  "autoUpdates": true,
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

#### Project Config (`.claude/settings.json`)

Project-specific rules committed alongside your code — great for team-shared guardrails:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test)",
      "Bash(npm run lint)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "npm run lint" }]
      }
    ]
  }
}
```

#### Local Config (`.claude/settings.local.json`)

Machine-specific personal overrides that **should not be committed** — ideal for developer-specific permissions or preferences that differ from the team's shared config:

```json
{
  "permissions": {
    "allow": [
      "Bash(start:*)",
      "Bash(node:*)"
    ]
  }
}
```

View the current file contents with:

```bash
cat .claude/settings.local.json
```

> **Tip:** Run `claude /doctor` anytime to diagnose issues. It checks authentication, API connectivity, Node.js version, and config files.

### Starting Your First Session

Navigate to any project directory and run `claude`. Claude will automatically read your project structure and be ready for instructions.
