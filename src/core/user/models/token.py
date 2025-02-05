import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.commons.model import Base
from src.core.user.models.user import UserModel


class RefreshTokenModel(Base):
    __tablename__ = 'refresh_token'
    refresh_token: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(UserModel.user_id, ondelete="CASCADE"))
