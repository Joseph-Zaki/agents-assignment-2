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

def list_upcoming_events(max_results: int = 10, from_timestamp: str | None = None, to_timestamp: str | None = None) -> dict:
    '''Fetch upcoming events from Google Calendar between 'from_time' and 'to_time'.

    Use this when you need to determine what events occurring between two datetimes or when the user asks what's on their calendar.

    Args:
        max_results (optional, defaults to 10): Maximum number of upcoming events to return, integer (e.g. 5, 10)
        from_timestamp (optional, defaults to current time): Earliest possible start time for returned events. RFC3339 format with timezone offset. (e.g. 2026-10-11T14:09:45-07:00)
        to_timestamp (optional): Latest possible start time for returned events. RFC3339 format with timezone offset. (e.g. 2026-10-11T14:09:45-07:00)
    '''
    if from_timestamp is None:
        # Default to current datetime, Pacific Time
        from_datetime = datetime.now(ZoneInfo("America/Los_Angeles"))
    else:
        try:
            from_datetime = datetime.fromisoformat(from_timestamp)
        except Exception as e:
            return {"status" : "error", "message" : str(e)}

    formatted_from_time = from_datetime.replace(microsecond=0).isoformat(timespec='seconds')

    if to_timestamp:
        try:
            to_datetime = datetime.fromisoformat(to_timestamp)
        except Exception as e:
            return {"status" : "error", "message" : str(e)}
        formatted_to_time = to_datetime.replace(microsecond=0).isoformat(timespec='seconds')

    try:
        service = get_calendar_service()
        events_result = service.events().list(
            calendarId='primary', 
            maxResults=max_results, 
            timeMin = formatted_from_time,
            timeMax = formatted_to_time
        ).execute()
        return {"status": "success", "events": events_result.get("items", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def create_event():
    pass

calendar_tools = [list_upcoming_events]

if __name__ == "__main__":
    print(list_upcoming_events())