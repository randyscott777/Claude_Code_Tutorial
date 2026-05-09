#!/bin/bash
# Daily 9 AM routine: sends email via Gmail SMTP.
# Requires GMAIL_SENDER and GMAIL_APP_PASSWORD in /home/user/.claude_routine_env
set -euo pipefail

ENV_FILE="/home/user/.claude_routine_env"
if [[ -f "$ENV_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$ENV_FILE"
fi

cd /home/user/Claude_Code_Tutorial
python3 send_daily_email.py 2>&1 | tee -a /home/user/Claude_Code_Tutorial/routine.log
