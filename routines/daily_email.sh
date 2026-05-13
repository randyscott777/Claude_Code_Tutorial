#!/bin/bash
# Daily 9 AM routine: send Claude Code Routine email.
# Requires GMAIL_USER and GMAIL_APP_PASSWORD to be set.
# For a Gmail App Password: https://myaccount.google.com/apppasswords

export GMAIL_USER="randyscott777@gmail.com"
# Set GMAIL_APP_PASSWORD in /etc/environment or ~/.profile (do NOT commit it here)
# export GMAIL_APP_PASSWORD="your-16-char-app-password"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$SCRIPT_DIR/daily_email.log"

python3 "$SCRIPT_DIR/send_daily_email.py" >> "$LOG" 2>&1
