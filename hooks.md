Hooks let you run custom shell commands automatically in response to Claude Code events. They're powerful for enforcing code quality, sending notifications, logging, and automating your workflow.

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code’s lifecycle. Use Claude Code Docs reference to look up event schemas, configuration options, JSON input/output formats, and advanced features like async hooks, HTTP hooks, and MCP tool hooks.

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

###Event	and When it fires
* SessionStart	     When a session begins or resumes
* UserPromptSubmit	 When you submit a prompt, before Claude processes it
* PreToolUse	       Before a tool call executes. Can block it
* PermissionRequest	 When a permission dialog appears
* PostToolUse	       After a tool call succeeds
* PostToolUseFailure After a tool call fails
* Notification	     When Claude Code sends a notification
* SubagentStart	     When a subagent is spawned
* SubagentStop	     When a subagent finishes
* Stop	             When Claude finishes responding
* TeammateIdle	     When an agent team teammate is about to go idle
* TaskCompleted	     When a task is being marked as completed
* ConfigChange	     When a configuration file changes during a session
* WorktreeCreate	   When a worktree is being created via --worktree or isolation: "worktree". Replaces default git behavior
* WorktreeRemove	   When a worktree is being removed, either at session exit or when a subagent finishes
* PreCompact	       Before context compaction
* SessionEnd	       When a session terminates

# Config of my Claude stop notification (in .claude/settings.json)
"hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"Add-Type -AssemblyName System.Windows.Forms; \\$n = New-Object System.Windows.Forms.NotifyIcon; \\$n.Icon = [System.Drawing.SystemIcons]::Information; \\$n.Visible = \\$true; \\$n.ShowBalloonTip(3000, 'Claude Done', 'Claude has finished!', 'Info'); Start-Sleep -Seconds 4; \\$n.Dispose()\""
          }
        ]
      }
    ]
  }
​
