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


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# GET ALL TASKS
@app.get("/tasks")
def get_tasks():
    connection = get_db_connection()
    try:
        rows = connection.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()
        return [convert_task(row) for row in rows]
    finally:
        connection.close()


# GET ONE TASK
@app.get("/tasks/{task_id}")
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


# CREATE TASK
@app.post("/tasks")
def create_task(payload: TaskCreate):
    title = payload.title

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    connection = get_db_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (title.strip(), 0)
        )
        connection.commit()

        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return JSONResponse(
            status_code=201,
            content=convert_task(row)
        )
    finally:
        connection.close()


# STAGE 3: UPDATE TASK USING SQL
@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    values = []
    sql_parts = []

    if "title" in updates:
        title = updates["title"]

        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        sql_parts.append("title = ?")
        values.append(title.strip())

    if "done" in updates:
        done = updates["done"]

        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"}
            )

        sql_parts.append("done = ?")
        values.append(int(done))

    connection = get_db_connection()

    try:
        existing = connection.execute(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if existing is None:
            return JSONResponse(
                status_code=404,
                content={"error": f"Task {task_id} not found"}
            )

        values.append(task_id)

        connection.execute(
            f"UPDATE tasks SET {', '.join(sql_parts)} WHERE id = ?",
            values
        )
        connection.commit()

        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        return convert_task(row)

    finally:
        connection.close()


# STAGE 3: DELETE TASK USING SQL
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        if cursor.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"error": f"Task {task_id} not found"}
            )

        connection.commit()
        return Response(status_code=204)

    finally:
        connection.close()
