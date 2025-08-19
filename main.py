from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False

# In-memory "database"
todos: List[TodoItem] = []

# Get all todos
@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return todos

# Add a new todo
@app.post("/todos", response_model=TodoItem)
def add_todo(todo: TodoItem):
    # Check if id already exists
    for t in todos:
        if t.id == todo.id:
            raise HTTPException(status_code=400, detail="ID already exists")
    todos.append(todo)
    return todo

# Update a todo
@app.put("/todos/{id}", response_model=TodoItem)
def update_todo(id: int, updated_todo: TodoItem):
    for index, t in enumerate(todos):
        if t.id == id:
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

# Delete a todo
@app.delete("/todos/{id}")
def delete_todo(id: int):
    for index, t in enumerate(todos):
        if t.id == id:
            todos.pop(index)
            return {"detail": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
