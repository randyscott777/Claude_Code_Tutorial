#!/usr/bin/env python3
"""Daily 9 AM email routine for the Claude Code Tutorial."""
import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

RECIPIENT = "randyscott777@gmail.com"
SUBJECT = "Claude Code Routine"
BODY = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."


def send_email():
    sender = os.environ.get("GMAIL_SENDER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        print("ERROR: Set GMAIL_SENDER and GMAIL_APP_PASSWORD environment variables.", file=sys.stderr)
        print("  export GMAIL_SENDER=your@gmail.com", file=sys.stderr)
        print("  export GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Gmail App Password", file=sys.stderr)
        sys.exit(1)

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = RECIPIENT
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, RECIPIENT, msg.as_string())

    print(f"Email sent to {RECIPIENT}: {SUBJECT}")


if __name__ == "__main__":
    send_email()
