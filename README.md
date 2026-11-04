# To-Do List App

A clean, responsive task management web app built with Flask and SQLite.

## Features
- Create tasks with title and category (General, Work, Personal, Urgent)
- Mark tasks complete / incomplete
- Delete tasks
- Filter by status (All / Active / Done) and category
- Persistent SQLite storage

## Running locally
```bash
pip install -r requirements.txt
python app.py
```

## Health check
`GET /health` -> `{"status": "ok"}`
