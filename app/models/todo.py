from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TodoModel:
    id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
