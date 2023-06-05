from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    name: str


class UserUpdate(BaseModel):
    username: str | None
    password: str | None
    name: str | None
