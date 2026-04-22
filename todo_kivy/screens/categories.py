from pathlib import Path

from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.textfield import MDTextField

import db

Builder.load_file(str(Path(__file__).with_suffix(".kv")))


# ---------------------------------------------------------------------------
# Dialog content widget — reused for both add and edit
# ---------------------------------------------------------------------------

class CategoryInputContent(MDBoxLayout):
    """A single MDTextField used as dialog content."""
    pass


# ---------------------------------------------------------------------------
# Individual category row
# ---------------------------------------------------------------------------

class CategoryItem(BoxLayout):
    category_id = NumericProperty(0)
    name        = StringProperty("")
    task_count  = NumericProperty(0)

    def edit(self):
        self._get_screen().open_edit_dialog(self.category_id, self.name)

    def delete(self):
        self._get_screen().confirm_delete(self.category_id, self.name, self.task_count)

    def _get_screen(self):
        widget = self.parent
        while widget:
            if isinstance(widget, CategoriesScreen):
                return widget
            widget = widget.parent
        return None


# ---------------------------------------------------------------------------
# Categories screen
# ---------------------------------------------------------------------------

class CategoriesScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dialog         = None
        self._editing_id     = None   # None = add mode, int = edit mode
        self._delete_dialog  = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_enter(self):
        self.refresh_list()

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------

    def refresh_list(self):
        cat_list = self.ids.cat_list
        cat_list.clear_widgets()

        app    = MDApp.get_running_app()
        cats   = db.get_categories(db_path=app.db_path)
        counts = db.get_category_task_counts(db_path=app.db_path)

        self.ids.empty_label.opacity = 1 if not cats else 0

        for cat in cats:
            item = CategoryItem(
                category_id=cat["id"],
                name=cat["name"],
                task_count=counts.get(cat["id"], 0),
            )
            cat_list.add_widget(item)

    # ------------------------------------------------------------------
    # Add dialog
    # ------------------------------------------------------------------

    def open_add_dialog(self):
        self._editing_id = None
        self._open_dialog(title="New Category", prefill="")

    # ------------------------------------------------------------------
    # Edit dialog
    # ------------------------------------------------------------------

    def open_edit_dialog(self, category_id, current_name):
        self._editing_id = category_id
        self._open_dialog(title="Rename Category", prefill=current_name)

    # ------------------------------------------------------------------
    # Shared dialog builder
    # ------------------------------------------------------------------

    def _open_dialog(self, title, prefill):
        content = CategoryInputContent()
        content.ids.name_field.text = prefill

        self._dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda _: self._dialog.dismiss(),
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=lambda _: self._save_category(),
                ),
            ],
        )
        self._dialog.open()

    def _save_category(self):
        name = self._dialog.content_cls.ids.name_field.text.strip()
        if not name:
            MDSnackbar(MDSnackbarText(text="Category name cannot be empty")).open()
            return

        app = MDApp.get_running_app()
        try:
            if self._editing_id is None:
                db.create_category(name, db_path=app.db_path)
            else:
                db.update_category(self._editing_id, name, db_path=app.db_path)
        except Exception:
            MDSnackbar(MDSnackbarText(text=f'"{name}" already exists')).open()
            return

        self._dialog.dismiss()
        self.refresh_list()

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def confirm_delete(self, category_id, name, task_count):
        if task_count > 0:
            body = (
                f'Delete "{name}"?\n'
                f'{task_count} task{"s" if task_count != 1 else ""} '
                f'will become uncategorized.'
            )
        else:
            body = f'Delete "{name}"?'

        def do_dismiss(*_):
            self._delete_dialog.dismiss()

        self._delete_dialog = MDDialog(
            text=body,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=do_dismiss),
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Custom",
                    text_color=(0.9, 0.2, 0.2, 1),
                    on_release=lambda _: self._do_delete(category_id),
                ),
            ],
        )
        self._delete_dialog.open()

    def _do_delete(self, category_id):
        if self._delete_dialog:
            self._delete_dialog.dismiss()
        db.delete_category(category_id, db_path=MDApp.get_running_app().db_path)
        self.refresh_list()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def go_back(self):
        self.manager.current = "task_list"
        self.manager.get_screen("task_list").refresh_list()
