"""
Option A: Calendar Assistant Tools

Implement at least 3 tools for Google Calendar operations.
"""

from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from google.adk.tools import FunctionTool
from tools.auth import get_calendar_service

# TODO: Implement your calendar tools
# Define each tool as a plain Python function with a clear docstring and type
# hints (ADK reads these to build the tool schema and auto-wraps the function),
# then add it to the list below. Each tool should return a dict with 'status'
# and relevant data. Wrapping with FunctionTool(func=my_function) is optional
# and only needed when you want explicit control over the tool.

service = get_calendar_service()

def list_upcoming_events(max_results: int = 10, from_time: datetime | None = None, to_time: datetime | None = None) -> dict:
    if from_time is None:
        from_time = datetime.now(ZoneInfo("America/Los_Angeles"))

    formatted_from_time = from_time.replace(microsecond=0).isoformat(timespec='seconds')

    if to_time:
        formatted_to_time = to_time.replace(microsecond=0).isoformat(timespec='seconds')

    try:
        service = get_calendar_service()
        events_result = service.events().list(
            calendarId='primary', maxResults=max_results, timeMin = formatted_from_time
        ).execute()
        return {"status": "success", "events": events_result.get("items", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def create_event():
    pass

calendar_tools = [list_upcoming_events]

if __name__ == "__main__":
    print(list_upcoming_events())