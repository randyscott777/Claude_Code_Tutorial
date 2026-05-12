"""
Daily routine email sender.
Reads Gmail app-password credentials from ~/.email_credentials and sends a
scheduled message to randyscott777@gmail.com.

Setup (one-time):
  1. Enable 2-Step Verification on your Google account.
  2. Create an App Password at https://myaccount.google.com/apppasswords
     (select Mail / Other, copy the 16-char password).
  3. Create ~/.email_credentials with the two lines shown in .email_credentials.example
"""

import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".email_credentials"

TO = "randyscott777@gmail.com"
SUBJECT = "Claude Code Routine"
BODY = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."


def load_credentials():
    if not CREDENTIALS_FILE.exists():
        sys.exit(
            f"Missing credentials file: {CREDENTIALS_FILE}\n"
            "Create it with:\n  GMAIL_USER=you@gmail.com\n  GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx"
        )
    creds = {}
    for line in CREDENTIALS_FILE.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            key, _, value = line.partition("=")
            creds[key.strip()] = value.strip()
    user = creds.get("GMAIL_USER")
    password = creds.get("GMAIL_APP_PASSWORD")
    if not user or not password:
        sys.exit("credentials file must contain GMAIL_USER and GMAIL_APP_PASSWORD")
    return user, password


def send_email():
    user, password = load_credentials()

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = TO
    msg["Subject"] = SUBJECT
    msg.set_content(BODY)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)

    print(f"Email sent to {TO}")


if __name__ == "__main__":
    send_email()
