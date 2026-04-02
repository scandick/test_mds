from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI(title="Pet API")

class TaskIn(BaseModel):
    title: str = Field(min_length=3, max_length=100)

class TaskOut(TaskIn):
    id: int
    done: bool = False

db: Dict[int, TaskOut] = {}
counter = 1

# создание задачи
@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskIn):
    global counter
    new_task = TaskOut(id=counter, title=task.title, done=False)
    db[counter] = new_task
    counter += 1
    return new_task

# получение задачи по id
@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    task = db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# обновление задачи (установка флага done в True)
@app.patch("/tasks/{task_id}/done", response_model=TaskOut)
def mark_done(task_id: int):
    task = db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = True
    db[task_id] = task
    return task
