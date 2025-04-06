import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, func


class TimestampMixin(SQLModel):
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now(), "nullable": False},
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            # func.now() = server time, datetime.now() = client time
            "server_default": func.now(),
            "nullable": False,
            "onupdate": func.now(),
        },
    )


class PKMixin:
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
