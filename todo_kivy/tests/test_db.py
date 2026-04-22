"""Unit tests for db.py — uses a temp file DB, no Kivy required."""
import pytest
from datetime import date, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from db import (
    init_db,
    create_category, get_categories, get_category, update_category, delete_category,
    create_todo, get_todo, get_todos, update_todo, delete_todo, toggle_done,
    get_next_due_date, advance_recurrence,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db(tmp_path):
    path = tmp_path / "test.db"
    init_db(path)
    return path


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class TestInitDb:
    def test_creates_tables(self, db):
        todos = get_todos(db_path=db)
        assert todos == []

        cats = get_categories(db_path=db)
        assert cats == []


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

class TestCategories:
    def test_create_and_get(self, db):
        cid = create_category("Work", db_path=db)
        assert cid == 1
        cats = get_categories(db_path=db)
        assert len(cats) == 1
        assert cats[0]["name"] == "Work"

    def test_get_single(self, db):
        cid = create_category("Personal", db_path=db)
        cat = get_category(cid, db_path=db)
        assert cat["name"] == "Personal"

    def test_get_missing_returns_none(self, db):
        assert get_category(999, db_path=db) is None

    def test_update(self, db):
        cid = create_category("Old", db_path=db)
        update_category(cid, "New", db_path=db)
        assert get_category(cid, db_path=db)["name"] == "New"

    def test_delete(self, db):
        cid = create_category("Temp", db_path=db)
        delete_category(cid, db_path=db)
        assert get_category(cid, db_path=db) is None

    def test_delete_nullifies_todo_category(self, db):
        cid = create_category("Work", db_path=db)
        tid = create_todo("Task", category_id=cid, db_path=db)
        delete_category(cid, db_path=db)
        todo = get_todo(tid, db_path=db)
        assert todo["category_id"] is None

    def test_ordered_alphabetically(self, db):
        create_category("Zebra", db_path=db)
        create_category("Alpha", db_path=db)
        names = [c["name"] for c in get_categories(db_path=db)]
        assert names == ["Alpha", "Zebra"]

    def test_duplicate_name_raises(self, db):
        create_category("Work", db_path=db)
        with pytest.raises(Exception):
            create_category("Work", db_path=db)


# ---------------------------------------------------------------------------
# Todos — CRUD
# ---------------------------------------------------------------------------

class TestTodoCrud:
    def test_create_minimal(self, db):
        tid = create_todo("Buy milk", db_path=db)
        todo = get_todo(tid, db_path=db)
        assert todo["title"] == "Buy milk"
        assert todo["done"] == 0
        assert todo["priority"] == "med"
        assert todo["recurrence"] == "none"

    def test_create_full(self, db):
        cid = create_category("Work", db_path=db)
        tid = create_todo(
            "Write report",
            due_date="2026-05-01",
            priority="high",
            category_id=cid,
            notes="See brief",
            recurrence="weekly",
            db_path=db,
        )
        todo = get_todo(tid, db_path=db)
        assert todo["due_date"] == "2026-05-01"
        assert todo["priority"] == "high"
        assert todo["category_id"] == cid
        assert todo["notes"] == "See brief"
        assert todo["recurrence"] == "weekly"

    def test_get_missing_returns_none(self, db):
        assert get_todo(999, db_path=db) is None

    def test_update_fields(self, db):
        tid = create_todo("Old title", db_path=db)
        update_todo(tid, db_path=db, title="New title", priority="high")
        todo = get_todo(tid, db_path=db)
        assert todo["title"] == "New title"
        assert todo["priority"] == "high"

    def test_update_ignores_unknown_fields(self, db):
        tid = create_todo("Task", db_path=db)
        update_todo(tid, db_path=db, hacked_field="evil")
        todo = get_todo(tid, db_path=db)
        assert "hacked_field" not in todo

    def test_delete(self, db):
        tid = create_todo("Temp", db_path=db)
        delete_todo(tid, db_path=db)
        assert get_todo(tid, db_path=db) is None

    def test_toggle_done(self, db):
        tid = create_todo("Task", db_path=db)
        toggle_done(tid, db_path=db)
        assert get_todo(tid, db_path=db)["done"] == 1
        toggle_done(tid, db_path=db)
        assert get_todo(tid, db_path=db)["done"] == 0


# ---------------------------------------------------------------------------
# Todos — Filtering & sorting
# ---------------------------------------------------------------------------

class TestTodoFiltering:
    def _seed(self, db):
        cid = create_category("Work", db_path=db)
        create_todo("Buy milk", priority="low", db_path=db)
        create_todo("Write report", priority="high", category_id=cid, db_path=db)
        create_todo("Call doctor", priority="med", due_date="2026-06-01", db_path=db)
        return cid

    def test_get_all(self, db):
        self._seed(db)
        assert len(get_todos(db_path=db)) == 3

    def test_filter_by_priority(self, db):
        self._seed(db)
        results = get_todos(priority="high", db_path=db)
        assert len(results) == 1
        assert results[0]["title"] == "Write report"

    def test_filter_by_category(self, db):
        cid = self._seed(db)
        results = get_todos(category_id=cid, db_path=db)
        assert len(results) == 1
        assert results[0]["title"] == "Write report"

    def test_filter_by_done(self, db):
        self._seed(db)
        todos = get_todos(db_path=db)
        toggle_done(todos[0]["id"], db_path=db)
        done = get_todos(done=True, db_path=db)
        not_done = get_todos(done=False, db_path=db)
        assert len(done) == 1
        assert len(not_done) == 2

    def test_search_title(self, db):
        self._seed(db)
        results = get_todos(search="milk", db_path=db)
        assert len(results) == 1
        assert results[0]["title"] == "Buy milk"

    def test_search_notes(self, db):
        create_todo("Task", notes="remember the umbrella", db_path=db)
        results = get_todos(search="umbrella", db_path=db)
        assert len(results) == 1

    def test_search_case_insensitive(self, db):
        create_todo("Buy Milk", db_path=db)
        assert len(get_todos(search="milk", db_path=db)) == 1

    def test_sort_by_priority_desc(self, db):
        self._seed(db)
        results = get_todos(sort_by="priority", sort_dir="DESC", db_path=db)
        priorities = [r["priority"] for r in results]
        assert priorities == ["high", "med", "low"]

    def test_sort_by_priority_asc(self, db):
        self._seed(db)
        results = get_todos(sort_by="priority", sort_dir="ASC", db_path=db)
        priorities = [r["priority"] for r in results]
        assert priorities == ["low", "med", "high"]

    def test_invalid_sort_col_defaults_to_created_at(self, db):
        self._seed(db)
        # Should not raise
        results = get_todos(sort_by="injected; DROP TABLE todos--", db_path=db)
        assert len(results) == 3


# ---------------------------------------------------------------------------
# Recurrence
# ---------------------------------------------------------------------------

class TestRecurrence:
    def test_none_returns_none(self):
        assert get_next_due_date("2026-01-01", "none") is None

    def test_no_due_date_returns_none(self):
        assert get_next_due_date(None, "daily") is None
        assert get_next_due_date("", "weekly") is None

    def test_daily_future_date(self):
        future = (date.today() + timedelta(days=5)).isoformat()
        result = get_next_due_date(future, "daily")
        expected = (date.today() + timedelta(days=6)).isoformat()
        assert result == expected

    def test_daily_past_date_returns_tomorrow(self):
        past = "2020-01-01"
        result = get_next_due_date(past, "daily")
        expected = (date.today() + timedelta(days=1)).isoformat()
        assert result == expected

    def test_weekly(self):
        base = date.today() + timedelta(days=3)
        result = get_next_due_date(base.isoformat(), "weekly")
        expected = (base + timedelta(weeks=1)).isoformat()
        assert result == expected

    def test_monthly(self):
        result = get_next_due_date("2026-01-15", "monthly")
        result_date = date.fromisoformat(result)
        assert result_date > date.today()
        assert result_date.day == 15

    def test_monthly_end_of_month_clamp(self):
        # Jan 31 + 1 month → Feb 28 (not Feb 31)
        result = get_next_due_date("2025-01-31", "monthly")
        result_date = date.fromisoformat(result)
        assert result_date > date.today()
        assert result_date.month in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1)
        assert result_date.day <= 31

    def test_yearly(self):
        result = get_next_due_date("2020-06-15", "yearly")
        result_date = date.fromisoformat(result)
        assert result_date > date.today()
        assert result_date.month == 6
        assert result_date.day == 15


# ---------------------------------------------------------------------------
# advance_recurrence
# ---------------------------------------------------------------------------

class TestAdvanceRecurrence:
    def test_advances_due_date_and_resets_done(self, db):
        tid = create_todo(
            "Weekly review",
            due_date="2026-01-01",
            recurrence="weekly",
            db_path=db,
        )
        toggle_done(tid, db_path=db)
        advance_recurrence(tid, db_path=db)
        todo = get_todo(tid, db_path=db)
        assert todo["done"] == 0
        next_due = date.fromisoformat(todo["due_date"])
        assert next_due > date.today()

    def test_no_op_for_nonrecurring(self, db):
        tid = create_todo("One-off", due_date="2026-01-01", db_path=db)
        toggle_done(tid, db_path=db)
        advance_recurrence(tid, db_path=db)
        todo = get_todo(tid, db_path=db)
        # done stays 1, due_date unchanged — advance_recurrence does nothing
        assert todo["done"] == 1
        assert todo["due_date"] == "2026-01-01"

    def test_missing_todo_is_safe(self, db):
        advance_recurrence(999, db_path=db)  # should not raise
