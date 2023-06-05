from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserModel:
    id: UUID
    username: str
    password: str
    name: str
    created_at: datetime
    updated_at: datetime
