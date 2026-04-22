import sqlite3
import calendar
from datetime import datetime, date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "todos.db"

RECURRENCE_OPTIONS = ["none", "daily", "weekly", "monthly", "yearly"]
PRIORITY_OPTIONS = ["low", "med", "high"]
PRIORITY_ORDER = {"high": 0, "med": 1, "low": 2}


# ---------------------------------------------------------------------------
# Connection & schema
# ---------------------------------------------------------------------------

def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                done        INTEGER NOT NULL DEFAULT 0,
                due_date    TEXT,
                priority    TEXT    NOT NULL DEFAULT 'med',
                created_at  TEXT    NOT NULL,
                category_id INTEGER,
                notes       TEXT,
                recurrence  TEXT    NOT NULL DEFAULT 'none',
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)
        conn.commit()


# ---------------------------------------------------------------------------
# Categories — CRUD
# ---------------------------------------------------------------------------

def create_category(name, db_path=DB_PATH):
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO categories (name) VALUES (?)", (name,)
        )
        conn.commit()
        return cursor.lastrowid


def get_categories(db_path=DB_PATH):
    with get_connection(db_path) as conn:
        return [dict(row) for row in conn.execute(
            "SELECT * FROM categories ORDER BY name"
        )]


def get_category(category_id, db_path=DB_PATH):
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM categories WHERE id=?", (category_id,)
        ).fetchone()
        return dict(row) if row else None


def update_category(category_id, name, db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.execute(
            "UPDATE categories SET name=? WHERE id=?", (name, category_id)
        )
        conn.commit()


def delete_category(category_id, db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM categories WHERE id=?", (category_id,))
        conn.commit()


def get_category_task_counts(db_path=DB_PATH):
    """Return {category_id: task_count} for all categories that have tasks."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT category_id, COUNT(*) AS cnt FROM todos "
            "WHERE category_id IS NOT NULL GROUP BY category_id"
        ).fetchall()
        return {row["category_id"]: row["cnt"] for row in rows}


# ---------------------------------------------------------------------------
# Todos — CRUD
# ---------------------------------------------------------------------------

def create_todo(
    title,
    due_date=None,
    priority="med",
    category_id=None,
    notes=None,
    recurrence="none",
    db_path=DB_PATH,
):
    created_at = datetime.now().isoformat()
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO todos
                (title, done, due_date, priority, created_at, category_id, notes, recurrence)
            VALUES (?, 0, ?, ?, ?, ?, ?, ?)
            """,
            (title, due_date, priority, created_at, category_id, notes, recurrence),
        )
        conn.commit()
        return cursor.lastrowid


def get_todo(todo_id, db_path=DB_PATH):
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM todos WHERE id=?", (todo_id,)
        ).fetchone()
        return dict(row) if row else None


def get_todos(
    search=None,
    category_id=None,
    priority=None,
    done=None,
    sort_by="created_at",
    sort_dir="DESC",
    db_path=DB_PATH,
):
    """Return todos with optional filtering and sorting.

    sort_by options : created_at | due_date | priority | title
    sort_dir options: ASC | DESC
    """
    _valid_sort_cols = {"created_at", "due_date", "priority", "title"}
    _valid_sort_dirs = {"ASC", "DESC"}
    sort_by = sort_by if sort_by in _valid_sort_cols else "created_at"
    sort_dir = sort_dir.upper() if sort_dir.upper() in _valid_sort_dirs else "DESC"

    query = "SELECT * FROM todos WHERE 1=1"
    params = []

    if search:
        query += " AND (title LIKE ? OR notes LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if category_id is not None:
        query += " AND category_id=?"
        params.append(category_id)

    if priority is not None:
        query += " AND priority=?"
        params.append(priority)

    if done is not None:
        query += " AND done=?"
        params.append(1 if done else 0)

    # Priority sort needs special ordering (high > med > low), handled in Python
    if sort_by == "priority":
        with get_connection(db_path) as conn:
            rows = [dict(r) for r in conn.execute(query, params)]
        reverse = sort_dir == "ASC"  # PRIORITY_ORDER: high=0, so ascending key = high first
        return sorted(rows, key=lambda r: PRIORITY_ORDER.get(r["priority"], 99), reverse=reverse)

    query += f" ORDER BY {sort_by} {sort_dir}"
    with get_connection(db_path) as conn:
        return [dict(row) for row in conn.execute(query, params)]


def update_todo(todo_id, db_path=DB_PATH, **fields):
    allowed = {"title", "done", "due_date", "priority", "category_id", "notes", "recurrence"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return
    set_clause = ", ".join(f"{k}=?" for k in updates)
    values = list(updates.values()) + [todo_id]
    with get_connection(db_path) as conn:
        conn.execute(f"UPDATE todos SET {set_clause} WHERE id=?", values)
        conn.commit()


def delete_todo(todo_id, db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM todos WHERE id=?", (todo_id,))
        conn.commit()


def toggle_done(todo_id, db_path=DB_PATH):
    with get_connection(db_path) as conn:
        conn.execute("UPDATE todos SET done = 1 - done WHERE id=?", (todo_id,))
        conn.commit()


# ---------------------------------------------------------------------------
# Recurrence helpers
# ---------------------------------------------------------------------------

def _add_months(d, months):
    """Add a number of months to a date, clamping to the last day of the month."""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    max_day = calendar.monthrange(year, month)[1]
    return d.replace(year=year, month=month, day=min(d.day, max_day))


def get_next_due_date(due_date_str, recurrence):
    """Return the next ISO due date string after today for a recurring todo.

    Returns None if recurrence is 'none' or due_date_str is falsy.
    """
    if not due_date_str or recurrence == "none":
        return None

    due = date.fromisoformat(due_date_str)
    today = date.today()

    if recurrence == "daily":
        next_due = due + timedelta(days=1)
        if next_due <= today:
            # Jump directly to tomorrow rather than looping
            next_due = today + timedelta(days=1)
        return next_due.isoformat()

    if recurrence == "weekly":
        next_due = due + timedelta(weeks=1)
        while next_due <= today:
            next_due += timedelta(weeks=1)
        return next_due.isoformat()

    if recurrence == "monthly":
        next_due = _add_months(due, 1)
        while next_due <= today:
            next_due = _add_months(next_due, 1)
        return next_due.isoformat()

    if recurrence == "yearly":
        next_due = due.replace(year=due.year + 1)
        while next_due <= today:
            next_due = next_due.replace(year=next_due.year + 1)
        return next_due.isoformat()

    return None


def advance_recurrence(todo_id, db_path=DB_PATH):
    """When a recurring todo is marked done, set its due_date to the next
    occurrence and reset done to 0."""
    todo = get_todo(todo_id, db_path)
    if not todo:
        return
    next_due = get_next_due_date(todo["due_date"], todo["recurrence"])
    if next_due:
        update_todo(todo_id, db_path=db_path, due_date=next_due, done=0)
