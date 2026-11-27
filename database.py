from pathlib import Path
import os
import sqlite3


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///" + str(Path(__file__).resolve().parent / "tasks.db")
)

if not DATABASE_URL.startswith("sqlite:///"):
    raise ValueError("DATABASE_URL must use sqlite:///")

DATABASE_PATH = Path(DATABASE_URL[len("sqlite:///"):])
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    try:
        sql_file = Path(__file__).resolve().parent / "init.sql"
        sql_script = sql_file.read_text(encoding="utf-8-sig")

        connection.executescript(sql_script)

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
