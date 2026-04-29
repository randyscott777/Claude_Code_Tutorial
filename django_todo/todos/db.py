import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'db.sqlite3'

_initialized = False


def get_conn():
    global _initialized
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    if not _initialized:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS todos_todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            '''
        )
        conn.commit()
        _initialized = True
    return conn


def list_todos():
    with get_conn() as conn:
        rows = conn.execute(
            'SELECT id, title, completed, created_at FROM todos_todo '
            'ORDER BY completed ASC, created_at DESC'
        ).fetchall()
    return [dict(r) for r in rows]


def get_todo(todo_id):
    with get_conn() as conn:
        row = conn.execute(
            'SELECT id, title, completed, created_at FROM todos_todo WHERE id = ?',
            (todo_id,),
        ).fetchone()
    return dict(row) if row else None


def create_todo(title):
    created_at = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        conn.execute(
            'INSERT INTO todos_todo (title, completed, created_at) VALUES (?, 0, ?)',
            (title, created_at),
        )
        conn.commit()


def update_title(todo_id, title):
    with get_conn() as conn:
        conn.execute(
            'UPDATE todos_todo SET title = ? WHERE id = ?',
            (title, todo_id),
        )
        conn.commit()


def toggle_completed(todo_id):
    with get_conn() as conn:
        conn.execute(
            'UPDATE todos_todo SET completed = 1 - completed WHERE id = ?',
            (todo_id,),
        )
        conn.commit()


def delete_todo(todo_id):
    with get_conn() as conn:
        conn.execute('DELETE FROM todos_todo WHERE id = ?', (todo_id,))
        conn.commit()
