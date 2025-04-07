from enum import Enum
from typing import List, Optional, TYPE_CHECKING
import uuid

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from src.models.shared.mixins import PKMixin, TimestampMixin

if TYPE_CHECKING:
    from src.models.users import User


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TaskBase(BaseModel):
    service_name: Optional[str] = None
    task_name: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)


class Task(TimestampMixin, PKMixin, TaskBase, table=True):
    __tablename__: str = "tasks"
    owner_id: uuid.UUID = Field(
        foreign_key="users.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    service_name: Optional[str] = None
    task_name: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskPublic(TaskBase, PKMixin, TimestampMixin):
    pass


class TasksPublic(BaseModel):
    data: List[TaskPublic]
    count: int
