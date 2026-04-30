#!/usr/bin/env python3
"""Daily email sender for Claude Code Routine — run via cron at 9:00 AM."""

import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

ENV_FILE = Path(__file__).parent / ".email_credentials"


def load_credentials():
    creds = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                creds[key.strip()] = value.strip()
    return creds


def send_email():
    creds = load_credentials()
    sender = creds.get("GMAIL_ADDRESS") or os.environ.get("GMAIL_ADDRESS")
    password = creds.get("GMAIL_APP_PASSWORD") or os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not password:
        print(
            "ERROR: Missing credentials. Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD "
            f"in {ENV_FILE}",
            file=sys.stderr,
        )
        sys.exit(1)

    recipient = "randyscott777@gmail.com"
    subject = "Claude Code Routine"
    body = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Email sent to {recipient}")


if __name__ == "__main__":
    send_email()
