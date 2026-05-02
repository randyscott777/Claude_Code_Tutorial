# Invoked by .claude/settings.json statusLine command. Runs in the CLI (terminal),
# not in the web app.
import json, subprocess, sys

data = json.load(sys.stdin)
model = data.get('model', {}).get('display_name', 'Unknown')
cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
cwd = data.get('workspace', {}).get('current_dir') or data.get('cwd')

changes = ""
try:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=cwd, capture_output=True, text=True, timeout=2,
    )
    if result.returncode == 0:
        n = sum(1 for line in result.stdout.splitlines() if line.strip())
        changes = f" | {n} change{'s' if n != 1 else ''}"
except (FileNotFoundError, subprocess.TimeoutExpired):
    pass

print(f"[{model}] ${cost:.2f}{changes} - see /commit-status and update CLAUDE.md")
