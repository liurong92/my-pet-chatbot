from __future__ import annotations
from pydantic_ai import Agent, RunContext

from mcp_service import toolsets

from init import search_memery
from pet_agent import pet_agent

pet_system_agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    toolsets=[toolsets],
    instructions=f"""
        You are a Pet System, focus on pet's info and health.
            - First you should search memory, then search pet data if needed
            - You can call the search_pet_data tool to call pet agent to search pet data
    """
)

