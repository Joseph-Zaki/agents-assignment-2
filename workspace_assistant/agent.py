"""
Google Workspace Assistant - Main Agent Definition

Part 1: Implement tools and system instruction for Calendar OR Tasks
Part 2: Add McpToolset for GitHub integration
"""

import os

from config.settings import Settings
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from tools.calendar_tools import calendar_tools

# TODO: Import your chosen tool set
# from tools.calendar_tools import calendar_tools
# from tools.tasks_tools import tasks_tools

# TODO Part 2: Import MCP tools
# from tools.mcp_tools import mcp_tools


def create_agent() -> LlmAgent:
    """Create the Workspace Assistant agent."""
    settings = Settings()

    # TODO Part 1: Write your system instruction
    SYSTEM_INSTRUCTION = '''
        You are a helpful calendar management agent.

        You have the following tools:
        - `list_upcoming_events(max_results: int = 10, from_timestamp: str | None = None, to_timestamp: str | None = None)` - when you need to view events within a date and time or the user asks what's they have on their calendar
        - `create_event(summary: str, start_timestamp: str, end_timestamp: str, description: str | None = None, location: str | None = None)` - when you need to create an event. this also returns details of the event after creation.

        Always provide datetime objects in RFC3339 fromat with timezone offset. Unless otherwise specified, use Los Angeles timezone.
        '''

    # TODO Part 2: Create McpToolset for GitHub

    # TODO: Create and return your LlmAgent
    calendar_agent = LlmAgent(
        name = "calendar_assistant",
        model = settings.model_name,
        instruction=SYSTEM_INSTRUCTION,
        tools=calendar_tools
    )
    return calendar_agent


def create_agent_with_tool_search() -> LlmAgent:
    """BONUS: Create agent with defer_loading for tool search."""
    raise NotImplementedError("Bonus: Implement tool search pattern")
