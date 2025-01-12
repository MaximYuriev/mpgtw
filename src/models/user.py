import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..models.base import Base


class RoleModel(Base):
    __tablename__ = "role"
    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str]


class UserModel(Base):
    __tablename__ = "user"
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    role_id: Mapped[int] = mapped_column(ForeignKey(RoleModel.role_id), default=1)  # Роль "пользователь"
    login: Mapped[str]
    password: Mapped[str]

    role: Mapped["RoleModel"] = relationship()