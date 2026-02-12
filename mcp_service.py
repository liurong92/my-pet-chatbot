from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from init import search_memery

mcp = FastMCP("pet-service")

@mcp.tool()
def get_pet_information(user_input):
    print("[TOOL]: Get pet information...")
    return search_memery(user_input, collection_name="system-resource")


@mcp.tool()
def search_memory_data(user_input: str):
    print("[TOOL]: Start searching memery data...")
    return search_memery(user_input)

toolset: FastMCPToolset = FastMCPToolset(mcp)
