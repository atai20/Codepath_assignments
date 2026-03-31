import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler


def init_owner():
    if "owner" not in st.session_state:
        owner = Owner(name="Atai")
        st.session_state.owner = owner
        st.session_state.scheduler = Scheduler(owner)


def add_pet_form():
    with st.form("add_pet"):
        pet_name = st.text_input("Pet name")
        species = st.text_input("Species", "dog")
        submitted = st.form_submit_button("Add pet")
        if submitted and pet_name:
            owner: Owner = st.session_state.owner
            try:
                owner.add_pet(Pet(name=pet_name, species=species))
                st.success(f"Added pet: {pet_name}")
            except ValueError as e:
                st.error(str(e))


def add_task_form():
    with st.form("add_task"):
        pet_name = st.selectbox("Pet", options=[*st.session_state.owner.pets.keys()])
        description = st.text_input("Task description")
        due_time = st.text_input("Due time (HH:MM)")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        submitted = st.form_submit_button("Add task")
        if submitted and description and due_time and pet_name:
            pet = st.session_state.owner.get_pet(pet_name)
            if pet:
                pet.add_task(Task(description=description, pet_name=pet_name, due_time=due_time, frequency=frequency))
                st.success("Task added")


def run_app():
    st.title("PawPal+ Task Manager")

    init_owner()

    st.header("Add Pet")
    add_pet_form()

    if st.session_state.owner.pets:
        st.header("Add Task")
        add_task_form()

    scheduler: Scheduler = st.session_state.scheduler
    all_tasks = scheduler.sort_by_time()
    st.subheader("All Tasks")
    if all_tasks:
        for task in all_tasks:
            st.write(f"{task.due_time} - {task.pet_name} - {task.description} ({task.frequency}) - {'✓' if task.completed else '⏳'}")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning(f"Conflict: {len(conflicts)} tasks at same time")
        for pet_name, due_time, description in conflicts:
            st.write(f"{due_time}: {pet_name} - {description}")


if __name__ == "__main__":
    run_app()
