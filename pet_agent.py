from __future__ import annotations
from pydantic_ai import Agent

from mcp_service import toolset
from init import create_and_update_memory, DataType, search_memery

pet_agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    toolsets=[toolset],
    instructions=f"""
        You are a Pet's management system, you can get pet information, such like name, age, like, etc.

        Answer format(MUST BE FOLLOW THIS FORMAT):
        <your answer>

        <your answer>
        - If you don't know, must response "I don't know".
        - No explanation, short answer.
    """
)
