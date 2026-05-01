#!/usr/bin/env python3
"""
hello_world.py — helper script for the hello-world Claude Code skill.

Usage: python hello_world.py [name]

Prints an ASCII banner greeting and a brief explanation of how
the skill's $ARGUMENTS extra-prompt feature passed the name in.
"""

import sys
from datetime import datetime

name = sys.argv[1] if len(sys.argv) > 1 else "World"
now = datetime.now().strftime("%Y-%m-%d %H:%M")

banner_width = max(len(name) + 14, 40)
border = "=" * banner_width
padding = " " * ((banner_width - len(name) - 8) // 2)

print(border)
print(f"|{padding}  Hello, {name}!{padding}  |")
print(border)
print()
print(f"  Greeted at : {now}")
print(f"  Name arg   : {name!r}  (came from $ARGUMENTS in SKILL.md)")
print(f"  Script     : .claude/skills/hello-world/hello_world.py")
print()
print("  How it works:")
print("    1. User types  /hello-world Alice")
print("    2. Claude Code replaces $ARGUMENTS with 'Alice' in SKILL.md")
print("    3. SKILL.md instructs Claude to run this script with that name")
print("    4. Script output is shown verbatim — no hallucination needed")
