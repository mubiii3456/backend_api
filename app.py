import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

# Agar .env load na ho paye toh default string use ho jaye
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:dev@localhost:5433/tasks"

app = FastAPI()

def get_db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            conn.commit()

            cursor.execute("SELECT COUNT(*) FROM tasks")
            count = cursor.fetchone()["count"]

            if count == 0:
                cursor.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    [
                        ("Learn FastAPI", True),
                        ("Connect Postgres DB", False),
                        ("Submit Week 3 Assignment", False)
                    ]
                )
                conn.commit()

init_db()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.get("/")
def home():
    return {"message": "Database CRUD API is running!"}

@app.get("/tasks")
def get_all_tasks():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks ORDER BY id ASC")
            return cursor.fetchall()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Task not found")
            return row

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
                (task.title, False)
            )
            new_task = cursor.fetchone()
            conn.commit()
            return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
                (task.title, task.done, task_id)
            )
            updated_task = cursor.fetchone()
            conn.commit()

            if updated_task is None:
                raise HTTPException(status_code=404, detail="Task not found")

            return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
            deleted_row = cursor.fetchone()
            conn.commit()

            if deleted_row is None:
                raise HTTPException(status_code=404, detail="Task not found")

            return None