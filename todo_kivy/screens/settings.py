from pathlib import Path

from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

import settings_store

Builder.load_file(str(Path(__file__).with_suffix(".kv")))

# Must match SORT_OPTIONS in task_list.py
_SORT_OPTIONS = [
    ("created_at", "DESC", "Date Created (Newest)"),
    ("created_at", "ASC",  "Date Created (Oldest)"),
    ("due_date",   "ASC",  "Due Date (Soonest)"),
    ("due_date",   "DESC", "Due Date (Latest)"),
    ("priority",   "DESC", "Priority (High → Low)"),
    ("priority",   "ASC",  "Priority (Low → High)"),
    ("title",      "ASC",  "Title (A → Z)"),
]

_SORT_LABEL = {(sb, sd): label for sb, sd, label in _SORT_OPTIONS}


class SettingsScreen(MDScreen):
    _dark_mode        = BooleanProperty(False)
    _default_priority = StringProperty("med")
    _sort_label       = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sort_menu = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_enter(self):
        s = settings_store.load_all()
        self._dark_mode        = s["theme"] == "Dark"
        self._default_priority = s["default_priority"]
        self._sort_label       = _SORT_LABEL.get(
            (s["default_sort_by"], s["default_sort_dir"]),
            "Date Created (Newest)",
        )

    # ------------------------------------------------------------------
    # Theme
    # ------------------------------------------------------------------

    def toggle_theme(self, active):
        theme = "Dark" if active else "Light"
        settings_store.put("theme", theme)
        MDApp.get_running_app().theme_cls.theme_style = theme

    # ------------------------------------------------------------------
    # Default priority
    # ------------------------------------------------------------------

    def set_default_priority(self, value):
        self._default_priority = value
        settings_store.put("default_priority", value)

    # ------------------------------------------------------------------
    # Default sort
    # ------------------------------------------------------------------

    def open_sort_menu(self, caller):
        items = [
            {
                "viewclass": "OneLineListItem",
                "text": label,
                "on_release": (lambda sb=sort_by, sd=sort_dir: self._apply_sort(sb, sd)),
            }
            for sort_by, sort_dir, label in _SORT_OPTIONS
        ]
        self._sort_menu = MDDropdownMenu(caller=caller, items=items, width_mult=4)
        self._sort_menu.open()

    def _apply_sort(self, sort_by, sort_dir):
        settings_store.put("default_sort_by", sort_by)
        settings_store.put("default_sort_dir", sort_dir)
        self._sort_label = _SORT_LABEL.get((sort_by, sort_dir), "")
        if self._sort_menu:
            self._sort_menu.dismiss()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def go_back(self):
        self.manager.current = "task_list"
