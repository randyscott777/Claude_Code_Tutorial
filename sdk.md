# Claude Agent (Code) SDK

## Usage
1.) pip install claude.agent.sdk


2.) Code:

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="Find all TODO comments and create a summary",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"]),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())

3.) Run as python xxx.py  

