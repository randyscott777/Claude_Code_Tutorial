# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A self-contained Claude Code tutorial consisting of educational markdown files, a Python terminal menu navigator (`menu.py`), two Flask todo apps built as examples, and Claude Agent SDK demo scripts.

## Running the Tutorial Menu

```bash
python menu.py
```

Presents a numbered menu (supports decimal options like `1.1`, `2.1`) that renders tutorial markdown files using `rich`. Must be run from the project root.

Option 13 requires Google API client libraries (`google-auth`, `google-auth-oauthlib`, `google-api-python-client`) with credentials at `~/.config/mcp-gdrive/gcp-oauth.keys.json`.

## Tutorial Content Files (menu → file mapping)

| Menu | File | Topic |
|------|------|-------|
| 1.1 | `intro.md` | What Claude Code is |
| 1.2 | `overview.md` | Overview |
| 2 | `settings.md` | StatusLine and settings.json |
| 2.1–2.4 | system files | Raw settings.json content (global/project, normal/local) |
| 3 | `commands.md` | Slash commands |
| 4 | `memoryDoc.md` | Memory — CLAUDE.md, `/init`, `/memory` |
| 5 | `mcp.md` | MCP servers |
| 6 | `skills.md` | Available skills |
| 7 | `hooks.md` | Hook events and config |
| 8 | `git.md` | Git/GitHub integration |
| 9 | `tips.md` | Best practices |
| 10 | `sub_agents.md` | Sub-agents overview |
| 10.1 | `sub-agents.md` | Sub-agents practical guide |
| 11 | `todos.md` | Future development backlog |
| 12 | `cost.md` | Token usage and balances |
| 17 | `web.md` | Web and routines |
| 18 | `sdk.md` | Claude Agent SDK |
| 19 | `sdk_files_example.py` | Lists directory files via Agent SDK |
| 20 | `sdk_todos_example.py` | Lists TODO comments via Agent SDK |
| 22 | `vs-code.md` | VS Code integration |

## Example Apps

- **`todo_flask/`** — Flask todo app. SQLite DB at `todo_flask/todos.db`. Fields: title, description, priority (low/medium/high), due_date, completed. Run: `python todo_flask/app.py` (port 5000).
- **`todos_list/`** — Enhanced Flask todo dashboard with persisted filter/sort preferences stored in a `prefs` table. SQLite DB path is hardcoded to an absolute path in `todos_list/app.py:5` — update this if cloning. Fields: title, description, status (Not Started/In Progress/Done/Blocked), priority (Low/Medium/High/Urgent), due_date. Run: `python todos_list/app.py` (port 5000). Launch via `/open-todos` skill.
- **`todo_cli.py`** — Click-based CLI todo manager. SQLite DB at `~/.todos.db`. Run: `python todo_cli.py menu`.
- **`todo_kivy/`** — Kivy mobile app. Has `tests/` and `buildozer.spec` for Android.
- **`django_todo/`** — Django todo app. Run: `python django_todo/manage.py runserver`.

## SDK Demo Scripts

- **`sdk_files_example.py`** — Uses `claude_agent_sdk.query()` with `ClaudeAgentOptions` to list files via Bash/Glob tools.
- **`sdk_todos_example.py`** — Similar pattern; finds TODO comments. Loaded via `exec()` from menu option 20.

## Project-Level Skills and Commands

Custom skills live in `.claude/skills/` and slash commands in `.claude/commands/`:

- `/deadcode` — Runs `vulture` (min-confidence 80) to find unused Python code; groups by category, asks before removing.
- `/open-todos` — Starts `todos_list/app.py` and opens browser.
- `/commit-status`, `/log`, `/hello-world`, `/codebase-visualizer`, `/field-extractor` — see respective `SKILL.md` files.

## Stop Hook

`.claude/settings.json` registers a `Stop` hook that fires a Windows toast notification ("Claude has finished!") using PowerShell + `System.Windows.Forms.NotifyIcon` after every Claude response.

## Extending the Tutorial Menu

1. Create `<topic>.md` in the project root.
2. Add a `print("N. <topic>")` line in `menu.py`.
3. Add `if option == N: show("<topic>.md")` below the input line.

Menu option numbers are parsed as `float`, so decimal options (e.g. `10.1`) work natively.

## Config Files

- `.claude/settings.json` — project-level Claude Code settings (committed; contains Stop hook).
- `.claude/settings.local.json` — personal auto-approval overrides (not committed).

---
*Last updated: 2026-05-02*
