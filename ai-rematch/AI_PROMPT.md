# AI Rematch Prompt

Build a complete Task CRUD REST API using Python and FastAPI.

Requirements:
1. GET / - Return API information.
2. GET /health - Return API health.
3. GET /tasks - Return all tasks.
4. GET /tasks/{task_id} - Return one task.
5. POST /tasks - Create a task.
6. PUT /tasks/{task_id} - Update title or done status.
7. DELETE /tasks/{task_id} - Delete a task.

Additional requirements:
- Use Pydantic models.
- Validate title and done values.
- Return 400 for invalid data.
- Return 404 for unknown task IDs.
- Return 201 when creating a task.
- Return 204 when deleting a task.
- Use in-memory storage.
- Add Swagger documentation.
- Write clean, readable beginner-friendly code.
