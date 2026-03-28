from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from .project import Project


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="user", init=False)
