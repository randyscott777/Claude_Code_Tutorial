import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL    = os.environ["SENDER_EMAIL"]
SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]
SMTP_SERVER     = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT       = int(os.environ.get("SMTP_PORT", "587"))

SUBJECT = "Claude Code Routine"
BODY    = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."

msg = MIMEMultipart()
msg["From"]    = SENDER_EMAIL
msg["To"]      = RECIPIENT_EMAIL
msg["Subject"] = SUBJECT
msg.attach(MIMEText(BODY, "plain"))

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

print(f"Email sent to {RECIPIENT_EMAIL}")
