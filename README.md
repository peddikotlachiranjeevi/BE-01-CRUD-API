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

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

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

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Task created successfully |
| 204 | Task deleted successfully |
| 400 | Invalid request data |
| 404 | Task not found |

## Swagger API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open:

`http://127.0.0.1:8000/docs`

Use the **Try it out** feature to test all API endpoints directly from your browser.

### Swagger Screenshot

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