"""
Option A: Calendar Assistant Tools

Implement at least 3 tools for Google Calendar operations.
"""

from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from google.adk.tools import FunctionTool

from .auth import get_calendar_service

# TODO: Implement your calendar tools
# Define each tool as a plain Python function with a clear docstring and type
# hints (ADK reads these to build the tool schema and auto-wraps the function),
# then add it to the list below. Each tool should return a dict with 'status'
# and relevant data. Wrapping with FunctionTool(func=my_function) is optional
# and only needed when you want explicit control over the tool.

service = get_calendar_service()

def _format_datetime(datetime: datetime) -> str | None:
    if datetime:
        return datetime.replace(microsecond=0).isoformat(timespec="seconds")
    return None

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
            return {"status" : "error", "message" : f"Invalid timestamp: {str(e)}"}

    if to_timestamp:
        try:
            to_datetime = datetime.fromisoformat(to_timestamp)
        except Exception as e:
            return {"status" : "error", "message" : f"Invalid timestamp: {str(e)}"}

    try:
        events_result = service.events().list(
            calendarId='primary', 
            maxResults=max_results, 
            timeMin = _format_datetime(from_datetime),
            timeMax = _format_datetime(to_datetime)
        ).execute()
        return {"status": "success", "events": events_result.get("items", [])}
    except Exception as e:
        return {"status": "error", "message": f"Error fetching events: {str(e)}"}


def create_event(summary: str, start_timestamp: str, end_timestamp: str, description: str | None = None, location: str | None = None) -> dict:
    """
    Create a new event in the user's primary Google Calendar.

    Args:
        summary: The title of the event.
        start_time: RFC 3339 start timestamp with timezone offset,
            e.g. '2026-10-12T14:00:00-07:00'.
        end_time: RFC 3339 end timestamp with timezone offset,
            e.g. '2026-10-12T15:00:00-07:00'.
        description (optional): Details about the event.
        location: Optional event location.

    Returns:
        A dictionary containing the creation status and event details.
    """
    try:
        start_datetime = datetime.fromisoformat(start_timestamp)
        end_datetime = datetime.fromisoformat(end_timestamp)
        # verify timezone offset is included
        if start_datetime.utcoffset() is None or end_datetime.utcoffset() is None:
            return {
                "status": "error",
                "message": "Both timestamps must include a timezone offset, such as -07:00 or +00:00."
            }

        if end_datetime <= start_datetime:
            return {
                "status" : "error",
                "message" : "End time must come after start time."
            }

        event_body = {
            "summary": summary,
            "start": {"dateTime": _format_datetime(start_datetime)},
            "end": {"dateTime": _format_datetime(end_datetime)}
        }

        if description:
            event_body["description"] = description

        if location:
            event_body["location"] = location

        created_event = service.events().insert(
            calendarId = "primary",
            body = event_body
        ).execute()

        return {
            "status": "success",
            "message": "Event created successfully.",
            "event": {
                "id": created_event.get("id"),
                "summary": created_event.get("summary"),
                "start": created_event.get("start"),
                "end": created_event.get("end"),
                "htmlLink": created_event.get("htmlLink"),
            },
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def delete_event(eventId: str) -> dict:
    '''
    Delete the event with the provided eventId.

    Args:
        - eventId: The ID of the event you wish to delete.
    '''
    try:
        deleted_event = service.events().delete(
            calendarId = 'primary',
            eventId = eventId
        ).execute()

        return {"status" : "success", "message": f"Event {eventId} deleted. API response {deleted_event.status}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def reschedule_event(eventId: str, new_start_timestamp: str, new_end_timestamp: str) -> dict:
    """
    Reschedule an existing Google Calendar event.

    Args:
        eventId: The ID of the event to reschedule.
        new_start_time: RFC 3339 start timestamp with timezone offset,
                        e.g. '2026-10-12T14:00:00-07:00'.
        new_end_time: RFC 3339 start timestamp with timezone offset,
                        e.g. '2026-10-12T14:00:00-07:00'.

    Returns:
        A dictionary indicating success or failure.
    """
    try:
        start_datetime = datetime.fromisoformat(new_start_timestamp)
        end_datetime = datetime.fromisoformat(new_end_timestamp)
        # verify timezone offset is included
        if start_datetime.utcoffset() is None or end_datetime.utcoffset() is None:
            return {
                "status": "error",
                "message": "Both timestamps must include a timezone offset, such as -07:00 or +00:00."
            }

        if end_datetime <= start_datetime:
            return {
                "status" : "error",
                "message" : "End time must come after start time."
            }
        
        updated_event = service.events().patch(
            calendarId = "primary",
            eventId = eventId,
            body = {
                "start" : {"dateTime" : _format_datetime(start_datetime)},
                "end" : {"dateTime" : _format_datetime(end_datetime)}
            }
        ).execute()

        return {
            "status": "success",
            "message": f"Event '{updated_event.get('summary', eventId)}' rescheduled successfully.",
            "event": {
                "id": updated_event.get("id"),
                "summary": updated_event.get("summary"),
                "start": updated_event.get("start"),
                "end": updated_event.get("end"),
                "htmlLink": updated_event.get("htmlLink"),
            },
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


    
calendar_tools = [list_upcoming_events, create_event, delete_event, reschedule_event]

if __name__ == "__main__":
    print(list_upcoming_events())