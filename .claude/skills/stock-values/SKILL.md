---
name: stock-values
description: Display current market value of the user's stock/fund holdings in a rich terminal table. Use when the user says "stock values", "portfolio value", "show my stocks", "show holdings", or invokes /stock-values.
---

# stock-values skill

## Steps

1. Run the script:
   ```
   python .claude/skills/stock-values/stock_values.py
   ```
2. Print the script's output verbatim — do NOT re-render or paraphrase the table.
3. If any ticker shows "No price found", ask the user to verify that symbol.

## Setup (first time only)
```
pip install yfinance rich
```
