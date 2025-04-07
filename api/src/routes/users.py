import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from src.deps import CurrentUser, DBSessionDep
from src.models.shared.common import Message
from src.models.users import User, UserCreate, UserPublic, UsersPublic, UserUpdate

router = APIRouter()


@router.get("", response_model=UsersPublic)
def read_users(
    session: DBSessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    users_public = [UserPublic.model_validate(user) for user in users]
    return UsersPublic(data=users_public, count=count)


@router.get("/{id}", response_model=UserPublic)
def read_user(
    id: uuid.UUID,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Get user by ID.
    """
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.model_validate(user)


@router.post("", response_model=UserPublic)
def create_user(
    *,
    user_in: UserCreate,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Create new user.
    """
    user = User.model_validate(user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserPublic.model_validate(user)


@router.put("/{id}", response_model=UserPublic)
def update_user(
    *,
    id: uuid.UUID,
    user_in: UserUpdate,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Update a user.
    """
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = user_in.model_dump(exclude_unset=True)
    user.sqlmodel_update(update_dict)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserPublic.model_validate(user)


@router.delete("/{id}")
def delete_user(
    id: uuid.UUID,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Message:
    """
    Delete a user.
    """
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
