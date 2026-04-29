# Sub-Agents in Claude Code

Sub-agents are specialized Claude instances that the main agent can spawn to do a focused job and report back. Each one starts with **a fresh context window**, its own tool allowlist, and its own system prompt. They're how you parallelize work and protect the main conversation from drowning in noise.

## When a Sub-Agent Earns Its Cost

Spawning an agent is **not free** — it re-loads context from scratch, costs tokens, and adds latency. Use one when at least one of these is true:

- **Open-ended search** across many files (3+ rounds of grep/glob you'd otherwise do yourself)
- **Independent parallel work** — two unrelated investigations you can run at once
- **Context protection** — the task will produce a flood of output you don't want in the main thread (large file dumps, log scans)
- **Specialized expertise** — a security review, a design plan, a code review where a separate perspective matters

If the target is already known (a specific file path, a specific symbol), use `Read` / `Grep` directly. Don't spawn an agent to do one lookup.

## Built-in Agent Types

| Agent               | Use For |
|---------------------|---------|
| `general-purpose`  | Multi-step research, broad codebase questions |
| `Explore`           | Read-only code search, finding files/symbols/references |
| `Plan`              | Designing implementation strategy before coding |
| `security-reviewer` | Security audit (this project has one — see below) |
| `claude-code-guide` | Questions about Claude Code itself, the SDK, or the API |
| `statusline-setup`  | Configuring the status line in `settings.json` |

## Defining a Custom Project Agent

Agent definitions live in `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (global). They're plain markdown with YAML frontmatter:

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Frontmatter fields:

- **`name`** — the agent identifier (used in `subagent_type`)
- **`description`** — when this agent should be picked; Claude reads this to auto-route
- **`tools`** — allowlist of tools the agent may use; omit to inherit defaults
- **`model`** — `opus`, `sonnet`, or `haiku`; pick `haiku` for cheap/fast lookups, `opus` for hard reasoning

The body is the agent's system prompt — give it a role, a checklist, an output format.

## Three Ways to Invoke

1. **Natural language** — Claude auto-routes based on the agent's `description` field
   *"review django_todo for security vulnerabilities"*

2. **Explicit by name**
   *"use the security-reviewer agent to audit todo_flask/app.py"*

3. **`/agents` slash command** — list, manage, and edit agent definitions interactively

## Foreground vs Background

Agents can run in either mode:

- **Foreground (default)** — the main agent waits for the result before continuing. Use when you need the findings to inform the next step.
- **Background** — agent runs in parallel; you get notified on completion. Use when you have genuinely independent work to do meanwhile (e.g., kick off a long codebase audit while you keep editing).

In parallel: send **one message with multiple agent calls** to fan out — that's how you actually parallelize, not by chaining sequential calls.

## Briefing an Agent Well

A sub-agent has zero context from the current conversation. Treat it like a smart colleague who just walked into the room:

- State the **goal** and **why it matters**
- Include **file paths and line numbers** — don't make it re-discover them
- Say what's already been **ruled out**
- Ask for a **specific output shape** ("punch list under 200 words")

Terse one-line prompts produce shallow, generic work.

## Agents vs Skills vs Hooks

|           | Triggered by           | Runs as                          | Best for                               |
|-----------|------------------------|----------------------------------|----------------------------------------|
| **Agent** | The main agent decides | Separate Claude with own context | Open-ended sub-tasks needing reasoning |
| **Skill** | User types `/<name>`   | Inline in main conversation      | Reusable workflows you invoke yourself |
| **Hook** | Lifecycle event         | Shell command                    | Deterministic side effects (lint, notify, log) |

## Example: This Project's Reviewers

This repo ships two project-scoped review agents in `.claude/agents/`:

- **`security-reviewer`** — audits for injection, auth flaws, secrets, insecure data handling
- **`code-reviewer`** — catches bugs, broken contracts, edge-case mishandling, and convention violations on recently changed code

Try them:

```
use the security-reviewer agent to audit todo_flask/app.py
use the code-reviewer agent to review my last commit
```

Both run with read-only tools (`Read, Grep, Glob, Bash`) — no `Write` or `Edit` — so they can't accidentally modify code while reviewing. They stay in their own lanes: `code-reviewer` defers security issues to `security-reviewer` and skips style nits.

## Anti-Patterns

- **Spawning for a single file read.** Just use `Read`.
- **Daisy-chaining agents sequentially when they're independent.** Fan out instead.
- **"Based on your findings, fix the bug."** That pushes synthesis onto the agent. Read the findings yourself, then give the next agent (or yourself) a specific instruction.
- **Vague prompts.** "Look at the codebase and tell me what's wrong" gets you a vague answer. Constrain the question.
