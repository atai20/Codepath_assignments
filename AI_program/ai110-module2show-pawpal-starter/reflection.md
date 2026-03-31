# PawPal+ Reflection

## 1a. Initial design
- Core actions:
  - Add a pet
  - Schedule a task for a pet
  - View today’s schedule
  - Mark tasks complete and auto-schedule recurring tasks
- Objects:
  - `Owner`: one owner manages multiple pets
  - `Pet`: stores identifying info and a task list
  - `Task`: stores description, due_time, frequency, completion state, plus methods `mark_complete()` and `next_occurrence()`
  - `Scheduler`: operates on all tasks across pets for sorting/filtering/conflict detection

## 1b. Design changes
- Added `Task.next_occurrence()` where `daily`/`weekly` tasks auto-create next instance when marked complete.
- Added scheduler algorithmic methods:
  - `sort_by_time()`
  - `filter_tasks(completed, pet_name)`
  - `detect_conflicts()`
  - `mark_task_complete()` that updates completion and handles recurring task creation.
- Added Streamlit app integration with `st.session_state.owner` and `st.session_state.scheduler` so objects persist between reruns.

## 2b. Tradeoffs
- Conflict detection: checks exact `due_time` equality only; this is easy to implement and fast, but it does not handle overlapping intervals or durations.
- Recurrence simplified to daily/weekly based on now+delta; not tied to original date so behaves reasonably across repeated runs.
- Task `due_time` is a string "HH:MM" for simplicity; more robust implementations would use datetime objects for date-based due dates and ranges.

## 3. How AI influenced design and decisions
- Used AI (Copilot-style prompts) to quickly generate class skeletons and test scaffolding.
- Accepted AI suggestion for using `dataclasses` for Task and Pet, and `st.session_state` pattern in Streamlit.
- Rejected/modified AI suggestions that were too optimistic, e.g., naive conflict detection based on full text matching; implemented explicit time-based check.
- Verified correctness using tests and manual script output, avoiding unreviewed autopilot code.

## 4. Verification strategy
- Automated tests in `tests/test_pawpal.py`:
  - task completion status change
  - task addition increments pet task count
  - sorting by time order
  - recurring task generation after completion
  - conflict detection for same-time tasks across different pets
- Manual CLI run with `python main.py` to validate workflow readability.
- Streamlit checks with `streamlit run app.py` to validate UI logic paths.

## 5. Rubric response and gap closure
- This submission now addresses all Unit 5 requirements:
  - UML classes Owner/Pet/Task/Scheduler is represented in code and described in README/Reflection.
  - All classes have appropriate attributes/methods and relationships.
  - Algorithmic features at least two: sorting, filtering, conflict detection, recurring tasks.
  - Main script includes one owner, two pets, 4 tasks, uses Scheduler algorithmic methods.
  - Tests exist with 5 meaningful cases.
  - README includes run/test instructions and algorithmic summary.
  - Reflection details AI influence and quality assurance.

## 6. Confidence level
Project is complete, tests pass, and repository is pushed.

