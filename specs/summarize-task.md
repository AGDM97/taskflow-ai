# Feature: Summarize Task

## Goal
Allow a user to generate a short summary for an existing task.

## Business Rules
1. The task ID is required.
2. The task must exist.
3. The summary must include the task title.
4. The summary must include the task status.
5. The summary must include the task priority.
6. If the task has a description, the summary should include it.
7. If the task does not exist, return HTTP 404.
8. The response must return the task ID and generated summary.

## Acceptance Criteria

### Scenario 1: Summarize existing task with description
Given an existing task with title and description
When the user requests a summary
Then the system returns HTTP 200
And returns a summary containing title, description, status and priority

### Scenario 2: Summarize existing task without description
Given an existing task without description
When the user requests a summary
Then the system returns HTTP 200
And returns a summary containing title, status and priority

### Scenario 3: Task not found
Given a non-existing task ID
When the user requests a summary
Then the system returns HTTP 404
