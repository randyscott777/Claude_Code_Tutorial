---
name: commit-reminder
description: Check whether the working tree has accumulated enough uncommitted changes to warrant a commit, and if so, summarize them and offer to commit. Use when the user invokes /commit-reminder.
---

# commit-reminder

When invoked, do the following:

1. Run `git status --short` and `git diff --stat HEAD` to see what has changed.
2. Count:
   - Files changed (modified + added + deleted + untracked).
   - Total lines changed (insertions + deletions from `--stat`).
3. Decide whether a commit is warranted. Threshold: **3+ files changed OR 50+ lines changed**. Untracked files count toward the file total.
4. Report one of two outcomes to the user:

   **Below threshold** — one short sentence: "Only N file(s) / M line(s) changed — no commit needed yet." Stop.

   **At/above threshold** — show:
   - A one-line summary of what changed (grouped by area, not a file list).
   - A proposed commit message (subject line only, imperative mood, under 70 chars).
   - Then ask: "Commit now? (yes / edit message / no)"

5. If the user says yes, create the commit following the standard git workflow in the main system prompt (HEREDOC message, `Co-Authored-By` trailer, no `-A`, never `--amend` unless asked). If they say "edit", wait for their revised message. If they say no, stop.

## Notes

- Do not push. Only commit.
- Do not stage files you did not inspect — if there are untracked files, list them and ask before adding.
- If there are zero changes, say so and stop.
