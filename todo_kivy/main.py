from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from pathlib import Path
import db
import settings_store


class TodoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_path = Path(__file__).parent / "todos.db"

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = settings_store.get("theme")
        db.init_db(self.db_path)

        from screens.task_list import TaskListScreen
        from screens.task_form import TaskFormScreen
        from screens.categories import CategoriesScreen
        from screens.settings import SettingsScreen

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(TaskListScreen(name="task_list"))
        sm.add_widget(TaskFormScreen(name="task_form"))
        sm.add_widget(CategoriesScreen(name="categories"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

    def switch_theme(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )


if __name__ == "__main__":
    TodoApp().run()
