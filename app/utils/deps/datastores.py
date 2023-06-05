from app.datastores.todo_store import TodoStore

todo_store: TodoStore | None = None


def get_todo_store() -> TodoStore:
    global todo_store
    if todo_store is None:
        todo_store = TodoStore()
    return todo_store
