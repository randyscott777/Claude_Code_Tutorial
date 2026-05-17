#!/usr/bin/env python3
"""Send the daily Claude Code Routine email via Gmail SMTP.

Requires the GMAIL_APP_PASSWORD environment variable to be set.
Generate one at: https://myaccount.google.com/apppasswords
"""

import os
import smtplib
import sys
from datetime import datetime
from email.mime.text import MIMEText

SENDER = "randyscott777@gmail.com"
RECIPIENT = "randyscott777@gmail.com"
SUBJECT = "Claude Code Routine"
BODY = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."


def send_email():
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        print("ERROR: GMAIL_APP_PASSWORD environment variable not set.", file=sys.stderr)
        print("Generate an app password at https://myaccount.google.com/apppasswords", file=sys.stderr)
        sys.exit(1)

    msg = MIMEText(BODY)
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, app_password)
        server.sendmail(SENDER, [RECIPIENT], msg.as_string())

    print(f"[{datetime.now().isoformat()}] Email sent to {RECIPIENT}")


if __name__ == "__main__":
    send_email()
