"""Start the todos_list Flask app in the background and open it in the browser."""

import subprocess
import sys
import time
import webbrowser
import urllib.request
from pathlib import Path

APP_PATH = Path(__file__).parents[3] / "todos_list" / "app.py"
URL = "http://127.0.0.1:5000"


def is_running():
    try:
        urllib.request.urlopen(URL, timeout=1)
        return True
    except Exception:
        return False


if not is_running():
    subprocess.Popen(
        [sys.executable, str(APP_PATH)],
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
    )
    for _ in range(10):
        time.sleep(0.5)
        if is_running():
            break

webbrowser.open(URL)
print(f"todos_list is running at {URL} — browser opened.")
