from sqlalchemy import Column, DateTime, Boolean,\
    String, UUID, func
# from sqlalchemy.orm import relationship
from app.database.base import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUID, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean)
    # user_id = Column(UUID, ForeignKey("users.id"))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # owner = relationship("User", back_populates="todos")