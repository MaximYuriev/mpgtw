from pydantic import BaseModel

from .user import BaseUserSchema, UserInfoSchema


class BaseResponse(BaseModel):
    detail: str
    data: str | None = None


class UserResponse(BaseResponse):
    data: UserInfoSchema
