from __future__ import annotations
from pydantic_ai import Agent, RunContext

from mcp_service import toolsets
from init import search_memery

pet_system_agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    toolsets=[toolsets],
    instructions="""
        You are a Pet System, focus on pet's info and health.
        - First you should search memory, then search pet data if needed
        - Use the available MCP tools to retrieve pet information
        - Always respond in Chinese for better user experience
    """
)

