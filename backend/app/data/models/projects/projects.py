from sqlalchemy import Column, String

from app.data.models import Base


class Project(Base):
    """Проект."""

    __tablename__ = "project"

    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
