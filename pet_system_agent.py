"""
Pet System Agent Module

This module provides the main AI agent for the pet chatbot system.
The agent uses Claude Sonnet 4.5 with MCP tools to answer questions
about pets using RAG (Retrieval-Augmented Generation).
"""

from __future__ import annotations
from pydantic_ai import Agent

from mcp_service import toolsets

# Model configuration
MODEL_NAME = "anthropic:claude-sonnet-4-5"
# MODEL_NAME = "google-gla:gemini-3-flash-preview"

# Agent instructions
SYSTEM_INSTRUCTIONS = """
You are an intelligent Pet Information Assistant focused on providing helpful information about pets' health, behavior, and care.

## Your Capabilities:
- Access to a knowledge base containing pet information from documents (PDFs and text files)
- Memory of previous conversations to provide contextual responses
- Tools to search both historical conversations and system resources

## Response Guidelines:
1. **Search Strategy**: Always search conversation memory first, then query the knowledge base if needed
2. **Language**: Respond in Chinese for better user experience
3. **Accuracy**: Only provide information you can verify from your knowledge base
4. **Tone**: Be friendly, helpful, and concise
5. **Unknown Information**: If you don't know something, say "我不知道" (I don't know) honestly

## Response Format:
- Provide clear, structured answers
- Use bullet points for lists
- Include relevant details like pet names, characteristics, and preferences
- Keep responses concise but informative
"""

# Initialize the pet system agent
pet_system_agent = Agent(
    model=MODEL_NAME,
    toolsets=[toolsets],
    instructions=SYSTEM_INSTRUCTIONS,
)


def get_agent() -> Agent:
    """
    Get the pet system agent instance.

    Returns:
        Agent: The configured pet system agent
    """
    return pet_system_agent


__all__ = ["pet_system_agent", "get_agent"]
