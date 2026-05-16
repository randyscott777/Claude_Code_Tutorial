# Claude Code on the Web

## Setup
* Use the /web-setup command to go to the Anthropic web at claude.ai/code
* Transfer from laptop to web (using claude --remote ???) - tbd
* Run from mobile to a running claude session - tbd

## Claude Code Routines (currently in 'Preview')
* Browse to claude.ai/code and choose routines or claude.ai/code/routines
* Test new or existing via 'Run Now'

### Define 'Briefing' routine
* Select Routines
* Create New
* Choose the Briefing template
* Take defaults for schedule and description
* Run Now to test

### Define 'Daily Email' routine
* Browse to claude.ai/code/routines
* Select Routines → Create New
* Set schedule to **9:00 AM daily**
* Set the repository to `Claude_Code_Tutorial`
* Use the following prompt:

```
Send an email to randyscott777@gmail.com with:
  Subject: Claude Code Routine
  Body: This is invoked from Claude Code Routine and defined to use the Claude_Code_Tutorial repo.
```

* Click Run Now to test (uses Gmail MCP to create and send the email)