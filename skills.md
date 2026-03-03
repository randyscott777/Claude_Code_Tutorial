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
