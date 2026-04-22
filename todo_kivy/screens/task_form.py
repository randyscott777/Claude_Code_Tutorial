from pathlib import Path

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

import db
import settings_store

Builder.load_file(str(Path(__file__).with_suffix(".kv")))

RECURRENCE_LABELS = {
    "none":    "Does not repeat",
    "daily":   "Daily",
    "weekly":  "Weekly",
    "monthly": "Monthly",
    "yearly":  "Yearly",
}


class TaskFormScreen(MDScreen):
    _priority         = StringProperty("med")
    _due_date         = StringProperty("")
    _category_name    = StringProperty("No category")
    _recurrence       = StringProperty("none")
    _recurrence_label = StringProperty("Does not repeat")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._todo_id      = None
        self._category_id  = None
        self._cat_menu     = None
        self._rec_menu     = None
        self._delete_dialog = None

    # ------------------------------------------------------------------
    # Property observers
    # ------------------------------------------------------------------

    def on__recurrence(self, _instance, value):
        self._recurrence_label = RECURRENCE_LABELS.get(value, value)

    # ------------------------------------------------------------------
    # Load / reset
    # ------------------------------------------------------------------

    def load_todo(self, todo_id):
        """Call this before navigating to the screen.
        Pass None for add mode, or an int todo id for edit mode."""
        self._todo_id = todo_id
        if todo_id is None:
            self._reset_form()
        else:
            todo = db.get_todo(todo_id, db_path=MDApp.get_running_app().db_path)
            if todo:
                self._populate_form(todo)

    def _reset_form(self):
        self.ids.title_field.text  = ""
        self.ids.notes_field.text  = ""
        self._priority             = settings_store.get("default_priority")
        self._due_date             = ""
        self._category_id          = None
        self._category_name        = "No category"
        self._recurrence           = "none"
        self.ids.toolbar.title     = "Add Task"
        self.ids.delete_btn.opacity  = 0
        self.ids.delete_btn.disabled = True

    def _populate_form(self, todo):
        self.ids.title_field.text  = todo["title"]
        self.ids.notes_field.text  = todo["notes"] or ""
        self._priority             = todo["priority"]
        self._due_date             = todo["due_date"] or ""
        self._category_id          = todo["category_id"]
        self._recurrence           = todo["recurrence"]
        self.ids.toolbar.title     = "Edit Task"
        self.ids.delete_btn.opacity  = 1
        self.ids.delete_btn.disabled = False

        if todo["category_id"]:
            cat = db.get_category(todo["category_id"], db_path=MDApp.get_running_app().db_path)
            self._category_name = cat["name"] if cat else "No category"
        else:
            self._category_name = "No category"

    # ------------------------------------------------------------------
    # Priority
    # ------------------------------------------------------------------

    def set_priority(self, value):
        self._priority = value

    # ------------------------------------------------------------------
    # Date picker
    # ------------------------------------------------------------------

    def show_date_picker(self):
        # Immediately unfocus so the field doesn't steal keyboard
        self.ids.due_date_field.focus = False
        picker = MDDatePicker()
        picker.bind(on_save=self._on_date_save)
        picker.open()

    def _on_date_save(self, _instance, value, _date_range):
        self._due_date = value.isoformat()

    def clear_date(self):
        self._due_date = ""

    # ------------------------------------------------------------------
    # Category menu
    # ------------------------------------------------------------------

    def open_category_menu(self, caller):
        app  = MDApp.get_running_app()
        cats = db.get_categories(db_path=app.db_path)

        items = [{
            "viewclass": "OneLineListItem",
            "text": "No category",
            "on_release": lambda: self._set_category(None, "No category"),
        }]
        for cat in cats:
            items.append({
                "viewclass": "OneLineListItem",
                "text": cat["name"],
                "on_release": (lambda c=cat: self._set_category(c["id"], c["name"])),
            })

        self._cat_menu = MDDropdownMenu(caller=caller, items=items, width_mult=3)
        self._cat_menu.open()

    def _set_category(self, cat_id, cat_name):
        self._category_id   = cat_id
        self._category_name = cat_name
        if self._cat_menu:
            self._cat_menu.dismiss()

    # ------------------------------------------------------------------
    # Recurrence menu
    # ------------------------------------------------------------------

    def open_recurrence_menu(self, caller):
        items = [
            {
                "viewclass": "OneLineListItem",
                "text": label,
                "on_release": (lambda v=value: self._set_recurrence(v)),
            }
            for value, label in RECURRENCE_LABELS.items()
        ]
        self._rec_menu = MDDropdownMenu(caller=caller, items=items, width_mult=3)
        self._rec_menu.open()

    def _set_recurrence(self, value):
        self._recurrence = value
        if self._rec_menu:
            self._rec_menu.dismiss()

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self):
        title = self.ids.title_field.text.strip()
        if not title:
            MDSnackbar(MDSnackbarText(text="Title is required")).open()
            return

        app   = MDApp.get_running_app()
        notes = self.ids.notes_field.text.strip() or None

        if self._todo_id is None:
            db.create_todo(
                title=title,
                due_date=self._due_date or None,
                priority=self._priority,
                category_id=self._category_id,
                notes=notes,
                recurrence=self._recurrence,
                db_path=app.db_path,
            )
        else:
            db.update_todo(
                self._todo_id,
                db_path=app.db_path,
                title=title,
                due_date=self._due_date or None,
                priority=self._priority,
                category_id=self._category_id,
                notes=notes,
                recurrence=self._recurrence,
            )

        self._go_back_and_refresh()

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def confirm_delete(self):
        def do_dismiss(*_):
            self._delete_dialog.dismiss()

        self._delete_dialog = MDDialog(
            text="Permanently delete this task?",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=do_dismiss),
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Custom",
                    text_color=(0.9, 0.2, 0.2, 1),
                    on_release=lambda _: self._do_delete(),
                ),
            ],
        )
        self._delete_dialog.open()

    def _do_delete(self):
        if self._delete_dialog:
            self._delete_dialog.dismiss()
        if self._todo_id is not None:
            db.delete_todo(self._todo_id, db_path=MDApp.get_running_app().db_path)
        self._go_back_and_refresh()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def go_back(self):
        self.manager.current = "task_list"

    def _go_back_and_refresh(self):
        self.manager.current = "task_list"
        self.manager.get_screen("task_list").refresh_list()
