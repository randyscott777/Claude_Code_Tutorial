#!/usr/bin/env python3
"""
Daily email sender — run via cron at 9:00 AM.

Requires the GMAIL_APP_PASSWORD environment variable to be set.
Generate one at: myaccount.google.com > Security > App passwords
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = "randyscott777@gmail.com"
RECIPIENT = "randyscott777@gmail.com"
SUBJECT = "Claude Code Routine"
BODY = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def send_email():
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        print("Error: GMAIL_APP_PASSWORD environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain"))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SENDER, app_password)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())

    print(f"Email sent to {RECIPIENT}")


if __name__ == "__main__":
    send_email()
