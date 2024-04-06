import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Project(Base):
    __tablename__ = "projects"

    name = Column(String, nullable=False)
    alias = Column(String, nullable=True)
