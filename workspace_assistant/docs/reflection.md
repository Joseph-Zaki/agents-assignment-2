# Assignment 2 Reflection

**Name:** Joseph Zaki
**Option:** A - Calendar
**Date:** 10/11/2026

---

## Tool Design Decisions

### Tools Implemented
1. **list_upcoming_events**: Provides a list of events scheduled on Google Calendar between given date and time range.
2. **create_event**: Schedules a new event at the specified time with the given summary, description, and location.
3. **delete_event**: Deletes the desired event (by eventId)
4. **reschedule_event**: Changes the start and end time of the desired event (by eventId)

### Why These Tools?
I chose to focus on tools that allow the agent to manage and modify the user's calendar. The only informational tool is the `list_upcoming_events` tool, which is necessary to find the `eventId` for use in the other tools. I found it helpful to provide a conversational interface to Google Calendar. Pairing the calendar with natural language processing allowed for conversational changes and booking. Things like "Bump my music lesson by a couple of days" led the agent to listing the events, finding the music lesson, determining the timestamps for a couple (2 days) later, and calling the `reschedule_event` tool.

### Description Strategy
I chose to write my descriptions with a very clear and short summary. For example "Create a new event in the user's primary Google Calendar". In addition to this I explained the Arguments and possible returns. I found that the most helpful strategy was providing examples of arguments, especially when it came to timestamp formats. The agent became very good at supplying timestamps in the correct format and time zone.

---

## Challenges Encountered

### Challenge 1: Session not found error
- **Problem:** It was difficult to initially get Google ADK working. I repeatedly got an error saying the session was not found.
- **Solution:** I fixed this by modifying `main.py` to initialize the session before calling `runner.run()`. This took some time and experimentation to figure out.

### Challenge 2: Connecting to GitHub MCP
- **Problem:** As far as I understand, the nodeJS GitHub MCP package is deprecated and I faced lots of issues getting the MCP server working. I would get module not found errors, then once I resolved that, the agent could not consistently write/create issues.
- **Solution:** I had to clear my npm cache, verify my npm and npx installations, modify the system instructions to include the GitHub MCP, use `Remove-Item -Recurse -Force "$env:LOCALAPPDATA\npm-cache\_npx\3dfbf5a9eea4a1b3"` to purge my npm cache. Overall, it was a long series of trouble shooting steps, but I am still not sure why the model can't consistently create GitHub issues.

---

## Error Handling Approach

I tried to use error handling to keep the model grounded and avoid illogical API calls. For example, I would verify the timestamp formats to ensure the agent was providing times in the RFC3339 format required by the Google Calendar API. I also checked that end times came after start times. In case of API errors, I provided the agent with the error message so it could determine the best course of action.

---

## Ideas for Improvement

If you had more time, what would you add or change?

1. More detail in error handling - I would expand how many edge cases I handle, possibly consider handling different types of API errors (429 for rate limiting, 500 errors for internal server errors).
2. I think separating the Google Calendar functionality and the GitHub functionality into two separate agents might make more sense. I don't think having the same agent handle scheduling and calendar management as well as GitHub repos makes sense and makes the system somewhat confusing to work with.
3. I would like to extend the Google Calendar functionality
    - Handle Schedule Conflicts
    - Invite other people to events
    - Keep a memory of contacts and their emails to add them to events without providing the email each time
    - Handle recurring events


---

## Key Learnings

The primary takeaway for me from this assignment was the experience in building custom tools. This was the most exciting part of the assignment to me since this is what will enable me to build useful agentic systems with several capabilities. Additionally, I learned how to provide structured and guiding tool descriptions and agent instructions.

While working on this assignment the importance of example arguments and formats became very apparent, especially since the Google Calendar API requires very specific timestamp formats. I also learned that I can access the agent's ReAct workflow by asking it to perform a task, then asking it to explain how it completed it. The agent would go on to explain why it asked clarifying questions, which tools it used and what their results were, and finally was the agent successful or not. In cases where it was not successful, it tried again, learing from the feedback of the error messages.

The most surprising thing I found was how impactful the error messages were in improving the model's performance. They allowed the model to recover gracefully when it provided an improper time stamp for example. At one point I asked the model to reschedule an event then explain how it did it. The model explained that it encountered an issue using the `reschedule_event` tool, so it reasoned that it could simply use `delete_event` then `create_event` to effectively work around the issue and still complete the task of rescheduling.