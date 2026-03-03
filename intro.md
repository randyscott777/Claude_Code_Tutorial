# Introduction to Claude Code

Claude Code is an **agentic AI coding assistant** that operates directly in your terminal. It understands your codebase and can take real actions — reading files, writing code, running tests, and managing your full development workflow.

### What Makes Claude Code Different?

Unlike chatbots where you copy-paste code back and forth, Claude Code works *inside your environment*. It has direct access to your filesystem, can execute shell commands, and completes multi-step tasks autonomously — just like a developer sitting at the keyboard.

> **Key Insight:** Claude Code is an *agent*, not a chatbot. It can chain dozens of actions — reading files, running tests, editing code — to complete a complex task from a single instruction.

### Core Capabilities

- **File Operations** — Read, create, edit, and delete files across your project
- **Command Execution** — Run tests, build scripts, linters, and shell commands
- **Codebase Understanding** — Analyze structure, patterns, and dependencies
- **Git Integration** — Commits, branches, diffs, pull requests, and history
- **Multi-step Automation** — Chain complex workflows from one instruction


### Claude Code Version

claude --version (from the command line it displays the version of Claude Code)


### Claude Code Prompt

Prompts can be anything with double quotes, for example:
- claude /doctor
- claude --version will display the version in 1.2.3 format
- claude "What does this project do?"
- claude -p "prompt" switch executes the prompt and returns to the command line
- claude -c switch continues the current conversation
- claude -r switch continues the previous conversation
- claude /help will display a link to Claude Code website for the options
- claude /model modelname' will use the model specified or blank for the picker
Note: use opus for planning and then sonnet for building
- claude /clear will clear the current conversation
- claude /exit will end claude code agent and return to the command line
