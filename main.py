
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    version="1.0"
)


# Request body model for creating tasks
class TaskCreate(BaseModel):
    title: Any = None


# Return HTTP 400 for invalid request bodies
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


# In-memory task list
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


@app.get("/health", description="Check API health")
def health():
    return {"status": "ok"}


@app.get("/tasks", description="Get all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", description="Get one task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


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

    return JSONResponse(
        status_code=201,
        content=new_task
    )
