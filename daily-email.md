# Daily Email

## Setup
* On GitHub, setup a repo
* Invoke Calude and enter the following prompt:  
Create a github actions workflow that runs a python script daily to email me a hello message. 
Use environment secrets for credentials.
* Setup the 5 secrets
* Commit and push

## Folder Structure
daily-email (root repo)
- daily-email.py (python script to send an email)
- .github/workflows folder
- - daily-email.yml (GitHub config to CRON this task)

## Test Now
From a Claude prompt: Run now the daily-email repo on GitHub