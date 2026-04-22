import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = "todos.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.commit()
    db.close()


@app.route("/")
def index():
    db = get_db()
    filter_status = request.args.get("status", "all")
    filter_priority = request.args.get("priority", "all")

    query = "SELECT * FROM todos WHERE 1=1"
    params = []

    if filter_status == "active":
        query += " AND completed = 0"
    elif filter_status == "done":
        query += " AND completed = 1"

    if filter_priority in ("low", "medium", "high"):
        query += " AND priority = ?"
        params.append(filter_priority)

    query += " ORDER BY completed ASC, CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, due_date ASC"

    todos = db.execute(query, params).fetchall()

    total = db.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
    done = db.execute("SELECT COUNT(*) FROM todos WHERE completed = 1").fetchone()[0]
    active = total - done
    high = db.execute("SELECT COUNT(*) FROM todos WHERE priority='high' AND completed=0").fetchone()[0]

    return render_template(
        "index.html",
        todos=todos,
        total=total,
        done=done,
        active=active,
        high=high,
        filter_status=filter_status,
        filter_priority=filter_priority,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date", "")
        if title:
            db = get_db()
            db.execute(
                "INSERT INTO todos (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
                (title, description, priority, due_date or None),
            )
            db.commit()
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    db = get_db()
    todo = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if todo is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date", "")
        if title:
            db.execute(
                "UPDATE todos SET title=?, description=?, priority=?, due_date=? WHERE id=?",
                (title, description, priority, due_date or None, todo_id),
            )
            db.commit()
        return redirect(url_for("index"))

    return render_template("edit.html", todo=todo)


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    db = get_db()
    db.execute(
        "UPDATE todos SET completed = CASE WHEN completed=1 THEN 0 ELSE 1 END WHERE id=?",
        (todo_id,),
    )
    db.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
