from fastapi import FastAPI, Depends, Query, status
from pydantic import BaseModel
from pydantic.generics import GenericModel
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Annotated, TypeVar, Generic, Optional
from fastapi.exceptions import HTTPException

T = TypeVar('T')


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]


class TodoModel(BaseModel):
    id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class TodoCreate(BaseModel):
    title: str
    description: str = ""


class TodoUpdate(BaseModel):
    title: str | None
    description: str | None
    completed: bool | None


class TodoManager():

    def __init__(self):
        self.todos: List[TodoModel] = []

    def create_todo(self, title: str, description: str):
        todo = TodoModel(id=uuid4(), title=title, description=description,
                         completed=False,
                         created_at=datetime.now(),
                         updated_at=datetime.now())
        self.todos.append(todo)
        return todo

    def get_todo(self, id: UUID):
        for todo in self.todos:
            if todo.id == id:
                return todo
        return None

    def get_todos(self, page: int, limit: int = 10):
        limit = min(limit, 50)
        offset = page * limit

        if len(self.todos) <= offset:
            return []

        todos = self.todos[offset:offset+limit]
        return todos

    def update_todo(self, id: UUID, todo_update: TodoUpdate) -> TodoModel:
        todo_index = 0
        todo = None
        for i in range(len(self.todos)):
            if id == self.todos[i].id:
                todo = self.todos[i]
                todo_index = i

        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

        if todo_update.title is not None:
            todo.title = todo_update.title
        if todo_update.description is not None:
            todo.description = todo_update.description
        if todo_update.completed is not None:
            todo.completed = todo_update.completed
        todo.updated_at = datetime.now()

        self.todos[todo_index] = todo

        return todo

    def delete_todo(self, id: UUID):
        todo_index = 0
        todo = None
        for i in range(len(self.todos)):
            if id == self.todos[i].id:
                todo = self.todos[i]
                todo_index = i

        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

        return self.todos.pop(todo_index)


todo_manager: TodoManager | None = None


def get_todo_manager() -> TodoManager:
    global todo_manager
    if todo_manager is None:
        todo_manager = TodoManager()
    return todo_manager


app = FastAPI()


@app.get('/ping')
def health_check():
    return {"status": "ok"}


@app.get("/todos", status_code=status.HTTP_200_OK)
def get_todos(todo_manager: Annotated[TodoManager, Depends(get_todo_manager)],
              page: Annotated[int, Query(ge=0)] = 0,
              limit: Annotated[int, Query(le=50)] = 10) -> Response[
                  List[TodoModel]]:

    todos = todo_manager.get_todos(page, limit)
    return Response(code=status.HTTP_200_OK, status="OK",
                    message="", result=todos)


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def get_single_todo(todo_manager: Annotated[
        TodoManager, Depends(get_todo_manager)],
        todo_id: UUID) -> Response[TodoModel]:
    todo = todo_manager.get_todo(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    return Response(code=status.HTTP_200_OK, status="OK",
                    message="", result=todo)


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo_manager: Annotated[
                TodoManager, Depends(get_todo_manager)],
                todo: TodoCreate) -> Response[TodoModel]:

    created_todo = todo_manager.create_todo(todo.title, todo.description)

    return Response(code=status.HTTP_201_CREATED, status="OK",
                    message="", result=created_todo)


@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo(todo_manager: Annotated[
                TodoManager, Depends(get_todo_manager)],
                todo_id: UUID, todo_update: TodoUpdate):
    updated_todo = todo_manager.update_todo(todo_id, todo_update)
    return Response(code=status.HTTP_200_OK, status="OK",
                    message="", result=updated_todo)


@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_manager: Annotated[
                TodoManager, Depends(get_todo_manager)],
                todo_id: UUID):
    deleted_todo = todo_manager.delete_todo(todo_id)
    return Response(code=status.HTTP_200_OK, status="OK",
                    message="", result=deleted_todo)
