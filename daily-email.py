import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = os.environ["GMAIL_SENDER"]
APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT = "randyscott777@gmail.com"
SUBJECT = "Claude Code Routine"
BODY = "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."

msg = MIMEMultipart()
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg["Subject"] = SUBJECT
msg.attach(MIMEText(BODY, "plain"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER, APP_PASSWORD)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())

print(f"Email sent to {RECIPIENT}")
