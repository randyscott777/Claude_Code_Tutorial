import os
from rich.console import Console
from rich.markdown import Markdown

os.system('cls' if os.name == 'nt' else 'clear')

console = Console()

def show(filename):
    with open(filename, encoding="utf-8") as f:
        console.print(Markdown(f.read()))

print("--- MAIN MENU FOR CLAUDE CODE ---")
print("1. Introduction and overview")
print("2. Setup and configure settings.json file")
print("3. Commands by category and commonly used")
print("4. Memory (cross session via CLAUDE.md)")
print("5. MCP servers for Google calendar, Gmail, and Github")
print("6. Skills for explain-code and create-todo-list")
print("7. Hook for Claude stop notifications")
print("8. Github for version control and backup")
print("9. Tips")
print("10. Subagents ***TBD***")
print("11. Todos for future development and markdown commands")
print("12. Costs - token usage and balances")

opt = input("Enter the number of the file you want to read: ")

if opt == "1":
    show("intro.md")

if opt == "2":
    show("setup.md")

if opt == "3":
    show("commands.md")

if opt == "4":
    show("memory.md")

if opt == "5":
    show("mcp.md")

if opt == "6":
    show("skills.md")

if opt == "7":
    show("hooks.md")

if opt == "8":
    show("git.md")

if opt == "9":
    show("tips.md")

if opt == "10":
    print("subagents TBD")

if opt == "11":
    show("todos.md")

if opt == "12":
    show("cost.md")
