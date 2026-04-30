# todos_list — Build Notes

## What it is
A Flask todo app with a Monday.com-style dashboard. No JavaScript. Persists data and user preferences in SQLite via raw SQL.

## Design choices
- **Single-row-per-key `prefs` table** stores filter and sort selections so they survive across sessions.
- **Hardcoded absolute DB path** (per global rule) — `todos_list/todos.db`.
- **Custom status/priority sort order** via SQL `CASE` so "Urgent → Low" and "Not Started → Done" sort by severity, not alphabetically.
- **Colored rectangle chips** for status and priority — Monday.com palette, white text on colored background.
- **Confirmation page** before delete (per global rule).
- **No JavaScript** — filter/sort changes are submitted via a plain `<form>` with an Apply button.

## Schema
- `todos(id, title, description, status, priority, due_date, created_at)`
- `prefs(key, value)` — keys: `filter_status`, `filter_priority`, `sort_field`, `sort_dir`.

## Run
```
python todos_list/app.py
```
Then open http://localhost:5000.
