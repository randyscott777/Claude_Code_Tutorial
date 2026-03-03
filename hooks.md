Hooks let you run custom shell commands automatically in response to Claude Code events. They're powerful for enforcing code quality, sending notifications, logging, and automating your workflow.

## What Are Hooks?

Hooks are shell commands defined in your `settings.json` that execute at specific lifecycle points:

- **PreToolUse** — Fires before Claude uses any tool (read, write, bash, etc.)
- **PostToolUse** — Fires after a tool completes successfully
- **Notification** — Fires when Claude sends you a notification
- **Stop** — Fires when Claude finishes a task

## Configuring Hooks

Add hooks to `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint -- --fix"
          }
        ]
      }
    ]
  }
}
```

This automatically runs ESLint auto-fix every time Claude writes a file.

## Common Hook Patterns

### Auto-format on every write

```json
{
  "matcher": "Write",
  "hooks": [{ "type": "command", "command": "prettier --write \"$CLAUDE_TOOL_FILE\"" }]
}
```

### Run tests after file changes

```json
{
  "matcher": "Write",
  "hooks": [{ "type": "command", "command": "npm test -- --passWithNoTests" }]
}
```

### Desktop notification when task completes

```json
{
  "event": "Stop",
  "hooks": [{ "type": "command", "command": "notify-send 'Claude Code' 'Task complete!'" }]
}
```

## Hook Exit Codes

Hooks can influence Claude's behavior through their exit code and output:

- **Exit 0** — Success, Claude continues as normal
- **Non-zero exit** — Hook failed; Claude sees the output and may adjust its approach
- **Stdout** — Hook output is fed back to Claude as additional context

> **Audit Trail:** Use a PreToolUse hook on Bash commands to log every command Claude runs to a file — great for security auditing in team environments.
