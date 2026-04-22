# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A self-contained Claude Code tutorial consisting of educational markdown files, a Python terminal menu navigator, and several example todo apps built in different frameworks (CLI, Flask, Kivy, Django).

## Running the Tutorial Menu

```bash
python menu.py
```

Presents a numbered menu that renders any tutorial markdown file using `rich`. Must be run from the project root. Requires `rich` and, for option 13, Google API client libraries.

## Tutorial Content Files

| File | Topic |
|------|-------|
| `intro.md` | What Claude Code is and its core capabilities |
| `setup.md` | Installation, authentication, config file locations |
| `commands.md` | Slash commands reference |
| `memory.md` | CLAUDE.md purpose, `/init`, `/memory` command |
| `hooks.md` | Hook events (PreToolUse, PostToolUse, Stop) and config |
| `mcp.md` | MCP servers — adding, configuring, managing |
| `skills.md` | Available skills |
| `git.md` | Git/GitHub integration, PR workflow, `gh` CLI |
| `tips.md` | Best practices and antipatterns |
| `cost.md` | Token usage and balances |
| `StatusLine.md` | Custom status line configuration |
| `todos.md` | Future development backlog |

## Example Apps

- **`todo_cli.py`** — Click-based CLI todo manager. SQLite DB at `~/.todos.db`. Run: `python todo_cli.py` or `python todo_cli.py menu` for interactive mode.
- **`todo_flask/`** — Flask web todo app. SQLite DB at `todo_flask/todos.db`. Run: `python todo_flask/app.py` (starts on port 5000).
- **`todo_kivy/`** — Kivy mobile todo app (`main.py`). Has `tests/` subdirectory and `buildozer.spec` for Android builds.
- **`django_todo/`** — Django todo app. Run: `python django_todo/manage.py runserver`.

## Extending the Tutorial Menu

When adding a new topic file:
1. Create `<topic>.md` in the project root.
2. Add a `print("N. <topic>")` line to the menu output in `menu.py`.
3. Add a corresponding `if option == N:` block calling `show("<topic>.md")`.

## Config Files

- `.claude/settings.json` — project-level Claude Code settings (committed).
- `.claude/settings.local.json` — personal auto-approval overrides (not committed).
