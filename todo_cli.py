import sqlite3
import os
from datetime import datetime
import click

DB_PATH = os.path.expanduser("~/.todos.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT NOT NULL,
                done       INTEGER DEFAULT 0,
                priority   TEXT DEFAULT 'med',
                due_date   TEXT,
                tags       TEXT,
                created_at TEXT NOT NULL
            )
        """)


def priority_color(pri):
    return {"high": "red", "med": "yellow", "low": "cyan"}.get(pri, "white")


def format_row(row):
    done_mark = click.style("[x]", fg="green") if row["done"] else "[ ]"
    pri = (row["priority"] or "med").lower()
    pri_label = click.style(pri.upper().ljust(4), fg=priority_color(pri))
    due = row["due_date"] or "-"
    tags = row["tags"] or "-"
    title = row["title"]
    if row["done"]:
        title = click.style(title, dim=True)
    return f"  {row['id']:>3}  {pri_label}  {title:<30}  {due:<12}  {tags:<20}  {done_mark}"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A simple CLI to-do list manager."""
    init_db()
    if ctx.invoked_subcommand is None:
        ctx.invoke(list_tasks, show_all=True)


@cli.command()
@click.argument("title")
@click.option("--due", default=None, help="Due date (YYYY-MM-DD)")
@click.option("--priority", "-p", default="med", type=click.Choice(["low", "med", "high"]), help="Priority level")
@click.option("--tags", default=None, help="Comma-separated tags")
def add(title, due, priority, tags):
    """Add a new task."""
    now = datetime.now().isoformat(timespec="seconds")
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO todos (title, priority, due_date, tags, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, priority, due, tags, now),
        )
        task_id = cur.lastrowid
    click.echo(click.style(f"Added task #{task_id}: {title}", fg="green"))


@cli.command("list")
@click.option("--all", "show_all", is_flag=True, help="Include completed tasks")
@click.option("--tag", default=None, help="Filter by tag")
@click.option("--priority", "-p", default=None, type=click.Choice(["low", "med", "high"]), help="Filter by priority")
def list_tasks(show_all, tag, priority):
    """List tasks."""
    query = "SELECT * FROM todos WHERE 1=1"
    params = []
    if not show_all:
        query += " AND done = 0"
    if tag:
        query += " AND (',' || tags || ',' LIKE ?)"
        params.append(f"%,{tag},%")
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'med' THEN 2 ELSE 3 END, due_date ASC NULLS LAST, id ASC"

    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()

    if not rows:
        click.echo("No tasks found.")
    else:
        header = f"  {'ID':>3}  {'PRI ':<6}  {'TITLE':<30}  {'DUE':<12}  {'TAGS':<20}  STATUS"
        click.echo(click.style(header, bold=True))
        click.echo("-" * len(header))
        for row in rows:
            click.echo(format_row(row))

    click.echo()
    click.echo(click.style("Commands:", bold=True))
    click.echo("  add <title> [-p low|med|high] [--due YYYY-MM-DD] [--tags t1,t2]")
    click.echo("  done <id>")
    click.echo("  undone <id>")
    click.echo("  edit <id> [--title ...] [-p ...] [--due ...] [--tags ...]")
    click.echo("  delete <id>")
    click.echo("  list [--all] [--tag <tag>] [-p low|med|high]")
    click.echo("  clear [--done]")
    click.echo("  menu")


@cli.command()
@click.argument("task_id", type=int)
def done(task_id):
    """Mark a task as complete."""
    with get_db() as conn:
        cur = conn.execute("UPDATE todos SET done = 1 WHERE id = ?", (task_id,))
    if cur.rowcount == 0:
        click.echo(click.style(f"No task with ID {task_id}.", fg="red"))
    else:
        click.echo(click.style(f"Task #{task_id} marked done.", fg="green"))


@cli.command()
@click.argument("task_id", type=int)
def undone(task_id):
    """Mark a completed task as incomplete."""
    with get_db() as conn:
        cur = conn.execute("UPDATE todos SET done = 0 WHERE id = ?", (task_id,))
    if cur.rowcount == 0:
        click.echo(click.style(f"No task with ID {task_id}.", fg="red"))
    else:
        click.echo(click.style(f"Task #{task_id} marked incomplete.", fg="yellow"))


@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", default=None)
@click.option("--due", default=None)
@click.option("--priority", "-p", default=None, type=click.Choice(["low", "med", "high"]))
@click.option("--tags", default=None)
def edit(task_id, title, due, priority, tags):
    """Edit a task's fields."""
    fields, params = [], []
    if title:
        fields.append("title = ?"); params.append(title)
    if due:
        fields.append("due_date = ?"); params.append(due)
    if priority:
        fields.append("priority = ?"); params.append(priority)
    if tags is not None:
        fields.append("tags = ?"); params.append(tags)
    if not fields:
        click.echo("Nothing to update. Provide at least one option.")
        return
    params.append(task_id)
    with get_db() as conn:
        cur = conn.execute(f"UPDATE todos SET {', '.join(fields)} WHERE id = ?", params)
    if cur.rowcount == 0:
        click.echo(click.style(f"No task with ID {task_id}.", fg="red"))
    else:
        click.echo(click.style(f"Task #{task_id} updated.", fg="green"))


@cli.command()
@click.argument("task_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this task?")
def delete(task_id):
    """Delete a task permanently."""
    with get_db() as conn:
        cur = conn.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    if cur.rowcount == 0:
        click.echo(click.style(f"No task with ID {task_id}.", fg="red"))
    else:
        click.echo(click.style(f"Task #{task_id} deleted.", fg="green"))


@cli.command()
@click.option("--done", "done_only", is_flag=True, default=False, help="Only purge completed tasks")
@click.confirmation_option(prompt="Are you sure you want to clear tasks?")
def clear(done_only):
    """Remove tasks. Use --done to remove only completed tasks."""
    with get_db() as conn:
        if done_only:
            cur = conn.execute("DELETE FROM todos WHERE done = 1")
            click.echo(click.style(f"Cleared {cur.rowcount} completed task(s).", fg="green"))
        else:
            cur = conn.execute("DELETE FROM todos")
            click.echo(click.style(f"Cleared all {cur.rowcount} task(s).", fg="green"))


@cli.command()
@click.pass_context
def menu(ctx):
    """Interactive menu for all todo commands."""
    init_db()
    show_all = True
    while True:
        click.echo()
        ctx.invoke(list_tasks, show_all=show_all)
        show_all = False
        click.echo()
        click.echo(click.style("=== TODO MENU ===", bold=True))
        click.echo("  1. Add task")
        click.echo("  2. Mark task done")
        click.echo("  3. Mark task undone")
        click.echo("  4. Edit task")
        click.echo("  5. Delete task")
        click.echo("  6. List all tasks (including completed)")
        click.echo("  7. Clear completed tasks")
        click.echo("  8. Clear ALL tasks")
        click.echo("  q. Quit")
        click.echo()
        choice = click.prompt("Choose", default="q")

        if choice == "q":
            break
        elif choice == "1":
            title = click.prompt("Title")
            priority = click.prompt("Priority", default="med", type=click.Choice(["low", "med", "high"]))
            due = click.prompt("Due date (YYYY-MM-DD, or blank)", default="", show_default=False) or None
            tags = click.prompt("Tags (comma-separated, or blank)", default="", show_default=False) or None
            ctx.invoke(add, title=title, due=due, priority=priority, tags=tags)
        elif choice == "2":
            task_id = click.prompt("Task ID to mark done", type=int)
            ctx.invoke(done, task_id=task_id)
        elif choice == "3":
            task_id = click.prompt("Task ID to mark incomplete", type=int)
            ctx.invoke(undone, task_id=task_id)
        elif choice == "4":
            task_id = click.prompt("Task ID to edit", type=int)
            title = click.prompt("New title (blank to keep)", default="", show_default=False) or None
            priority = click.prompt("New priority (blank to keep)", default="", show_default=False) or None
            due = click.prompt("New due date (blank to keep)", default="", show_default=False) or None
            tags = click.prompt("New tags (blank to keep)", default="", show_default=False)
            ctx.invoke(edit, task_id=task_id, title=title, due=due,
                       priority=priority, tags=tags if tags != "" else None)
        elif choice == "5":
            task_id = click.prompt("Task ID to delete", type=int)
            if click.confirm(f"Delete task #{task_id}?"):
                with get_db() as conn:
                    cur = conn.execute("DELETE FROM todos WHERE id = ?", (task_id,))
                if cur.rowcount == 0:
                    click.echo(click.style(f"No task with ID {task_id}.", fg="red"))
                else:
                    click.echo(click.style(f"Task #{task_id} deleted.", fg="green"))
        elif choice == "6":
            ctx.invoke(list_tasks, show_all=True)
            click.pause()
            show_all = True
        elif choice == "7":
            if click.confirm("Clear all completed tasks?"):
                with get_db() as conn:
                    cur = conn.execute("DELETE FROM todos WHERE done = 1")
                click.echo(click.style(f"Cleared {cur.rowcount} completed task(s).", fg="green"))
        elif choice == "8":
            if click.confirm("Clear ALL tasks? This cannot be undone."):
                with get_db() as conn:
                    cur = conn.execute("DELETE FROM todos")
                click.echo(click.style(f"Cleared all {cur.rowcount} task(s).", fg="green"))
        else:
            click.echo(click.style("Invalid choice.", fg="red"))


if __name__ == "__main__":
    cli()
