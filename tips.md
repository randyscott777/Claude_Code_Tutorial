After extensive use, certain patterns consistently produce better results with Claude Code. These practices will help you get dramatically more value from every session.

## 1. Set Up CLAUDE.md Before Starting

Create a CLAUDE.md file (via /init) before writing a single line of code. This one-time investment pays dividends on every future session — Claude arrives knowing your stack, conventions, and rules.

## 2. Be Specific, Not Vague

**Too vague**
```
"fix the bug"
```

✓ **Specific and contextual**
```
"The login form submits but the user stays on the page. Check the onSubmit handler in LoginForm.tsx and fix the redirect after successful authentication."
```

## 3. Use /plan for Big Changes

Before large refactors or architectural changes, use `/plan` to review Claude's approach without any code being modified:

```
> /plan refactor authentication to use JWTs
# Claude explains its full approach
# Review it, ask questions, adjust the plan
# Then approve and Claude executes
```

## 4. Reference Files and Functions Directly

```
# Weak
"improve error handling"

# Strong
"In the authenticate() function in src/middleware/auth.js,
catch JWT expiry errors specifically and return a 401
with the message: 'Session expired, please log in again'"
```

## 5. Always Verify with Tests

End every significant change request with a verification step:

```
> Add the new feature, then run npm test to verify nothing broke
```

## 6. Pipe Inputs for Faster Debugging

```bash
# Share errors instantly — no copy-paste
npm test 2>&1 | claude "why are these tests failing?"

# Auto-generate PR descriptions from diffs
git diff main | claude "write a PR description for these changes"
```

## 7. Use /compact for Long Sessions

Run `/compact` periodically during long sessions to prevent context overflow while preserving the key information Claude needs.

## Common Antipatterns to Avoid

- Vague instructions without context or specific files
- Never running tests to verify changes actually work
- Skipping CLAUDE.md and repeating context every session
- Making sweeping requests ("rewrite the entire app") without planning first
- Ignoring `/review` before committing significant changes

> **Golden Rule:** Treat Claude Code as a collaborative pair programmer. Clear communication, specific context, and verification steps lead to the best outcomes — just like working with a human colleague.
