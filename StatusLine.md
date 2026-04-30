# How to create a Custom Status Line
1. Python script (or bash or powershell):
import json, sys
data = json.load(sys.stdin)
model = data['model']['display_name']
pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)
filled = pct * 10 // 100
bar = '▓' * filled + '░' * (10 - filled)
print(f"[{model}] {bar} {pct}%")

2. Allow it to be executable:
chmod

3. Define in global settings.json:
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/StatusLine.py"
  }
}

# Note: this only works in Claude Code if using the bash terminal 