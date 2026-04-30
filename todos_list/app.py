import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, g

DB_PATH = r"C:\Users\randy\OneDrive\VisualStudioCode\Claude_Code_Tutorial\todos_list\todos.db"

STATUSES = ["Not Started", "In Progress", "Done", "Blocked"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]
SORT_FIELDS = ["title", "status", "priority", "due_date", "created_at"]
SORT_DIRS = ["asc", "desc"]

app = Flask(__name__)


def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(_):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()


def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Not Started',
            priority TEXT NOT NULL DEFAULT 'Medium',
            due_date TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prefs (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    for k, v in [
        ("filter_status", "All"),
        ("filter_priority", "All"),
        ("sort_field", "created_at"),
        ("sort_dir", "desc"),
    ]:
        cur.execute("INSERT OR IGNORE INTO prefs (key, value) VALUES (?, ?)", (k, v))
    con.commit()
    con.close()


def get_prefs():
    rows = get_db().execute("SELECT key, value FROM prefs").fetchall()
    return {r["key"]: r["value"] for r in rows}


def set_pref(key, value):
    db = get_db()
    db.execute("UPDATE prefs SET value = ? WHERE key = ?", (value, key))
    db.commit()


@app.route("/")
def index():
    prefs = get_prefs()
    db = get_db()

    where, params = [], []
    if prefs["filter_status"] != "All":
        where.append("status = ?")
        params.append(prefs["filter_status"])
    if prefs["filter_priority"] != "All":
        where.append("priority = ?")
        params.append(prefs["filter_priority"])
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    sort_field = prefs["sort_field"] if prefs["sort_field"] in SORT_FIELDS else "created_at"
    sort_dir = prefs["sort_dir"] if prefs["sort_dir"] in SORT_DIRS else "desc"
    direction = "ASC" if sort_dir == "asc" else "DESC"

    if sort_field == "priority":
        order_sql = (
            f"CASE priority WHEN 'Urgent' THEN 1 WHEN 'High' THEN 2 "
            f"WHEN 'Medium' THEN 3 WHEN 'Low' THEN 4 END {direction}"
        )
    elif sort_field == "status":
        order_sql = (
            f"CASE status WHEN 'Not Started' THEN 1 WHEN 'In Progress' THEN 2 "
            f"WHEN 'Blocked' THEN 3 WHEN 'Done' THEN 4 END {direction}"
        )
    else:
        order_sql = f"{sort_field} {direction}"

    todos = db.execute(
        f"SELECT * FROM todos {where_sql} ORDER BY {order_sql}", params
    ).fetchall()

    today = date.today().isoformat()
    stats = {
        "total": db.execute("SELECT COUNT(*) FROM todos").fetchone()[0],
        "not_started": db.execute("SELECT COUNT(*) FROM todos WHERE status = 'Not Started'").fetchone()[0],
        "in_progress": db.execute("SELECT COUNT(*) FROM todos WHERE status = 'In Progress'").fetchone()[0],
        "done": db.execute("SELECT COUNT(*) FROM todos WHERE status = 'Done'").fetchone()[0],
        "blocked": db.execute("SELECT COUNT(*) FROM todos WHERE status = 'Blocked'").fetchone()[0],
        "overdue": db.execute(
            "SELECT COUNT(*) FROM todos WHERE due_date IS NOT NULL AND due_date < ? AND status != 'Done'",
            (today,),
        ).fetchone()[0],
    }

    return render_template(
        "index.html",
        todos=todos,
        prefs=prefs,
        stats=stats,
        statuses=STATUSES,
        priorities=PRIORITIES,
        sort_fields=SORT_FIELDS,
        today=today,
    )


@app.route("/prefs", methods=["POST"])
def update_prefs():
    set_pref("filter_status", request.form.get("filter_status", "All"))
    set_pref("filter_priority", request.form.get("filter_priority", "All"))
    set_pref("sort_field", request.form.get("sort_field", "created_at"))
    set_pref("sort_dir", request.form.get("sort_dir", "desc"))
    return redirect(url_for("index"))


@app.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            return render_template(
                "create.html",
                statuses=STATUSES, priorities=PRIORITIES,
                error="Title is required.", form=request.form,
            )
        db = get_db()
        db.execute(
            "INSERT INTO todos (title, description, status, priority, due_date) VALUES (?, ?, ?, ?, ?)",
            (
                title,
                request.form.get("description", "").strip() or None,
                request.form.get("status", "Not Started"),
                request.form.get("priority", "Medium"),
                request.form.get("due_date") or None,
            ),
        )
        db.commit()
        return redirect(url_for("index"))
    return render_template("create.html", statuses=STATUSES, priorities=PRIORITIES, form={})


@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        todo = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if not todo:
            return redirect(url_for("index"))
        if not title:
            return render_template(
                "edit.html", todo=todo,
                statuses=STATUSES, priorities=PRIORITIES,
                error="Title is required.",
            )
        db.execute(
            "UPDATE todos SET title = ?, description = ?, status = ?, priority = ?, due_date = ? WHERE id = ?",
            (
                title,
                request.form.get("description", "").strip() or None,
                request.form.get("status", "Not Started"),
                request.form.get("priority", "Medium"),
                request.form.get("due_date") or None,
                todo_id,
            ),
        )
        db.commit()
        return redirect(url_for("index"))
    todo = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not todo:
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo, statuses=STATUSES, priorities=PRIORITIES)


@app.route("/delete/<int:todo_id>", methods=["GET", "POST"])
def delete(todo_id):
    db = get_db()
    if request.method == "POST":
        db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        db.commit()
        return redirect(url_for("index"))
    todo = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not todo:
        return redirect(url_for("index"))
    return render_template("delete.html", todo=todo)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
