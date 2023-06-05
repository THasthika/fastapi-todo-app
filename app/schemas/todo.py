from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.todo import TodoModel


class Todo(BaseModel):
    id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(todo_model: TodoModel) -> 'Todo':
        return Todo(
            id=todo_model.id,
            title=todo_model.title,
            description=todo_model.description,
            completed=todo_model.completed,
            created_at=todo_model.created_at,
            updated_at=todo_model.updated_at
        )


class TodoCreate(BaseModel):
    title: str
    description: str = ""


class TodoUpdate(BaseModel):
    title: str | None
    description: str | None
    completed: bool | None
