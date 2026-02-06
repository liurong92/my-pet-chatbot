from __future__ import annotations
from pydantic_ai import Agent

from init import create_and_update_memory, DataType, search_memery

pet_agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    instructions=f"""
        You are a Pet's management system, you can get pet information, such like name, age, like, etc.
        You can use get_pet_information tool, to get pet information.

        Answer format(MUST BE FOLLOW THIS FORMAT):
        <your answer>

        <your answer>
        - If you don't know, must response "I don't know".
        - No explanation, short answer.
    """
)

@pet_agent.tool(name="pet_agent", )
def get_pet_information(user_input):
    print("[TOOL]: Get pet information...")
    return search_memery(user_input, collection_name="system-resource")
