# Invoked by .claude/settings.json statusLine command. Runs in the CLI (terminal),
# not in the web app.
import json, sys

data = json.load(sys.stdin)
model = data.get('model', {}).get('display_name', 'Unknown')
cost = data.get('cost', {}).get('total_cost_usd', 0) or 0

print(f"[{model}] ${cost:.2f}")
