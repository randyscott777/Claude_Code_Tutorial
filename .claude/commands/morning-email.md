Send the daily Claude Code Routine morning email.

First, try to send via the Python script (actual SMTP delivery):
```
python scripts/send_morning_email.py
```

If that succeeds, report the confirmation message and stop.

If it fails because GMAIL_APP_PASSWORD is not set, fall back to creating a Gmail draft using the mcp__Gmail__create_draft tool with these exact values:
- to: ["randyscott777@gmail.com"]
- subject: "Claude Code Routine"
- body: "This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo."

Report whether the email was sent (SMTP) or saved as a draft (MCP fallback), and include the timestamp.
