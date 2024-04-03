import uuid

from sqlalchemy import UUID, Column
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    """Базовая модель."""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
