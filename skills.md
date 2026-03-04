# Claude Code Skills

Skills are invokable via `/<skill-name>` syntax in Claude Code.

## Available Skills

### keybindings-help
Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings, or modify `~/.claude/keybindings.json`.

**Trigger examples:**
- "rebind ctrl+s"
- "add a chord shortcut"
- "change the submit key"
- "customize keybindings"

---

### simplify
Review changed code for reuse, quality, and efficiency, then fix any issues found.

---

### claude-developer-platform
Build apps with the Claude API or Anthropic SDK.

**Trigger when:** code imports `anthropic` / `@anthropic-ai/sdk` / `claude_agent_sdk`, or user asks to use Claude API, Anthropic SDKs, or Agent SDK.

**Do NOT trigger when:** code imports `openai` or other AI SDKs, general programming, or ML/data-science tasks.

For global, create the following in ~/.claude/skills/explain-code/SKILL.md
For project, create the following in .claude/skills/explain-code/SKILL.md

# LIVE EXAMPLE 1: to explain code (global)
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.

## Usage ##
Either:
claude "How does this code work"
or
claude /explain-code /users/randy/onedrive/visualstudiocode/Claude_Code_Tutorial/menu.py

# LIVE EXAMPLE 2: to create app to maintain a to do list using flask and SQLite3 raw commands
## Usage: clause /create-todo-list
