from fastapi import FastAPI
from app.routes.todo import router as todo_router

api_app = FastAPI()


@api_app.get('/ping')
def health_check():
    return {"status": "ok"}


api_app.include_router(todo_router, prefix="/todos")
