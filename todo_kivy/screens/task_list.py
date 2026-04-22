from pathlib import Path

from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

import db
import settings_store

Builder.load_file(str(Path(__file__).with_suffix(".kv")))

# (sort_by, sort_dir, display_label)
SORT_OPTIONS = [
    ("created_at", "DESC", "Date Created (Newest)"),
    ("created_at", "ASC",  "Date Created (Oldest)"),
    ("due_date",   "ASC",  "Due Date (Soonest)"),
    ("due_date",   "DESC", "Due Date (Latest)"),
    ("priority",   "DESC", "Priority (High → Low)"),
    ("priority",   "ASC",  "Priority (Low → High)"),
    ("title",      "ASC",  "Title (A → Z)"),
]

PRIORITY_COLORS = {
    "high": (0.9, 0.2, 0.2, 1),
    "med":  (0.95, 0.6, 0.1, 1),
    "low":  (0.2, 0.72, 0.32, 1),
}


class TaskItem(BoxLayout):
    todo_id       = NumericProperty(0)
    title         = StringProperty("")
    priority      = StringProperty("med")
    due_date_text = StringProperty("")
    category_text = StringProperty("")
    done          = BooleanProperty(False)

    def on_checkbox_active(self, _checkbox, value):
        # Guard against the initial binding firing during widget construction
        if bool(value) == self.done:
            return
        app = MDApp.get_running_app()
        db.toggle_done(self.todo_id, db_path=app.db_path)
        todo = db.get_todo(self.todo_id, db_path=app.db_path)
        if todo and todo["done"] and todo["recurrence"] != "none":
            db.advance_recurrence(self.todo_id, db_path=app.db_path)
        self._get_screen().refresh_list()

    def go_to_edit(self):
        screen = self._get_screen()
        if screen:
            screen.go_to_edit(self.todo_id)

    def _get_screen(self):
        widget = self.parent
        while widget:
            if isinstance(widget, TaskListScreen):
                return widget
            widget = widget.parent
        return None


class TaskListScreen(MDScreen):
    _search_text     = StringProperty("")
    _priority_filter = StringProperty("all")
    _done_filter     = StringProperty("all")
    _sort_by         = StringProperty("created_at")
    _sort_dir        = StringProperty("DESC")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sort_menu = None
        # Seed sort from persisted settings so the list opens correctly on first run
        s = settings_store.load_all()
        self._sort_by  = s["default_sort_by"]
        self._sort_dir = s["default_sort_dir"]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_enter(self):
        self.refresh_list()

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def on_search(self, text):
        self._search_text = text
        self.refresh_list()

    # ------------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------------

    def set_priority_filter(self, value):
        self._priority_filter = value
        self.refresh_list()

    def set_done_filter(self, value):
        self._done_filter = value
        self.refresh_list()

    # ------------------------------------------------------------------
    # Sort dropdown
    # ------------------------------------------------------------------

    def open_sort_menu(self, caller):
        if self._sort_menu is None:
            items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": label,
                    "on_release": (
                        lambda sb=sort_by, sd=sort_dir: self._apply_sort(sb, sd)
                    ),
                }
                for sort_by, sort_dir, label in SORT_OPTIONS
            ]
            self._sort_menu = MDDropdownMenu(
                caller=caller,
                items=items,
                width_mult=4,
            )
        else:
            self._sort_menu.caller = caller
        self._sort_menu.open()

    def _apply_sort(self, sort_by, sort_dir):
        self._sort_by = sort_by
        self._sort_dir = sort_dir
        if self._sort_menu:
            self._sort_menu.dismiss()
        self.refresh_list()

    # ------------------------------------------------------------------
    # List population
    # ------------------------------------------------------------------

    def refresh_list(self):
        task_list = self.ids.task_list
        task_list.clear_widgets()

        app      = MDApp.get_running_app()
        priority = None if self._priority_filter == "all" else self._priority_filter
        done     = None
        if self._done_filter == "active":
            done = False
        elif self._done_filter == "done":
            done = True

        cats  = {c["id"]: c["name"] for c in db.get_categories(db_path=app.db_path)}
        todos = db.get_todos(
            search=self._search_text or None,
            priority=priority,
            done=done,
            sort_by=self._sort_by,
            sort_dir=self._sort_dir,
            db_path=app.db_path,
        )

        for todo in todos:
            item = TaskItem(
                todo_id=todo["id"],
                title=todo["title"],
                priority=todo["priority"],
                due_date_text=todo["due_date"] or "",
                category_text=cats.get(todo["category_id"], "") if todo["category_id"] else "",
                done=bool(todo["done"]),
            )
            task_list.add_widget(item)

        self.ids.task_count.text = f"{len(todos)} task{'s' if len(todos) != 1 else ''}"

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def go_to_add(self):
        if "task_form" in [s.name for s in self.manager.screens]:
            form = self.manager.get_screen("task_form")
            form.load_todo(None)
            self.manager.current = "task_form"
        else:
            MDSnackbar(MDSnackbarText(text="Add/Edit screen coming in Phase 3")).open()

    def go_to_edit(self, todo_id):
        if "task_form" in [s.name for s in self.manager.screens]:
            form = self.manager.get_screen("task_form")
            form.load_todo(todo_id)
            self.manager.current = "task_form"
        else:
            MDSnackbar(MDSnackbarText(text="Add/Edit screen coming in Phase 3")).open()

    def go_to_categories(self):
        if "categories" in [s.name for s in self.manager.screens]:
            self.manager.current = "categories"
        else:
            MDSnackbar(MDSnackbarText(text="Category screen coming in Phase 4")).open()

    def go_to_settings(self):
        if "settings" in [s.name for s in self.manager.screens]:
            self.manager.current = "settings"
        else:
            MDSnackbar(MDSnackbarText(text="Settings screen coming in Phase 5")).open()
