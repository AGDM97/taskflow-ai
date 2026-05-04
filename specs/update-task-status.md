# Feature: Update Task Status

## Goal
Allow a user to update the status of an existing task.

## Business Rules
1. The task ID is required.
2. The task must exist.
3. The new status is required.
4. The new status must be one of: TODO, IN_PROGRESS, DONE, BLOCKED.
5. If the task does not exist, return HTTP 404.
6. The system must return the updated task.

## Acceptance Criteria

### Scenario 1: Update task status successfully
Given an existing task
When the user updates the status to IN_PROGRESS
Then the system returns HTTP 200
And the task status is IN_PROGRESS

### Scenario 2: Task not found
Given a non-existing task ID
When the user tries to update the status
Then the system returns HTTP 404

### Scenario 3: Invalid status
Given an existing task
When the user sends an invalid status
Then the system rejects the request
