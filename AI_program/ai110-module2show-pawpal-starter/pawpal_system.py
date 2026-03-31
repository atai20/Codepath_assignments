from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple


@dataclass
class Task:
    description: str
    pet_name: str
    due_time: str  # "HH:MM"
    frequency: str = "once"  # once/daily/weekly
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark task done and optionally compute next recurrence."""
        self.completed = True

    def next_occurrence(self) -> Optional[Task]:
        """Return the next task occurrence for recurring tasks, or None for single tasks."""
        if self.frequency not in {"daily", "weekly"}:
            return None

        current_datetime = datetime.now()
        due_time_obj = datetime.strptime(self.due_time, "%H:%M")
        next_date = current_datetime
        if self.frequency == "daily":
            next_date = current_datetime + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = current_datetime + timedelta(weeks=1)

        next_due = next_date.replace(hour=due_time_obj.hour, minute=due_time_obj.minute, second=0, microsecond=0)
        return Task(
            description=self.description,
            pet_name=self.pet_name,
            due_time=next_due.strftime("%H:%M"),
            frequency=self.frequency,
            completed=False,
        )


@dataclass
class Pet:
    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        if task.pet_name != self.name:
            raise ValueError(f"Task pet_name={{task.pet_name}} does not match Pet name={{self.name}}")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task by reference."""
        self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: Dict[str, Pet] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        if pet.name in self.pets:
            raise ValueError(f"Pet '{pet.name}' already exists")
        self.pets[pet.name] = pet

    def remove_pet(self, name: str) -> None:
        """Remove pet by name."""
        if name in self.pets:
            del self.pets[name]

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return pet by name."""
        return self.pets.get(name)

    def get_all_tasks(self) -> List[Task]:
        """Collect tasks from all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets.values():
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Orchestrates scheduling logic for tasks across pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by due_time ('HH:MM'). Invalid times are placed at the end."""
        tasks = tasks if tasks is not None else self.owner.get_all_tasks()

        def task_sort_key(task: Task):
            try:
                return datetime.strptime(task.due_time, "%H:%M")
            except ValueError:
                return datetime.max

        return sorted(tasks, key=task_sort_key)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        tasks = self.owner.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        return tasks

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[Tuple[str, str, str]]:
        """Return list of conflict warnings (pet_name, time, description)."""
        tasks = tasks if tasks is not None else self.owner.get_all_tasks()
        by_time: Dict[str, List[Task]] = {}
        for task in tasks:
            key = task.due_time
            by_time.setdefault(key, []).append(task)

        conflict: List[Tuple[str, str, str]] = []
        for time, bucket in by_time.items():
            if len(bucket) > 1:
                for t in bucket:
                    conflict.append((t.pet_name, t.due_time, t.description))
        return conflict

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark task completed and return next occurrence if recurring."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task:
            pet = self.owner.get_pet(task.pet_name)
            if pet:
                pet.add_task(next_task)
        return next_task

    def tasks_for_today(self) -> List[Task]:
        """Return tasks that are not completed."""
        return [t for t in self.owner.get_all_tasks() if not t.completed]
