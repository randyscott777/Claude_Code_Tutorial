"""Logs each message to a local SQLite database (messages.db).

Creates the table on first run. Displays the message and a count of
all entries logged so far.

Usage:
    python log_greeting.py [message]
    python log_greeting.py --history
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "messages.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    return conn


def log_message(message: str) -> int:
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO messages (message, created_at) VALUES (?, ?)",
            (message, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
        row = conn.execute(
            "SELECT COUNT(*) FROM messages").fetchone()
        return row[0]
    finally:
        conn.close()


def show_history() -> None:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT message, created_at FROM messages ORDER BY id DESC LIMIT 10").fetchall()
    finally:
        conn.close()

    if not rows:
        print(f"No messages logged yet.")
        return

    print(f"Last {len(rows)} message:")
    for (msg, ts) in rows:
        print(f"  - [{ts}] {msg}")


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--history":
        show_history()
        return

    message = args[0] #if args else "World"
    count = log_message(message)
    today = datetime.now().date().isoformat()
    print(f"For {today} logged {message}!")
    print(f"(That's message #{count} for you in the log.)")


if __name__ == "__main__":
    main()
