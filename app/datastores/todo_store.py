from uuid import uuid4, UUID
from threading import Lock
from datetime import datetime
from app.models.todo import TodoModel
from app.utils.meta import SingletonMeta
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoStore(metaclass=SingletonMeta):
    """Manages the todo lists in-memory for now
    """

    _todos: list[TodoModel]
    _lock: Lock

    def __init__(self) -> None:

        self._todos = []
        self._lock = Lock()

    def create_todo(self, todo_create: TodoCreate):
        with self._lock:
            todo = TodoModel(id=uuid4(),
                             title=todo_create.title,
                             description=todo_create.description,
                             completed=False,
                             created_at=datetime.now(),
                             updated_at=datetime.now())
            self._todos.append(todo)
            return todo

    def get_todo(self, id: UUID):
        for todo in self._todos:
            if todo.id == id:
                return todo
        raise TodoNotFoundException()

    def get_todos(self, page: int, limit: int = 10):
        limit = min(limit, 50)
        offset = page * limit

        if len(self._todos) <= offset:
            return []

        todos = self._todos[offset:offset+limit]
        return todos

    def update_todo(self, id: UUID, todo_update: TodoUpdate) -> TodoModel:
        with self._lock:
            todo_index = 0
            todo = None
            for i in range(len(self._todos)):
                if id == self._todos[i].id:
                    todo = self._todos[i]
                    todo_index = i

            if todo is None:
                raise TodoNotFoundException()

            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.description is not None:
                todo.description = todo_update.description
            if todo_update.completed is not None:
                todo.completed = todo_update.completed
            todo.updated_at = datetime.now()

            self._todos[todo_index] = todo

            return todo

    def delete_todo(self, id: UUID):
        with self._lock:
            todo_index = 0
            todo = None
            for i in range(len(self._todos)):
                if id == self._todos[i].id:
                    todo = self._todos[i]
                    todo_index = i

            if todo is None:
                raise TodoNotFoundException()

            return self._todos.pop(todo_index)


class TodoNotFoundException(Exception):
    pass
