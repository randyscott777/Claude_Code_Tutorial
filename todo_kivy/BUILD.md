# Building for Android

## Prerequisites

- Windows 11 with WSL2 enabled
- Ubuntu 22.04 LTS installed from the Microsoft Store
- An Android phone with Developer Options enabled

---

## Step 1 — Enable WSL2 and install Ubuntu

Open PowerShell as Administrator and run:

```powershell
wsl --install -d Ubuntu-22.04
```

Reboot if prompted. After reboot, Ubuntu will finish setup and ask for a Unix username/password.

---

## Step 2 — Install build dependencies inside Ubuntu

Open Ubuntu from the Start menu, then run:

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
    git zip unzip python3-pip \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev \
    openjdk-17-jdk

pip3 install --user buildozer cython==0.29.36
```

Add the local pip bin to your PATH (add this to `~/.bashrc` too):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Step 3 — Copy the project into WSL2

Building directly from `/mnt/c/...` is slow and causes permission errors.
Copy the project to your WSL2 home directory instead:

```bash
cp -r /mnt/c/Users/randy/OneDrive/VisualStudioCode/Claude_Code_Tutorial/todo_kivy ~/todo_kivy
cd ~/todo_kivy
```

For subsequent code changes, sync only changed files:

```bash
rsync -av --exclude='.buildozer' --exclude='__pycache__' \
    /mnt/c/Users/randy/OneDrive/VisualStudioCode/Claude_Code_Tutorial/todo_kivy/ \
    ~/todo_kivy/
```

---

## Step 4 — First build (downloads Android SDK/NDK automatically)

```bash
cd ~/todo_kivy
buildozer android debug
```

The **first build takes 20–40 minutes** — Buildozer downloads the Android SDK, NDK (~1 GB),
and compiles all dependencies. Subsequent builds are much faster (~2–5 min).

The APK will be output to:

```
~/todo_kivy/bin/mytasks-1.0.0-arm64-v8a-debug.apk
```

---

## Step 5 — Copy APK back to Windows

```bash
cp ~/todo_kivy/bin/*.apk \
    /mnt/c/Users/randy/OneDrive/VisualStudioCode/Claude_Code_Tutorial/todo_kivy/bin/
```

---

## Step 6 — Install on Android device

### Enable Developer Options on your phone
1. Go to **Settings → About phone**
2. Tap **Build number** 7 times until "You are now a developer" appears
3. Go to **Settings → Developer options** → enable **USB debugging**

### Install via ADB (recommended)
Connect your phone via USB, then in Ubuntu:

```bash
sudo apt install -y adb
adb devices          # confirm your device is listed
adb install ~/todo_kivy/bin/mytasks-1.0.0-arm64-v8a-debug.apk
```

### Install via file transfer (alternative)
Copy the APK to your phone, open it from the Files app, and tap Install.
You may need to allow installs from unknown sources in Settings.

---

## Iterative development workflow

After making code changes on Windows:

```bash
# 1. Sync changes into WSL2
rsync -av --exclude='.buildozer' --exclude='__pycache__' \
    /mnt/c/Users/randy/OneDrive/VisualStudioCode/Claude_Code_Tutorial/todo_kivy/ \
    ~/todo_kivy/

# 2. Rebuild
cd ~/todo_kivy && buildozer android debug

# 3. Reinstall (the -r flag replaces the existing installation)
adb install -r ~/todo_kivy/bin/mytasks-1.0.0-arm64-v8a-debug.apk
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `buildozer: command not found` | Run `export PATH="$HOME/.local/bin:$PATH"` and add it to `~/.bashrc` |
| `SDK not found` | Delete `~/.buildozer` and retry — Buildozer will re-download |
| `JAVA_HOME not set` | Run `export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64` |
| Build fails on `materialyoucolor` | Pin to `materialyoucolor==0.1.9` in `buildozer.spec` requirements (already set) |
| KivyMD import error at runtime | Ensure `kivymd==1.2.0` is in requirements and `.kv` files are in `source.include_exts` |
| App crashes on launch | Run `adb logcat \| grep python` to see the Python traceback |
| White/blank screen | Usually a missing `.kv` file — check `source.include_exts` includes `kv` |

---

## Release build (when ready to distribute)

```bash
buildozer android release
```

You will need a keystore to sign the APK. See the
[Buildozer docs](https://buildozer.readthedocs.io) for signing instructions.
