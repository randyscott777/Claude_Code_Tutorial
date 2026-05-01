---
name: log
description: Greets the user by name with today's date and logs the message to the database. Use when the user says "log" in the prompt or uses the /log command.
---

# Log Skill

This is a minimal sample skill that demonstrates the structure of a Claude Code skill.

## Instructions

When invoked, do the following:

1. Determine the user's first name (default to "Randy" from `randyscott777@gmail.com` if no other name is known).
2. Run `python scripts/log_message.py <message>` via Bash from this skill's directory. The script logs the message to `scripts/messages.db` and prints the message plus a running count.
3. Print the script's output verbatim.
4. End with a one-line offer to help with something specific (e.g., "Enter 'show history' to see past greetings.").

If the user asks to see past greetings, run `python scripts/log_greeting.py --history <name>` instead and print its output.

## Example output

```
Thank you for logging your message.
(That's entry #1 for you in the log.)
See 'Show History' to view past entries.
```

## Notes for skill authors

- The `name` field must match the folder name (`log`).
- The `description` field is what Claude matches against user prompts to decide when to invoke the skill — be specific about trigger phrases.
- Everything below the frontmatter is the instruction body Claude reads when the skill fires.
