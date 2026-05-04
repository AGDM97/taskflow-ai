# Feature: Create Task

## Goal
Allow a user to create a task.

## Business Rules
1. Task title is required.
2. Task title must have at least 3 characters.
3. Task description is optional.
4. Task status must start as TODO.
5. Task priority is optional.
6. If priority is not provided, it must default to MEDIUM.
7. The system must generate a unique task ID.
8. The system must return the created task.

## Acceptance Criteria

### Scenario 1: Create valid task
Given a valid task title
When the user creates a task
Then the system creates the task
And returns status TODO
And returns priority MEDIUM
And returns a unique ID

### Scenario 2: Invalid empty title
Given an empty title
When the user creates a task
Then the system rejects the request

### Scenario 3: Invalid short title
Given a title shorter than 3 characters
When the user creates a task
Then the system rejects the request
