# Git & GitHub with Claude Code

Claude Code has deep git and GitHub integration. It can commit, branch, diff, create pull requests, and manage your full version control workflow — all from natural language instructions or slash commands.

---

### Git Slash Commands

| Command | What it does |
|---------|--------------|
| `/commit` | Analyze staged changes and generate a conventional commit message |
| `/diff` | Show and explain recent git changes |
| `/pr` | Create a GitHub pull request with an auto-generated description |
| `/review` | Review staged changes for bugs, security issues, and style problems |

---

### Natural Language Git Operations

You don't need to remember git syntax. Just describe what you want:

```
"Commit all my changes with a meaningful message"
"Create a new branch called feature/login"
"Show me what changed since the last commit"
"Push this branch and open a pull request"
"Revert the last commit"
"What does the git log look like for this file?"
```

Claude translates your intent into the correct git commands and executes them.

---

### Commits

Claude follows **Conventional Commits** format by default:

```
feat: add user authentication
fix: resolve null pointer in cart service
refactor: extract payment logic into service
docs: update API usage examples
test: add unit tests for order processor
```

Example workflow:

```
> Stage your changes, then run /commit

Analyzing staged changes...

Proposed commit message:
  feat: add password reset flow

  - Add POST /reset-password endpoint
  - Send reset email via SendGrid integration
  - Token expires after 1 hour
  - Added 4 integration tests

Create this commit? [Y/n]: Y
✓ Committed: a1b2c3d
```

> **Safety Rule:** Claude will NEVER auto-commit without your approval. It always shows the proposed message and waits for confirmation.

---

### Branches

```
"Create a branch called fix/header-overflow"
"Switch to the main branch"
"List all branches"
"Delete the old feature branch"
"Merge this branch into main"
```

Claude uses standard `git branch`, `git checkout`, and `git merge` commands under the hood.

---

### Pull Requests with `gh`

Claude uses the **GitHub CLI (`gh`)** to create and manage pull requests. The `gh` tool must be installed and authenticated:

```bash
gh auth login
```

Once authenticated, Claude can:

```
"Create a pull request for this branch"
"Show open pull requests"
"Review PR #42"
"Merge pull request #38"
"Check the status of CI checks on PR #55"
```

#### Example: Creating a PR

```
> /pr

Analyzing branch vs main...

Title: feat: add password reset flow
Body:
  ## Summary
  - Add POST /reset-password endpoint
  - Send reset email via SendGrid
  - Token expires after 1 hour

  ## Test plan
  - [ ] Verify reset email is sent
  - [ ] Confirm token expiry works
  - [ ] Check UI error states

Create pull request? [Y/n]: Y
✓ PR created: https://github.com/you/repo/pull/12
```

---

### Diffs and History

```
"Show me what changed in the last commit"
"Diff this file against main"
"What files changed in the last 3 commits?"
"Explain the changes in this PR"
"Show me the git log for src/auth.py"
```

Claude can read and **explain** diffs in plain English — useful for understanding unfamiliar changes or reviewing someone else's work.

---

### Code Review

The `/review` command inspects staged or recent changes and reports:

- Bugs and logic errors
- Security vulnerabilities (injection, exposed secrets, etc.)
- Style and convention violations
- Missing tests or edge cases

```
> /review

Reviewing staged changes...

⚠ auth/login.js:34 — password compared before hashing
⚠ api/users.js:12 — user input passed directly to SQL query (injection risk)
✓ tests/auth.test.js — good coverage of happy path

2 issues found. Fix before committing?
```

---

### Git Safety Rules

Claude Code follows strict safety rules for git operations:

| Action | Behavior |
|--------|----------|
| Commit | Always asks for approval first |
| Push | Confirms before pushing to remote |
| Force push to main/master | **Refused** — Claude will warn you |
| `git reset --hard` | Warns before running destructive resets |
| `--no-verify` (skip hooks) | Only runs if you explicitly request it |
| Amend published commits | Warns that this rewrites history |

> **Key Principle:** Claude treats your git history as precious. It will always communicate what it's about to do before making irreversible changes.

---

### Working with Issues

With `gh` authenticated, Claude can interact with GitHub Issues:

```
"Show open issues labeled bug"
"Create an issue for the login crash"
"Comment on issue #23 with the fix details"
"Close issue #15"
"List issues assigned to me"
```

---

### Tips

- **Stage files yourself** with `git add` before asking Claude to commit, or ask Claude to stage specific files by name
- **Use `/diff` before `/commit`** to verify what's being committed
- Allow push to update the remote repository
- **Ask Claude to explain commits** from other contributors: *"Explain what commit abc123 does"*
- **Claude reads PR comments** — paste a GitHub PR URL and ask *"What is this PR doing?"*
