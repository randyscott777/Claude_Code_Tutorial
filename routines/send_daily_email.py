#!/usr/bin/env python3
"""Daily 9 AM routine: send Claude Code Routine email via Gmail SMTP."""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from datetime import datetime

RECIPIENT = "randyscott777@gmail.com"
SUBJECT = "Claude Code Routine"
BODY = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

if not GMAIL_USER or not GMAIL_APP_PASSWORD:
    print("Error: Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.", file=sys.stderr)
    sys.exit(1)

msg = MIMEText(BODY)
msg["Subject"] = SUBJECT
msg["From"] = GMAIL_USER
msg["To"] = RECIPIENT

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_USER, [RECIPIENT], msg.as_string())

print(f"[{datetime.now().isoformat()}] Email sent to {RECIPIENT}")
