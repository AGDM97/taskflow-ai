# Feature: Break Task into Subtasks

## Goal
Allow a user to break a complex task into smaller actionable subtasks using an LLM.

## Business Rules
1. The task ID is required.
2. The task must exist.
3. The system must generate between 3 and 7 subtasks.
4. Each subtask must have a title.
5. Each subtask must have a description.
6. Each subtask must have a suggested priority.
7. Suggested priority must be one of: LOW, MEDIUM, HIGH, CRITICAL.
8. The system must return the task ID and the generated subtasks.
9. If the task does not exist, return HTTP 404.
10. The system must not automatically persist generated subtasks yet.

## Acceptance Criteria

### Scenario 1: Break existing task into subtasks
Given an existing task
When the user requests a breakdown
Then the system returns HTTP 200
And returns between 3 and 7 subtasks
And each subtask has title, description and priority

### Scenario 2: Task not found
Given a non-existing task ID
When the user requests a breakdown
Then the system returns HTTP 404

### Scenario 3: Invalid LLM output
Given an existing task
When the LLM returns invalid output
Then the system returns a controlled error
