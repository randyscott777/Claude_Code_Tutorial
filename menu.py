import os
from rich.console import Console
from rich.markdown import Markdown

os.system('cls' if os.name == 'nt' else 'clear')

console = Console()

def show(filename):
    with open(filename, encoding="utf-8") as f:
        console.print(Markdown(f.read()))

print("--- MAIN MENU FOR CLAUDE CODE ---")
print("Introduction and overview")
print("1.1 Introduction")
print("1.2 Overview")
print("Installation, Setup, and Configurations")
print("2. Setup and configure settings.json file")
print("2.1. - Custom Status Line")
print("2.2. - Keyboard Shortcuts ***TBD**")
print("3. Commands by category and commonly used")
print("4. Memory (across sessions via CLAUDE.md)")
print("5. MCP servers for Google calendar, Gmail, and Github")
print("6. Skills for explain-code and create-todo-list")
print("7. Hook for Claude stop notifications")
print("8. Github for version control and backup")
print("9. Tips")
print("10. Subagents ***TBD***")
print("11. Todos for future development and markdown commands")
print("12. Costs - token usage and balances")
print("13. List messages in Gmail inbox")
print("14. Plugins and Marketplace ***TBD***")
print("15. Remote Control ***TBD***")
print("16. Agent TEAMS ***TBD***")
print("17. Web and Routines")
print("18. Claude Agent SDK")
print("19. Display all files using Claude Agent SDK")
print("20. Display all TODO comments using Claude Agent SDK")

option = float(input("Enter the number of the file you want to read: ") or 0)

print('\n ')

if option == 1.1:
    show("intro.md")
    
if option == 1.2:
    show("overview.md")

if option == 2:
    show("setup.md")
    
if option == 2.1:
    show("StatusLine.md")

if option == 3:
    show("commands.md")

if option == 4:
    show("memoryDoc.md")

if option == 5:
    show("mcp.md")

if option == 6:
    show("skills.md")

if option == 7:
    show("hooks.md")

if option == 8:
    show("git.md")

if option == 9:
    show("tips.md")

if option == 10:
    print("subagents TBD")

if option == 11:
    show("todos.md")

if option == 12:
    show("cost.md")

if option == 13:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    CREDS_PATH = os.path.expanduser('~/.config/mcp-gmail/credentials.json')
    CLIENT_SECRETS = os.path.expanduser('~/.config/mcp-gdrive/gcp-oauth.keys.json')

    creds = None
    if os.path.exists(CREDS_PATH):
        creds = Credentials.from_authorized_user_file(CREDS_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(CREDS_PATH), exist_ok=True)
        with open(CREDS_PATH, 'w') as f:
            f.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=25).execute()
    messages = results.get('messages', [])

    if not messages:
        console.print("[yellow]No messages found in inbox.[/yellow]")
    else:
        console.print(f"\n[bold cyan]Gmail Inbox[/bold cyan] — {len(messages)} messages\n")
        for msg in messages:
            detail = service.users().messages().get(
                userId='me', id=msg['id'], format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            headers = {h['name']: h['value'] for h in detail['payload']['headers']}
            subject = headers.get('Subject', '(no subject)')
            sender = headers.get('From', '(unknown)')
            date = headers.get('Date', '')[:16]
            console.print(f"[green]{date:<18}[/green] [yellow]{sender[:35]:<37}[/yellow] {subject}")

if option == 17:
    show("web.md")
 
if option == 18:
    show("sdk.md")


if option == 19:
    print("This is a long running process to display all files using Claude Agent SDK...\n")
    import sdk_files_example
    sdk_files_example.main()  # Directly calls the logic

if option == 20:
    print("This is a long running process to display all TODO comments using Claude Agent SDK...\n") 
    with open("sdk_todos_example.py") as f:
        exec(f.read())

# TODO - some examples 
