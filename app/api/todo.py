from fastapi import Depends, Query, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from typing import Annotated
from uuid import UUID
from app.utils.deps.datastores import get_todo_store
from app.schemas.response import Response
from app.datastores.todo_store import TodoStore, TodoNotFoundException
from app.schemas.todo import Todo, TodoCreate, TodoUpdate

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_todos(todo_store: Annotated[TodoStore, Depends(get_todo_store)],
              page: Annotated[int, Query(ge=0)] = 0,
              limit: Annotated[int, Query(le=50)] = 10) -> Response[
                  list[Todo]]:
    todos = todo_store.get_todos(page, limit)
    response_todos = list(map(lambda x: Todo.from_model(x), todos))
    return Response(code=status.HTTP_200_OK, status="OK",
                    message="", result=response_todos)


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
def get_single_todo(todo_store: Annotated[
        TodoStore, Depends(get_todo_store)],
        todo_id: UUID) -> Response[Todo]:
    try:
        todo_model = todo_store.get_todo(todo_id)
        todo = Todo.from_model(todo_model)
        return Response(code=status.HTTP_200_OK, status="OK",
                        message="", result=todo)
    except TodoNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(todo_store: Annotated[
                TodoStore, Depends(get_todo_store)],
                todo: TodoCreate) -> Response[Todo]:

    created_todo_model = todo_store.create_todo(todo)
    created_todo = Todo.from_model(created_todo_model)

    return Response(code=status.HTTP_201_CREATED, status="OK",
                    message="", result=created_todo)


@router.patch("/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo(todo_store: Annotated[
                TodoStore, Depends(get_todo_store)],
                todo_id: UUID, todo_update: TodoUpdate) -> Response[Todo]:
    try:
        updated_todo_model = todo_store.update_todo(todo_id, todo_update)
        updated_todo = Todo.from_model(updated_todo_model)
        return Response(code=status.HTTP_200_OK, status="OK",
                        message="", result=updated_todo)
    except TodoNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_store: Annotated[
                TodoStore, Depends(get_todo_store)],
                todo_id: UUID) -> Response[Todo]:
    try:
        deleted_todo_model = todo_store.delete_todo(todo_id)
        deleted_todo = Todo.from_model(deleted_todo_model)
        return Response(code=status.HTTP_200_OK, status="OK",
                        message="", result=deleted_todo)
    except TodoNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
