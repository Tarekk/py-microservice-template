from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field

from api.models.shared.mixins import PKMixin, TimestampMixin


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
