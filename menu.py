import os
from rich.console import Console
from rich.markdown import Markdown

os.system('cls' if os.name == 'nt' else 'clear')

console = Console()

def show(filename):
    with open(filename) as f:
        console.print(Markdown(f.read()))

print("--- MAIN MENU FOR CLAUDE CODE ---")
print("1. introduction and overview")
print("2. setup and configure settings.json file ***WIP***")
print("3. commands by category and commonly used")
print("4. memory (cross session via CLAUDE.md)")
print("5. mcp servers for Google calendar, Gmail, and ***WIP***")
print("6. skills currently has explain-code and create-todo-list")
print("7. hooks ***TBD***")
print("8. git for version control and backup")
print("9. tips")
print("10. subagents TBD")
print("11. todos and markdown commands")
print("12. cost - token usage and balances")

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
