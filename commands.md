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

### Command Claude Code commands, switches, and keyboard shortcuts

Prompts can be anything with double quotes, for example:
- claude to start the Claude Code agent
- claude /doctor to display diagnostic and update settings
- claude --version will display the version in 1.2.3 format
- claude "What does this project do?"
- claude -p "prompt" switch executes the prompt and returns to the command line
- claude -c switch continues the current conversation
- claude -r switch continues the previous conversation
- claude /help will display a link to Claude Code website for the options
- claude /model modelname' will use the model specified or blank for the picker
Note: use opus for planning and then sonnet for building
- claude /clear will clear the current conversation
- claude /exit or Ctrl-C will end claude code agent and return to the command line
- shift-tab in the agent to toggle between plan mode, shortcuts, and accept edits
- claude /status to display status, config, and usage
