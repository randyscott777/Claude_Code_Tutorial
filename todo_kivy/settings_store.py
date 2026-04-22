"""Thin wrapper around Kivy's JsonStore for app settings persistence."""
from pathlib import Path

from kivy.storage.jsonstore import JsonStore

_STORE_PATH = Path(__file__).parent / "app_settings.json"

DEFAULTS = {
    "theme":            "Light",
    "default_sort_by":  "created_at",
    "default_sort_dir": "DESC",
    "default_priority": "med",
}


def _store() -> JsonStore:
    return JsonStore(str(_STORE_PATH))


def get(key: str):
    store = _store()
    return store.get(key)["value"] if store.exists(key) else DEFAULTS[key]


def put(key: str, value) -> None:
    _store().put(key, value=value)


def load_all() -> dict:
    return {k: get(k) for k in DEFAULTS}
