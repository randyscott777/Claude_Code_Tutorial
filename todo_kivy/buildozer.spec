[app]

# App metadata
title           = My Tasks
package.name    = mytasks
package.domain  = org.example
version         = 1.0.0

# Source
source.dir          = .
source.include_exts = py,kv,json,atlas,png,jpg
source.exclude_dirs = tests,bin,.buildozer,__pycache__,.pytest_cache

# Entry point — Kivy's standard Android activity
#android.entrypoint = org.kivy.android.PythonActivity

# Requirements — pinned versions for reproducible builds
# materialyoucolor is a KivyMD 1.2.0 transitive dependency (pure Python)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,materialyoucolor==0.1.9,sqlite3

# Orientation
orientation = portrait
fullscreen  = 0

# Android SDK/NDK
android.api    = 33
android.minapi = 21
android.ndk    = 25b
android.arch   = arm64-v8a

# No permissions needed (no notifications, no external storage)
android.permissions =

# Allow the APK to be backed up by Android
android.allow_backup = True

# App icon — replace with your own 512×512 PNG
# icon.filename = %(source.dir)s/icon.png

# Presplash (loading screen) — optional
# presplash.filename = %(source.dir)s/presplash.png
# presplash.color    = #FFFFFF

[buildozer]
log_level   = 2
warn_on_root = 1
