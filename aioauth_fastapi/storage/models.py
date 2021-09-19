import uuid

from pydantic.types import UUID4
from sqlmodel import Field, SQLModel


class BaseTable(SQLModel):
    id: UUID4 = Field(
        primary_key=True,
        default=uuid.uuid4(),
        nullable=False,
        index=True,
        sa_column_kwargs={"unique": True},
    )
