from typing import List, Optional

from pydantic import BaseModel

from api.models.shared.mixins import PKMixin, TimestampMixin


class UserBase(BaseModel):
    api_key: str
    name: Optional[str] = None
    description: Optional[str] = None


class User(TimestampMixin, PKMixin, UserBase, table=True):
    __tablename__: str = "users"


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
