# Claude Code in Visual Studio Code
### Tips, Techniques & Best Practices created via Claude Chat

---

## Installation & Setup

- **VS Code version**: 1.98.0 or newer required
- **Install the extension**: `Ctrl+Shift+X` → search "Claude Code" → install the official **Anthropic** publisher (not third-party clones)
- **Account required**: Claude Pro, Max, Team, or Enterprise subscription — or pay-as-you-go API credits
- The CLI auto-installs the extension the first time you run `claude` in VS Code's integrated terminal
- **Restart VS Code** or run `Developer: Reload Window` from the Command Palette if the extension doesn't appear after install

---

## Navigating the Interface

| Entry Point | How to Access |
|---|---|
| Spark icon (editor toolbar) | Top-right corner of any open file |
| Activity Bar | Left sidebar — always visible, opens sessions list |
| Status Bar | Click `✱ Claude Code` in the bottom-right corner |
| Command Palette | `Ctrl+Shift+P` → search "Claude Code" |

- **Drag the panel** to reposition it anywhere in the VS Code layout
- **Multiple conversations**: open separate tabs or windows via the sessions list in the Activity Bar
- **Sidebar mode**: search `claudeCode.preferredLocation` in Settings and set it to `sidebar` to dock Claude next to Copilot Chat
- To auto-open Claude on startup, use the `auto-run-command` extension with command `claude-vscode.sidebar.open`

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Option+K` / `Alt+K` | Insert an `@file.ts#5-10` mention from your selection |
| `Ctrl+R` | Search prompt history in the terminal |
| `Cmd+N` / `Ctrl+N` | Start a new conversation |
| `Esc` twice | Rewind to the last checkpoint |
| `Shift+Enter` | Multi-line input (run `/terminal-setup` to configure) |

---

## Context & File References

- **Highlight code first**: select any snippet before typing a prompt — Claude automatically receives it as context
- **@-mentions**: type `@filename` or `@filename#10-25` to reference specific files and line ranges
- **Open tabs as context**: the extension tells Claude which files you have open, improving suggestion relevance
- **Lint errors are auto-shared**: syntax and diagnostic errors are automatically included in Claude's context

---

## Working with Diffs & Edits

- When Claude proposes a change, it opens VS Code's **native diff viewer** automatically — side-by-side, with accept/reject buttons
- **Plan mode**: review and edit Claude's plan *before* it makes any changes — critical for large refactors
- **Auto-accept**: enable in settings for trusted workflows where you want uninterrupted implementation
- **Extended Thinking**: toggle the reasoning button (bottom-right of prompt input) to see Claude's thought process before changes are applied

---

## Checkpoints & Rewinding

- Claude automatically saves your code state **before each change**
- To rewind: press `Esc` twice or run `/rewind`
- On rewind, choose to restore **code**, **conversation**, or **both**
- Checkpoints apply to Claude's edits only — not your own edits or bash commands
- **Always use checkpoints alongside version control** (git), not as a replacement

---

## Slash Commands

| Command | Purpose |
|---|---|
| `/clear` | Clear conversation history to free up context tokens |
| `/rewind` | Roll back to a previous checkpoint |
| `/model` | Switch between Claude models |
| `/plugins` | Open the plugin manager |
| `/terminal-setup` | Auto-configure `Shift+Enter` for multi-line input |

**Custom commands**: create a `.claude/commands/` folder in your project. Add `.md` files named after each command, written in natural language. Use `$ARGUMENTS` as a placeholder for dynamic input.

```
.claude/
  commands/
    add-tests.md
    explain-function.md
```

---

## Context Management

- **Use `/clear` frequently**: start every new task with a fresh context — old history wastes tokens and triggers unnecessary compaction
- **Use `↑` arrow** to navigate back through past prompts, even across sessions
- **One session per workspace folder**: run separate Claude sessions for separate projects or microservices — each maintains isolated context
- Keep prompts **specific and verifiable**: e.g., "Add JSDoc to all exported functions in `src/utils.js`" beats "document my code"

---

## Permissions & Autonomy

- By default, Claude asks permission before editing files or running commands
- To skip permission prompts for trusted sessions: `claude --dangerously-skip-permissions` (use with caution)
- **Auto-edit mode** in VS Code can allow Claude to modify IDE config files — be aware this may bypass some bash permission prompts
- **Background tasks**: Claude can keep long-running processes (e.g., dev servers) active without blocking its progress on other work

---

## MCP Server Integration

- Configure MCP servers through the **CLI first** — the extension then picks them up automatically
- Subagents must also be configured via CLI before using them in VS Code
- Third-party providers (Amazon Bedrock, Google Vertex AI): set environment variables in the Claude Code extension settings — no login prompt will appear

---

## Terminal vs. Extension — When to Use Each

| Situation | Use |
|---|---|
| Visual diff review, plan mode, inline accept/reject | **Extension (GUI panel)** |
| Full CLI flags, scripting, piping to other tools | **Integrated terminal** |
| Parallel sessions on different parts of a codebase | **Multiple extension tabs** |
| CI/CD environments | **CLI only** (set `CLAUDE_CODE_DISABLE_AUTO_UPDATER=1` to prevent auto-install) |

---

## Prompting Tips

- **Be specific about scope**: name the file, function, and what outcome you want
- **Verify with small tasks first**: open a real project and test a simple, verifiable task before delegating complex work
- **Iterate in plan mode**: for large changes, review and adjust the plan before giving Claude the green light
- **Reference line numbers**: `@src/app.py#42-67` is far more precise than "that function near the top"
- **State constraints explicitly**: "do not change the public API" or "keep the same file structure"

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Extension doesn't appear after install | Restart VS Code or run `Developer: Reload Window` |
| Panel disappears after restart | Run `Claude Code: Open in sidebar` from Command Palette, or add a keybinding |
| Wrong extension installed | Uninstall and reinstall — verify publisher is **Anthropic** |
| Multi-line input not working | Run `/terminal-setup` inside a Claude session |
| Windows keybinding conflicts | Use `Alt+V` for image paste; `Meta+M` for permission mode cycling |
| WSL issues | Ensure WSL2 is configured and VS Code's WSL extension is installed |

---

## Resources

- [Official Claude Code Docs](https://docs.claude.com/en/docs/claude-code/overview)
- [VS Code Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
- [Claude Code on Amazon Bedrock](https://docs.claude.com/en/docs/claude-code/bedrock)
- [Claude Code on Google Vertex AI](https://docs.claude.com/en/docs/claude-code/vertex)

