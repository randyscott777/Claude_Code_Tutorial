#!/usr/bin/env python3
"""Daily 9 AM email sender for Claude Code Routine."""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("GMAIL_SENDER", "")
SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
RECIPIENT = "randyscott777@gmail.com"
SUBJECT = "Claude Code Routine"
BODY = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."


def send_email():
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        raise EnvironmentError(
            "Set GMAIL_SENDER and GMAIL_APP_PASSWORD environment variables before running."
        )

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT, msg.as_string())

    print(f"Email sent to {RECIPIENT}")


if __name__ == "__main__":
    send_email()
