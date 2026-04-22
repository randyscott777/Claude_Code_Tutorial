# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A self-contained Claude Code tutorial consisting of educational markdown files and a Python menu navigator. The content teaches users how to install, configure, and effectively use Claude Code.

## Running the Tutorial Menu

```bash
python menu.py
```

Presents a numbered menu to display any tutorial file. Files are read from the current working directory, so the script must be run from the project root.

## Content Structure

Each markdown file covers a distinct Claude Code topic:

| File | Topic |
|------|-------|
| `intro.md` | What Claude Code is and its core capabilities |
| `setup.md` | Installation, authentication, and config file locations |
| `commands.md` | Slash commands reference (`/commit`, `/plan`, `/review`, etc.) |
| `memory.md` | CLAUDE.md purpose,'/init' and `/memory` command, memory file hierarchy |
| `hooks.md` | Hook events (PreToolUse, PostToolUse, Stop) and configuration patterns |
| `mcp.md` | MCP servers — adding, configuring, and managing external tool integrations |
| `skills.md` | Available skills (`keybindings-help`, `simplify`, `claude-developer-platform`) |
| `git.md` | Git/GitHub integration, PR workflow, safety rules, `gh` CLI usage |
| `tips.md` | Best practices and antipatterns for effective Claude Code usage |

## Config Files

`.claude/settings.local.json` grants auto-approval for `start:*` and `node:*` Bash commands locally. Project-level settings belong in `.claude/settings.json` (committed); personal overrides go in `.claude/settings.local.json` (not committed).

## Extending the Tutorial

When adding a new topic file:
1. Create the `<topic>.md` file in the project root
2. Add a corresponding `if opt == "N":` block in `menu.py` (following the existing pattern)
3. Add a `print("N. <topic>.md")` line to the menu output in `menu.py`
