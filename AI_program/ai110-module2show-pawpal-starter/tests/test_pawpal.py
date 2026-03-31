import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion_updates_status():
    task = Task(description="Test", pet_name="Bella", due_time="10:00")
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_task_addition_increases_count():
    pet = Pet(name="Bella")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Walk", pet_name="Bella", due_time="08:00"))
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Atai")
    pet = Pet(name="Bella")
    owner.add_pet(pet)
    pet.add_task(Task(description="Late", pet_name="Bella", due_time="19:00"))
    pet.add_task(Task(description="Early", pet_name="Bella", due_time="07:30"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].description == "Early"
    assert sorted_tasks[1].description == "Late"


def test_recurring_task_creates_new_instance_after_completion():
    owner = Owner(name="Atai")
    pet = Pet(name="Bella")
    owner.add_pet(pet)

    task = Task(description="Daily walk", pet_name="Bella", due_time="07:00", frequency="daily")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    new_task = scheduler.mark_task_complete(task)

    assert task.completed
    assert new_task is not None
    assert new_task.frequency == "daily"
    assert new_task.completed is False


def test_conflict_detection_finds_duplicate_times():
    owner = Owner(name="Atai")
    pet1 = Pet(name="Bella")
    pet2 = Pet(name="Leo")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    pet1.add_task(Task(description="Feed", pet_name="Bella", due_time="08:00"))
    pet2.add_task(Task(description="Pill", pet_name="Leo", due_time="08:00"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 2
