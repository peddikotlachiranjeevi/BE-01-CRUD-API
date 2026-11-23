# Task API — FastAPI CRUD Project

A simple REST API built using **Python** and **FastAPI** to create, read, update, and delete tasks.

## Features

- Get all tasks.
- Get a single task by ID.
- Create a new task.
- Update a task's title or completion status.
- Delete a task.
- Validate request data.
- Return appropriate HTTP status codes.
- Interactive API documentation using Swagger UI.

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Git

## Project Structure

```text
BE-01-CRUD-API/
│
├── .venv/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── swagger-screenshot.png
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd BE-01-CRUD-API
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the API

```bash
python -m uvicorn main:app --reload --port 8000
```

The API will run at:

`http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| GET    | `/`                | API information |
| GET    | `/health`          | Health check    |
| GET    | `/tasks`           | Get all tasks   |
| GET    | `/tasks/{task_id}` | Get one task    |
| POST   | `/tasks`           | Create a task   |
| PUT    | `/tasks/{task_id}` | Update a task   |
| DELETE | `/tasks/{task_id}` | Delete a task   |

## Example Requests

### Create a task

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Buy milk\"}"
```

Expected status: `201 Created`

### Get all tasks

```bash
curl -i http://127.0.0.1:8000/tasks
```

Expected status: `200 OK`

### Get one task

```bash
curl -i http://127.0.0.1:8000/tasks/1
```

Expected status: `200 OK`

### Update a task

```bash
curl -i -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn Advanced Python\",\"done\":true}"
```

Expected status: `200 OK`

### Delete a task

```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/1
```

Expected status: `204 No Content`

## HTTP Status Codes

| Status | Meaning                   |
| ------ | ------------------------- |
| 200    | Request successful        |
| 201    | Task created successfully |
| 204    | Task deleted successfully |
| 400    | Invalid request data      |
| 404    | Task not found            |

## Swagger API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open:

`http://127.0.0.1:8000/docs`

Use the **Try it out** feature to test all API endpoints directly from your browser.

### Swagger Screenshot

(<Screenshot 2026-11-20 003818.png>)

![Task API Swagger Documentation](swagger-screenshot.png)

## Data Storage

This project currently uses an in-memory Python list to store tasks. Data is temporary and resets when the server restarts.

## Learning Outcomes

- Understanding REST API fundamentals.
- Creating API endpoints with FastAPI.
- Working with GET, POST, PUT, and DELETE methods.
- Validating request data with Pydantic.
- Handling HTTP errors and status codes.
- Testing APIs using Swagger UI.
- Managing project versions with Git.

## Author

**Chiranjeevi**

Backend AI Engineering — BE-01: Build Your First CRUD API

## Stage 7 - AI Rematch

Created a separate AI-assisted implementation inside the `ai-rematch` folder.

### AI Rematch Testing

The following operations were tested successfully:

| Operation | Expected Result |
|---|---|
| GET all tasks | 200 OK |
| POST create task | 201 Created |
| PUT update task | 200 OK |
| DELETE task | 204 No Content |
| GET unknown task | 404 Not Found |
| Invalid title | 400 Bad Request |
| Invalid done value | 400 Bad Request |

### Three Differences Between Original and AI Versions

1. **Validation:** The original version uses `Any` fields and manual type checking. The AI version uses `StrictStr`, `StrictBool`, and Pydantic field validation.

2. **Task ID generation:** The original calculates the next ID using the maximum existing ID. The AI version uses a separate `next_task_id` counter.

3. **Task lookup:** The original uses a `for` loop to find tasks. The AI version uses `next()` with a generator expression.

### Files

- `ai-rematch/main.py` - AI-assisted implementation.
- `ai-rematch/requirements.txt` - Dependencies.
- `ai-rematch/AI_PROMPT.md` - Prompt used for the alternative implementation.

### Learning Outcome

Compared two implementations of the same CRUD API and learned about Pydantic validation, ID generation, and Python task lookup techniques.

## BE-02 - Connecting to SQLite Database

### Overview
The Task API now uses SQLite instead of temporary in-memory storage.

### Why SQLite?
SQLite is lightweight, stores data in a single file, and does not require a separate database server.

### Database Details
- Database file: tasks.db
- Table: tasks
- Columns: id, title, done
- Database library: Python built-in sqlite3
- Database location: Project root folder

The database and table are created automatically when the application starts. Three example tasks are inserted only when the table is empty.

### How to Run

1. Clone this repository.
2. Create a virtual environment:

   python -m venv .venv

3. Activate it:

   .venv\Scripts\Activate.ps1

4. Install dependencies:

   python -m pip install -r requirements.txt

5. Start the application:

   python -m uvicorn main:app --reload --port 8000

The tasks.db file is created automatically.

### Example SQL Queries

List all tasks:

    SELECT * FROM tasks;

Show completed tasks:

    SELECT * FROM tasks WHERE done = 1;

Count all tasks:

    SELECT COUNT(*) FROM tasks;

### Database Screenshot

See database-screenshot.png for the tasks table opened in DB Browser for SQLite.

### Completed BE-02 Stages

- Stage 0: Create SQLite database
- Stage 1: Database read endpoints
- Stage 2: Insert tasks into database
- Stage 3: Update and delete using SQL
- Stage 4: Explored SQLite queries
- Stage 5: Database documentation
