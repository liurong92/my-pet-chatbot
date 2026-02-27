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


def create_agent(model_name: str, api_key: str) -> Agent:
    """
    Create an agent with a custom model and API key.

    Supported provider prefixes: anthropic, openai, google-gla, groq, mistral.
    If no prefix is given, the provider is inferred from the model name.

    Args:
        model_name: Model identifier, e.g. "anthropic:claude-sonnet-4-5" or "claude-sonnet-4-5"
        api_key: API key for the specified provider

    Returns:
        Agent: A configured agent using the given model and key
    """
    if ":" in model_name:
        provider, model_id = model_name.split(":", 1)
    else:
        model_id = model_name
        if model_name.startswith("claude"):
            provider = "anthropic"
        elif model_name.startswith(("gpt-", "o1", "o3", "o4")):
            provider = "openai"
        elif model_name.startswith("gemini"):
            provider = "google-gla"
        else:
            provider = "anthropic"

    if provider == "anthropic":
        from pydantic_ai.models.anthropic import AnthropicModel
        from pydantic_ai.providers.anthropic import AnthropicProvider
        model = AnthropicModel(model_id, provider=AnthropicProvider(api_key=api_key))
    elif provider == "openai":
        from pydantic_ai.models.openai import OpenAIModel
        from pydantic_ai.providers.openai import OpenAIProvider
        model = OpenAIModel(model_id, provider=OpenAIProvider(api_key=api_key))
    elif provider in ("google-gla", "google"):
        from pydantic_ai.models.google import GoogleModel
        from pydantic_ai.providers.google import GoogleProvider
        model = GoogleModel(model_id, provider=GoogleProvider(api_key=api_key))
    elif provider == "groq":
        from pydantic_ai.models.groq import GroqModel
        from pydantic_ai.providers.groq import GroqProvider
        model = GroqModel(model_id, provider=GroqProvider(api_key=api_key))
    elif provider == "mistral":
        from pydantic_ai.models.mistral import MistralModel
        from pydantic_ai.providers.mistral import MistralProvider
        model = MistralModel(model_id, provider=MistralProvider(api_key=api_key))
    else:
        # Fall back to string format and let pydantic-ai resolve it
        model = f"{provider}:{model_id}"

    return Agent(
        model=model,
        toolsets=[toolsets],
        instructions=SYSTEM_INSTRUCTIONS,
    )


def get_agent() -> Agent:
    """
    Get the default pet system agent instance.

    Returns:
        Agent: The configured pet system agent
    """
    return pet_system_agent


__all__ = ["pet_system_agent", "get_agent", "create_agent"]
