#!/usr/bin/env bash
# Wrapper invoked by cron. Loads credentials from ~/.email_secrets then runs the mailer.
set -euo pipefail

SECRETS="${HOME}/.email_secrets"
if [ -f "$SECRETS" ]; then
    # shellcheck source=/dev/null
    source "$SECRETS"
fi

exec /usr/bin/python3 "$(dirname "$0")/send_daily_email.py"
