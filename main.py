from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import initialize_database
from repository import SQLiteTaskRepository, TaskRepository


initialize_database()

task_repository: TaskRepository = SQLiteTaskRepository()


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
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
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
    return task_repository.get_all_tasks()


# GET ONE TASK
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = task_repository.get_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return task


# CREATE TASK
@app.post("/tasks")
def create_task(payload: TaskCreate):
    title = payload.title

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    task = task_repository.create_task(title.strip())

    return JSONResponse(
        status_code=201,
        content=task
    )


# UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
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

        updates["title"] = title.strip()

    if "done" in updates:
        done = updates["done"]

        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"}
            )

    task = task_repository.update_task(task_id, updates)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return task


# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = task_repository.delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return Response(status_code=204)
