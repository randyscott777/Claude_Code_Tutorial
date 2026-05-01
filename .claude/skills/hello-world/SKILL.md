---
name: hello-world
description: Greet a person by name with a fun ASCII banner. Demonstrates skill extra-prompt ($ARGUMENTS) and script execution. Usage: /hello-world <name>
---

# hello-world skill

The user invoked this skill with arguments: $ARGUMENTS

## Steps

1. Parse `$ARGUMENTS` to extract the name. If empty, use "World".
2. Run the helper script:
   ```
   python .claude/skills/hello-world/hello_world.py "<name>"
   ```
3. Display the script output verbatim inside a code block so the ASCII banner renders correctly.
4. Follow up with one sentence: what `$ARGUMENTS` contained and how the script used it.

## Purpose

This skill exists as a tutorial example. It shows three Claude Code skill features:

- **Extra prompt injection** — `$ARGUMENTS` is replaced at invocation time with whatever the user typed after `/hello-world`.
- **Script execution** — the skill delegates real work to a Python script rather than asking Claude to generate output from scratch.
- **Skill frontmatter** — the `name` and `description` fields wire the skill into Claude's trigger system.
