---
name: field-extractor
description: Extracts structured data from an invoice file. Use when the user mentions processing of invoices.
---

# Instructions
When a user provides an invoice file, use the following process:
1. Run the `extract_fields.py` script on the provided file path.
2. Review the JSON output from the script.
3. Summarize the findings for the user.

## Examples
User: "What's the total on this invoice?"
Action: Execute `python extract_fields.py dummy_invoice.pdf` and report the 'total' field.
