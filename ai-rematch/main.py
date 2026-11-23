from fastapi import FastAPI, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, StrictBool, StrictStr, field_validator

app = FastAPI(title="Task API - AI Rematch", version="2.0")


class TaskCreate(BaseModel):
    title: StrictStr

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


class TaskUpdate(BaseModel):
    title: StrictStr | None = None
    done: StrictBool | None = None


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


tasks = [
    {"id": 1, "title": "Learn Python", "done": True},
    {"id": 2, "title": "Build my first API", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": False}
]

next_task_id = 4


@app.get("/")
def root():
    return {
        "name": "Task API - AI Rematch",
        "version": "2.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next(
        (item for item in tasks if item["id"] == task_id),
        None
    )

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return task


@app.post("/tasks")
def create_task(payload: TaskCreate):
    global next_task_id

    new_task = {
        "id": next_task_id,
        "title": payload.title,
        "done": False
    }

    tasks.append(new_task)
    next_task_id += 1

    return JSONResponse(status_code=201, content=new_task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    task = next(
        (item for item in tasks if item["id"] == task_id),
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

        if title is None or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        task["title"] = title.strip()

    if "done" in updates:
        done = updates["done"]

        if done is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"}
            )

        task["done"] = done

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = next(
        (item for item in tasks if item["id"] == task_id),
        None
    )

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    tasks.remove(task)
    return Response(status_code=204)