from sqlalchemy import Boolean, Column, Integer, String

from src.data.models import Base


class User(Base):
    """Пользователь."""

    __tablename__: str = "users"

    password = Column(type_=String, nullable=False)
    fullname = Column(type_=String, nullable=False)
    email = Column(type_=String, nullable=False)
    age = Column(type_=Integer, nullable=False)
    is_admin = Column(type_=Boolean, default=False)
    is_verify = Column(type_=Boolean, default=False)
