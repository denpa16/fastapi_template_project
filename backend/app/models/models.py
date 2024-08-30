import uuid

from sqlalchemy import UUID, Column, String, Integer, ForeignKey
from sqlalchemy.orm import as_declarative, relationship


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Project(Base):
    __tablename__ = "projects"

    name = Column(String, nullable=False)
    alias = Column(String, nullable=True)
    buildings = relationship("Building", back_populates="project")


class Building(Base):
    __tablename__ = "buildings"

    number = Column(Integer, nullable=False)
    project_id = Column(UUID, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="buildings")

    sections = relationship("Section", back_populates="building")


class Section(Base):
    __tablename__ = "sections"

    number = Column(Integer, nullable=False)
    building_id = Column(UUID, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="sections")
