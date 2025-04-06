from sqlmodel import Session, create_engine, select

from api.core.config import settings
from api.models.users import User, UserCreate

engine = create_engine(str(settings.SQLITE_URL))


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(user_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.api_key == settings.DEFAULT_API_KEY)
    ).first()
    if not user:
        user_in = UserCreate(
            api_key=settings.DEFAULT_API_KEY,
            name=settings.DEFAULT_API_USER,
            description=settings.DEFAULT_API_DESCRIPTION,
        )
        user = create_user(session=session, user_create=user_in)
