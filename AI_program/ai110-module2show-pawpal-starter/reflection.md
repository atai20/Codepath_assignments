# PawPal+ Reflection

## 1a. Initial design
- Core actions: add a pet, schedule a task, view today's tasks.
- Objects: Owner (holds pets), Pet (holds tasks), Task (activity with time/frequency), Scheduler (smart query/logic).

## 1b. Design changes
- Added `Task.next_occurrence()` to support recurrence
- Added `Scheduler.detect_conflicts()` and `Scheduler.filter_tasks()` for algorithmic layer

## 2b. Tradeoffs (algorithmic)
- Conflict detection is based on exact `HH:MM` equality, not overlapping durations; this is simpler but misses broader slot overlaps.

## AI strategy
- Used Copilot style prompts to generate class skeleton and then enhanced with logic.
- Chose explicit unit tests over one-liner integration tests for clear correctness.

## Confidence level
★★★★☆ (4/5) - all unit tests pass; can improve with more time range and duration support.
