from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlmodel import Session, select

from src.core.db import engine
from src.models.users import User

api_key_header = APIKeyHeader(name="SERVICE-NAME-API-KEY", auto_error=False)


def get_session():
    with Session(engine) as session:
        yield session


async def verify_api_key(
    api_key: Annotated[str | None, Depends(api_key_header)],
    session: Session = Depends(get_session),
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    user = session.exec(select(User).where(User.api_key == api_key)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return user


CurrentUser = Annotated[User, Depends(verify_api_key)]
DBSessionDep = Annotated[Session, Depends(get_session)]
