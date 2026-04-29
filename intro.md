# Introduction to Claude Code

Claude Code is an **agentic AI coding assistant** that operates directly in your terminal. It understands your codebase and can take real actions — reading files, writing code, running tests, and managing your full development workflow.

### Platforms
* Terminal / command line (CLI))
* Web at claude.ai/code
* Desktop
* VS Code (via extension)
* Chrome (via extension)
* JetBrains

### What Makes Claude Code Different?

Unlike chatbots where you copy-paste code back and forth, Claude Code works *inside your environment*. It has direct access to your filesystem, can execute shell commands, and completes multi-step tasks autonomously — just like a developer sitting at the keyboard.

> **Key Insight:** Claude Code is an *agent*, not a chatbot. It can chain dozens of actions — reading files, running tests, editing code — to complete a complex task from a single instruction.

### Core Capabilities

- **File Operations** — Read, create, edit, and delete files across your project
- **Command Execution** — Run tests, build scripts, linters, and shell commands
- **Codebase Understanding** — Analyze structure, patterns, and dependencies
- **Git Integration** — Commits, branches, diffs, pull requests, and history
- **Multi-step Automation** — Chain complex workflows from one instruction

# Features of Claude Code Usage in this Project
* Setup settings.json - in user for command to display a status line command (only works for a bash terminal and therefore had to change the default terminal setting)
  extension panel and by claude.ai 
  and in project for hook at stop time to display a Windows completion meesage
* Commands - deadcode in project
* Memory - cross session in CLAUDE.md file, created via claude /init
* MCP servers - Google Calendar, Gmail, filesystem
* Skills - explain-code, create-todo-list, create-a-system, frontend-design, plan-an=app (user)  
           and commit-reminder (project level)
* Hooks - see in project settings.json
* Sub Agents - invoke via /agents
* Git - for version control and commitment 
* Cost - show tokens used and balances
* Apps - menu (CLI), django_todo, todo_flask, todo_kivy, and SDK examples  
  and daily-email in GitHub (cron via .yml file)


