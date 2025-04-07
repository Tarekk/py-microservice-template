from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Relationship

from src.models.shared.mixins import PKMixin, TimestampMixin

if TYPE_CHECKING:
    from src.models.tasks import Task


class UserBase(BaseModel):
    api_key: str
    name: Optional[str] = None
    description: Optional[str] = None


class User(TimestampMixin, PKMixin, UserBase, table=True):
    __tablename__: str = "users"
    tasks: List["Task"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    api_key: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class UserPublic(UserBase, PKMixin, TimestampMixin):
    pass


class UsersPublic(BaseModel):
    data: List[UserPublic]
    count: int
