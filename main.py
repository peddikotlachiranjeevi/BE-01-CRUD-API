
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Task API",
    version="1.0"
)

# In-memory task list with 3 example tasks
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


@app.get("/health", description="Check API server health")
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
