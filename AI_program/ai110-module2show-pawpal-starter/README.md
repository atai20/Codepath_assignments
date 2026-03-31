# PawPal+ (ai110-module2show-pawpal-starter)

A smart pet-care scheduling app built with Python OOP. Includes:
- Task management (add, complete, recurring)
- Pet and owner relationships
- Scheduler: sort, filter, conflict detection
- CLI demo + Streamlit integration
- Automated tests with pytest

## Run

```bash
cd ai110-module2show-pawpal-starter
pip install -r requirements.txt  # optional for streamlit (streamlit==1.29.0)
python main.py
```

## Tests

```bash
python -m pytest -q
```

## Features

- Owner, Pet, Task, Scheduler classes in `pawpal_system.py`
- Task recurrence (daily/weekly)
- Task completion tracking
- Sorting by due time
- Filtering by completion/pet name
- Basic conflict detection for same-due-time tasks

## Overview

CLI demo is in `main.py`. Streamlit UI is in `app.py` (optional to run).

```bash
streamlit run app.py
```

## Reflection
See `reflection.md` for AI/human design notes.
