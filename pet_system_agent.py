from __future__ import annotations
from pydantic_ai import Agent, RunContext

from init import search_memery
from pet_agent import pet_agent

pet_system_agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    instructions=f"""
        You are a Pet System, focus on pet's info and health.
            - First you should search memory, then search pet data if needed
            - You can using search_pet_data and search_memory_data tools
    """
)

@pet_system_agent.tool
def search_memory_data(ctx: RunContext, user_input: str):
    print("[TOOL]: Start searching memery data...")
    return search_memery(user_input)


@pet_system_agent.tool
def search_pet_data(ctx: RunContext, user_input: str):
    print("[TOOL]: Start searching pet database...")
    return pet_agent.run_sync(user_input, usage=ctx.usage).output

