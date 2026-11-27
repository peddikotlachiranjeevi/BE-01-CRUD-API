import sqlite3
from typing import Any, Protocol

from database import get_db_connection


class TaskRepository(Protocol):

    def get_all_tasks(self) -> list[dict[str, Any]]:
        ...

    def get_task(self, task_id: int) -> dict[str, Any] | None:
        ...

    def create_task(self, title: str) -> dict[str, Any]:
        ...

    def update_task(
        self,
        task_id: int,
        updates: dict[str, Any]
    ) -> dict[str, Any] | None:
        ...

    def delete_task(self, task_id: int) -> bool:
        ...


class SQLiteTaskRepository:

    @staticmethod
    def convert_task(row):
        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }

    def get_all_tasks(self):
        connection = get_db_connection()

        try:
            rows = connection.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            ).fetchall()

            return [
                self.convert_task(row)
                for row in rows
            ]

        finally:
            connection.close()

    def get_task(self, task_id: int):
        connection = get_db_connection()

        try:
            row = connection.execute(
                "SELECT id, title, done FROM tasks WHERE id = ?",
                (task_id,)
            ).fetchone()

            if row is None:
                return None

            return self.convert_task(row)

        finally:
            connection.close()

    def create_task(self, title: str):
        connection = get_db_connection()

        try:
            cursor = connection.execute(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                (title, 0)
            )

            connection.commit()

            row = connection.execute(
                "SELECT id, title, done FROM tasks WHERE id = ?",
                (cursor.lastrowid,)
            ).fetchone()

            return self.convert_task(row)

        finally:
            connection.close()

    def update_task(
        self,
        task_id: int,
        updates: dict[str, Any]
    ):
        connection = get_db_connection()

        try:
            sql_parts = []
            values = []

            if "title" in updates:
                sql_parts.append("title = ?")
                values.append(updates["title"])

            if "done" in updates:
                sql_parts.append("done = ?")
                values.append(int(updates["done"]))

            if not sql_parts:
                return None

            values.append(task_id)

            cursor = connection.execute(
                f"UPDATE tasks SET {', '.join(sql_parts)} WHERE id = ?",
                values
            )

            if cursor.rowcount == 0:
                return None

            connection.commit()

            row = connection.execute(
                "SELECT id, title, done FROM tasks WHERE id = ?",
                (task_id,)
            ).fetchone()

            return self.convert_task(row)

        finally:
            connection.close()

    def delete_task(self, task_id: int):
        connection = get_db_connection()

        try:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()
