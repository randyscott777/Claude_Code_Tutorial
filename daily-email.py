import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = os.environ["EMAIL_SENDER"]
RECIPIENT = os.environ["EMAIL_RECIPIENT"]
PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

subject = "Claude Code Routine"
body = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg.attach(MIMEText(body, "plain"))

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())

print(f"Email sent to {RECIPIENT}")
