from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(tasks):
    if not tasks:
        print("No tasks scheduled.")
        return

    print("Today's schedule:")
    print("Time  | Pet   | Task description | Frequency | Completed")
    print("----- | ----- | ---------------- | --------- | --------- ")
    for task in tasks:
        print(f"{task.due_time:5} | {task.pet_name:5} | {task.description:16} | {task.frequency:9} | {task.completed}")


def run_demo():
    owner = Owner(name="Atai")
    bella = Pet(name="Bella", species="dog")
    leo = Pet(name="Leo", species="cat")

    owner.add_pet(bella)
    owner.add_pet(leo)

    t1 = Task(description="Morning walk", pet_name="Bella", due_time="08:00", frequency="daily")
    t2 = Task(description="Feed breakfast", pet_name="Leo", due_time="09:00", frequency="daily")
    t3 = Task(description="Vet appointment", pet_name="Bella", due_time="14:30", frequency="once")
    t4 = Task(description="Pill", pet_name="Leo", due_time="20:00", frequency="daily")

    bella.add_task(t1)
    bella.add_task(t3)
    leo.add_task(t2)
    leo.add_task(t4)

    scheduler = Scheduler(owner)

    all_tasks = scheduler.sort_by_time()
    print_schedule(all_tasks)

    print("\nMarking first task complete and generating recurrence")
    scheduler.mark_task_complete(t1)

    print_schedule(scheduler.sort_by_time())

    conflicts = scheduler.detect_conflicts()
    print(f"\nConflicts: {conflicts}")

    filtered = scheduler.filter_tasks(completed=False)
    print("\nPending tasks: ")
    print_schedule(filtered)


if __name__ == "__main__":
    run_demo()
