from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# Create the FastAPI application
app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API built with Python and FastAPI."
)


# Request models
class TaskCreate(BaseModel):
    title: Any = None


class TaskUpdate(BaseModel):
    title: Any = None
    done: Any = None


# Return a simple error when the request body is invalid
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


# Temporary in-memory task storage
tasks = [
    {"id": 1, "title": "Learn Python", "done": True},
    {"id": 2, "title": "Build my first API", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": False}
]


# ROOT ENDPOINT
@app.get("/", description="Get information about the Task API")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# HEALTH CHECK
@app.get("/health", description="Check whether the API is running")
def health():
    return {"status": "ok"}


# GET ALL TASKS
@app.get("/tasks", description="Get all tasks")
def get_tasks():
    return tasks


# GET ONE TASK
@app.get("/tasks/{task_id}", description="Get one task using its ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


# CREATE A NEW TASK
@app.post("/tasks", description="Create a new task")
def create_task(payload: TaskCreate):
    title = payload.title

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_task = {
        "id": max(
            (task["id"] for task in tasks),
            default=0
        ) + 1,
        "title": title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return JSONResponse(
        status_code=201,
        content=new_task
    )


# UPDATE AN EXISTING TASK
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


# DELETE A TASK
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