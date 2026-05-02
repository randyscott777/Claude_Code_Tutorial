# Different Types of Memory
- CLAUDE.md files at global and project and local levels
- MEMORY.md files at global and within an app in the project
- .claude/rules
- VS Code terminal sessions

# CLAUDE.md
CLAUDE.md files let you give Claude Code persistent instructions that apply automatically to every session. Think of it as a briefing document Claude always reads before starting work on a project.

A `CLAUDE.md` (created by you via /init) in your project root is automatically loaded at the start of every Claude Code session. Use it to document things Claude should always know:

- Tech stack and architecture overview
- Coding standards and naming conventions
- Common development commands (`npm test`, `npm run dev`, etc.)
- Rules: things Claude should always or never do
- Project-specific context and gotchas

### Example CLAUDE.md

```
# Project: E-Commerce API

## Tech Stack
- Backend: Node.js + Express 4.x
- Database: PostgreSQL 15 with Prisma ORM
- Cache: Redis for sessions
- Tests: Jest + Supertest

## Coding Standards
- TypeScript strict mode enabled
- async/await only — no callbacks or .then()
- Error handling via AppError class (src/utils/AppError.ts)
- All new endpoints require auth middleware

## Commands
- npm test          Run full test suite
- npm run dev       Start dev server (port 3000)
- npm run migrate   Run Prisma migrations
- npm run lint      ESLint + Prettier check

## Rules
- NEVER commit .env files
- Always run tests before committing
- New DB migrations go in prisma/migrations/
- User-facing error messages must be friendly
```

### Memory File Locations

- `~/.claude/CLAUDE.md` — Global instructions applied to ALL projects
- `./CLAUDE.md` — Project-level instructions for the current project
- `./src/CLAUDE.md` — Subdirectory instructions (e.g., frontend-specific rules)

### The /memory Command

Use `/memory` to view, add, or remove entries from Claude's memory files:

```
> /memory
# Opens memory files for viewing

> prompt: Remember to use Tailwind CSS v3 for all styling
# Saves this fact to memory

> prompt: Forget the note about using Redux
# Removes that memory entry
```

> **Best Practice:** Manually create a CLAUDE.md before starting any project via /init. This single investment pays dividends on every future session — Claude arrives already knowing your conventions, eliminating repetitive context-setting.

claude /init to initially create the CLAUDE.md file in the project root directory or to update it (after major changes)

### /memory to display:
* if auto memory is on (on by default; toggle via `/memory` command, `"autoMemoryEnabled": false` in settings.json, or env var `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`)
* User memory in ~/.claude/CLAUDE.md
* Project memory in ./CLAUDE.md
* .claude\rules


# MEMORY.md:
## in ~/.claude/project/encoded-project-path/memory folder contents is an index to the following files:
* user role - You're a Claude Code tutorial author/learner
* Terse replies
* Powershell preference
* Remember my name
* Creation and Maintenance is Automatic and can have manual entries, done via "remember xxxx"
## in todos_list folder
* how created
* contents - database schema and how to run instruction
