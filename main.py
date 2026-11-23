from pathlib import Path
import sqlite3
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


DATABASE_PATH = Path(__file__).resolve().parent / "tasks.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
                    CHECK (done IN (0, 1))
            )
        """)

        count = connection.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        if count == 0:
            connection.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Learn Python", 1),
                    ("Build my first API", 0),
                    ("Learn FastAPI", 0)
                ]
            )

        connection.commit()
    finally:
        connection.close()


initialize_database()


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def convert_task(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API built with Python and FastAPI."
)


class TaskCreate(BaseModel):
    title: Any = None


class TaskUpdate(BaseModel):
    title: Any = None
    done: Any = None


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


# Temporary memory storage for write operations.
# POST, PUT and DELETE will use SQLite in Stages 2 and 3.
tasks = [
    {"id": 1, "title": "Learn Python", "done": True},
    {"id": 2, "title": "Build my first API", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": False}
]


@app.get("/", description="Get information about the Task API")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", description="Check whether the API is running")
def health():
    return {"status": "ok"}


# STAGE 1: GET ALL TASKS FROM SQLITE
@app.get("/tasks", description="Get all tasks")
def get_tasks():
    connection = get_db_connection()
    try:
        rows = connection.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()

        return [convert_task(row) for row in rows]
    finally:
        connection.close()


# STAGE 1: GET ONE TASK FROM SQLITE
@app.get("/tasks/{task_id}", description="Get one task using its ID")
def get_task(task_id: int):
    connection = get_db_connection()
    try:
        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if row is None:
            return JSONResponse(
                status_code=404,
                content={"error": f"Task {task_id} not found"}
            )

        return convert_task(row)
    finally:
        connection.close()


# POST: Will be connected to SQLite in Stage 2
@app.post("/tasks", description="Create a new task")
def create_task(payload: TaskCreate):
    title = payload.title

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return JSONResponse(status_code=201, content=new_task)


# PUT: Will be connected to SQLite in Stage 3
@app.put("/tasks/{task_id}", description="Update an existing task")
def update_task(task_id: int, payload: TaskUpdate):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None
    )

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    if "title" in updates:
        title = updates["title"]
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )
        task["title"] = title.strip()

    if "done" in updates:
        done = updates["done"]
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"}
            )
        task["done"] = done

    return task


# DELETE: Will be connected to SQLite in Stage 3
@app.delete("/tasks/{task_id}", description="Delete a task")
def delete_task(task_id: int):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None
    )

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    tasks.remove(task)
    return Response(status_code=204)
