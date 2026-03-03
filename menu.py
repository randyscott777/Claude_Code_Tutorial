import os
os.system('cls' if os.name == 'nt' else 'clear')

print("MAIN MENU FOR CLAUDE CODE")
print("1. intro.md")
print("2. setup.md")
print("3. commands.md") 
print("4. memory.md") 
print("5. hooks.md") 
print("6. mcp.md") 
print("7. tips.md") 
print("8. skills.md") 
print("9. git.md TBD") 
print("10. subagents.md TBD") 

opt = input("Enter the number of the file you want to read: ")

if opt == "1":
    with open("intro.md", "r") as f:
        print(f.read())
        
if opt == "2":
    with open("setup.md", "r") as f:
        print(f.read())

if opt == "3":
    with open("commands.md", "r") as f:
        print(f.read())

if opt == "4":
    with open("memory.md", "r") as f:
        print(f.read())

if opt == "5":
    with open("hooks.md", "r") as f:
        print(f.read())

if opt == "6":
    with open("mcp.md", "r") as f:
        print(f.read())

if opt == "7":
    with open("tips.md", "r") as f:
        print(f.read())

if opt == "8":
    with open("skills.md", "r") as f:
        print(f.read())

if opt == "9":
    with open("git.md", "r") as f:
        print(f.read())

