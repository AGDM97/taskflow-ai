# Feature: Get Task by ID

## Goal
Allow a user to retrieve a specific task by its ID.

## Business Rules
1. The task ID is required.
2. If the task exists, the system must return it.
3. If the task does not exist, the system must return HTTP 404.
4. The error response must include a clear message.

## Acceptance Criteria

### Scenario 1: Existing task
Given an existing task
When the user requests the task by ID
Then the system returns HTTP 200
And returns the task data

### Scenario 2: Task not found
Given a non-existing task ID
When the user requests the task by ID
Then the system returns HTTP 404
And returns an error message
