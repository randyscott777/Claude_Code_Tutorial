# Claude Code — Tokens, Costs, and Usage

## What Are Tokens?

Claude reads and writes in **tokens**, not characters or words. A token is roughly 3–4 characters of English text.

| Example | Approx. Tokens |
|---------|---------------|
| "Hello, world!" | 4 |
| A typical line of code | 10–20 |
| A 1,000-word document | ~750 |
| A 500-line source file | ~2,000–4,000 |

Every API call consumes two kinds of tokens:

- **Input tokens** — everything sent to Claude (your prompt, file contents, conversation history, system prompt)
- **Output tokens** — everything Claude writes back (text, code, tool results)

---

## How Claude Code Spends Tokens

Each turn in a Claude Code session includes more than just your message:

| What Gets Sent | Why |
|---------------|-----|
| System prompt | Claude's built-in instructions and tool definitions |
| Conversation history | Prior messages are re-sent every turn (stateless API) |
| Tool results | File reads, search output, bash results |
| Your message | The actual prompt you typed |

> **Key Insight:** Long conversations accumulate fast. A session that reads many large files can consume tens of thousands of input tokens per turn because the full history is replayed each time.

---

## Pricing Tiers (as of early 2026)

Pricing is per **million tokens (MTok)**. Costs vary by model:

| Model | Input | Output |
|-------|-------|--------|
| Claude Haiku 4.5 | ~$0.80 / MTok | ~$4 / MTok |
| Claude Sonnet 4.6 | ~$3 / MTok | ~$15 / MTok |
| Claude Opus 4.6 | ~$15 / MTok | ~$75 / MTok |

> Prices change — always check the [Anthropic pricing page](https://www.anthropic.com/pricing) for current rates.

**Prompt caching** (when enabled) discounts repeated input at ~90% off, which significantly reduces costs for long, stable system prompts and file contents.

---

## Checking Your Balance and Usage

### Anthropic Console
Visit **console.anthropic.com** to see:
- Current credit balance
- Usage by day, model, and API key
- Billing history and invoices

### Claude Code Token Display
At the end of each session, Claude Code prints a usage summary:

```
Tokens:  12,450 input · 3,210 output
Cost:    ~$0.085
```

Use `/status` inside a session to see a running token count.

### Auto-Recharge
In the Console under **Billing**, you can enable auto-recharge so your balance tops up automatically when it drops below a threshold — avoiding interrupted sessions.

---

## Reducing Costs

| Strategy | Impact |
|----------|--------|
| Use `/clear` to reset conversation history | High — eliminates accumulated context |
| Use `-p` (print mode) for one-shot tasks | High — no persistent session overhead |
| Choose Haiku for simple tasks | High — ~4× cheaper than Sonnet |
| Use Opus only for complex planning | Medium — switch back to Sonnet to build |
| Avoid reading huge files unnecessarily | Medium — large reads inflate every subsequent turn |
| Enable prompt caching (API users) | High — up to 90% off repeated input |

---

## Context Window vs. Cost

Each model has a maximum **context window** (how many tokens fit in one call):

| Model | Context Window |
|-------|---------------|
| Haiku 4.5 | 200K tokens |
| Sonnet 4.6 | 200K tokens |
| Opus 4.6 | 200K tokens |

Hitting the context limit mid-session causes Claude to lose earlier messages. Claude Code handles this by automatically summarizing and compressing history, but compressed context is less precise. Starting a fresh session with `/clear` is often better than letting context overflow.

---

## Free Tier vs. Paid

- **Claude.ai** (web/app) offers a free tier with monthly message limits — no token billing.
- **Claude Code CLI** uses the **Anthropic API**, which is always pay-per-token — there is no free tier for API usage.
- API credits are purchased in the Console and do not expire.

> If you are new, start with a small credit purchase ($5–$20) to get a feel for your typical session costs before committing to larger amounts.
