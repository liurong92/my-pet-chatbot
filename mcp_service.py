from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from init import search_memery


class MCPService:
    def __init__(self, name: str = "pet-service"):
        self.mcp = FastMCP(name)

        # Register tools as simple callables that accept a single user_input argument.
        # We use small closures so the tool system will call functions that only
        # accept `user_input` (the tool runner won't know about `self`).
        self.mcp.tool()(self.get_pet_information)
        self.mcp.tool()(self.search_memory_data)

        # Toolset helper
        self.toolset = FastMCPToolset(self.mcp)

    def get_pet_information(self, user_input):
        print("[TOOL]: Get pet information...")
        return search_memery(user_input, collection_name="system-resource")

    def search_memory_data(self, user_input: str):
        print("[TOOL]: Start searching memery data...")
        return search_memery(user_input)


_service: Optional[MCPService] = None


def create_service(name: str = "pet-service") -> MCPService:
    return MCPService(name=name)


def get_service() -> MCPService:
    global _service
    if _service is None:
        _service = MCPService()
    return _service


def get_mcp() -> FastMCP:
    return get_service().mcp


def get_toolset() -> FastMCPToolset:
    return get_service().toolset


# Exports: prefer `MCPService`, `create_service`, and `get_service`.
__all__ = [
    "create_service",
    "get_service",
    "get_mcp",
    "get_toolset",
]

# For convenience and backwards compatibility, provide a default service instance
# so callers can `from mcp_service import service` and use it directly.
service = MCPService()
mcp = service.mcp
toolsets = service.toolset

# Export convenience names
__all__.extend(["service", "mcp", "toolsets"])

