from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import uuid

from sqlalchemy.orm import declarative_base

Base = declarative_base()  # type: ignore


class BaseTable(Base):  # type: ignore
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
