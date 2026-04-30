import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PATH = r"C:\Users\randy\OneDrive\VisualStudioCode\Claude_Code_Tutorial\todos_list\todos.db"

STATUS_OPTIONS = ["Not Started", "In Progress", "Done"]
PRIORITY_OPTIONS = ["Low", "Medium", "High", "Urgent"]
SORT_FIELDS = ["id", "title", "status", "priority", "due_date", "created_at"]

DEFAULT_SETTINGS = {
    "filter_status": "",
    "filter_priority": "",
    "sort_field": "created_at",
    "sort_dir": "desc",
}


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Not Started',
            priority TEXT NOT NULL DEFAULT 'Medium',
            due_date TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )
    for k, v in DEFAULT_SETTINGS.items():
        cur.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            (k, v),
        )
    conn.commit()
    conn.close()


def get_settings():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM settings")
    rows = cur.fetchall()
    conn.close()
    settings = dict(DEFAULT_SETTINGS)
    for row in rows:
        settings[row["key"]] = row["value"]
    return settings


def save_settings(updates):
    conn = get_conn()
    cur = conn.cursor()
    for k, v in updates.items():
        cur.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (k, v),
        )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    settings = get_settings()

    where = []
    params = []
    if settings["filter_status"]:
        where.append("status = ?")
        params.append(settings["filter_status"])
    if settings["filter_priority"]:
        where.append("priority = ?")
        params.append(settings["filter_priority"])

    sort_field = settings["sort_field"] if settings["sort_field"] in SORT_FIELDS else "created_at"
    sort_dir = "ASC" if settings["sort_dir"] == "asc" else "DESC"

    sql = "SELECT * FROM todos"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += f" ORDER BY {sort_field} {sort_dir}"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, params)
    todos = cur.fetchall()
    conn.close()

    return render_template(
        "index.html",
        todos=todos,
        settings=settings,
        status_options=STATUS_OPTIONS,
        priority_options=PRIORITY_OPTIONS,
        sort_fields=SORT_FIELDS,
    )


@app.route("/filter", methods=["POST"])
def filter_sort():
    save_settings(
        {
            "filter_status": request.form.get("filter_status", ""),
            "filter_priority": request.form.get("filter_priority", ""),
            "sort_field": request.form.get("sort_field", "created_at"),
            "sort_dir": request.form.get("sort_dir", "desc"),
        }
    )
    return redirect(url_for("index"))


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO todos (title, description, status, priority, due_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                request.form["title"].strip(),
                request.form.get("description", "").strip(),
                request.form.get("status", "Not Started"),
                request.form.get("priority", "Medium"),
                request.form.get("due_date") or None,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template(
        "create.html",
        status_options=STATUS_OPTIONS,
        priority_options=PRIORITY_OPTIONS,
    )


@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    conn = get_conn()
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute(
            "UPDATE todos SET title = ?, description = ?, status = ?, "
            "priority = ?, due_date = ? WHERE id = ?",
            (
                request.form["title"].strip(),
                request.form.get("description", "").strip(),
                request.form.get("status", "Not Started"),
                request.form.get("priority", "Medium"),
                request.form.get("due_date") or None,
                todo_id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    cur.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = cur.fetchone()
    conn.close()
    if not todo:
        return redirect(url_for("index"))
    return render_template(
        "edit.html",
        todo=todo,
        status_options=STATUS_OPTIONS,
        priority_options=PRIORITY_OPTIONS,
    )


@app.route("/delete/<int:todo_id>", methods=["GET", "POST"])
def delete(todo_id):
    conn = get_conn()
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    cur.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = cur.fetchone()
    conn.close()
    if not todo:
        return redirect(url_for("index"))
    return render_template("delete.html", todo=todo)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
