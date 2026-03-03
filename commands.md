# Claude Code Commands

Slash commands are built-in shortcuts typed directly in Claude Code's interactive prompt. They start with `/` and control behavior, trigger git operations, and manage your session.

### Essential Session Commands

| Command | What it does |
|---------|--------------|
| `/help` | Show all available commands and usage examples |
| `/clear` | Clear conversation history (resets context) |
| `/compact` | Compress conversation to save context window space |
| `/status` | Show session info, token usage, and model details |
| `/doctor` | Run installation health check |
| `/memory` | View and manage persistent memory files |
| `/quit` | Exit Claude Code |

### Git Commands

| Command | What it does |
|---------|--------------|
| `/commit` | Analyze staged changes and generate a meaningful commit |
| `/diff` | Show and explain recent git changes |
| `/pr` | Create a pull request with an auto-generated description |
| `/review` | Review staged changes for bugs, security issues, style |

### Mode Commands

| Command | What it does |
|---------|--------------|
| `/plan` | Enter plan-only mode — Claude explains without making changes |
| `/fast` | Toggle fast mode for quicker responses |
| `/verbose` | Toggle verbose output for debugging |

### Example: Using /commit

The `/commit` command analyzes your staged changes and produces a conventional commit message:

```
> /commit

Analyzing staged changes...

Proposed commit message:
  feat: add password reset flow

  - Add POST /reset-password endpoint
  - Send reset email via SendGrid integration
  - Token expires after 1 hour
  - Added 4 integration tests

Create this commit? [Y/n]: Y
✓ Committed: a1b2c3d
```

> **Context-Awareness:** Slash commands like `/commit` and `/review` use Claude's full understanding of your codebase to produce much more relevant output than generic git tools.
