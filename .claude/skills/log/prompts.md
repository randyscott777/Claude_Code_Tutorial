# Example Prompts for the Hello World Skill

These are sample user prompts that should trigger the `log` skill.
Use them to test the skill or to expand its `description` field for better matching.

## Direct invocation

- `/log`

## Natural-language triggers

- "save"


## Prompts that should NOT trigger this skill

These are too generic or belong to other skills — listed here so you can tune
the `description` field if false positives become a problem.

- "hello, can you help me debug this?" (a real coding request)
- "create a list of greetings" (belongs to `create-a-list`)
- "explain how greetings work in this codebase" (belongs to `explain_code`)
