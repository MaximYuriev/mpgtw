from pydantic import BaseModel, Field


class PaginationQueryParams(BaseModel):
    pn: int = Field(default=1, ge=1, description="Page number", serialization_alias="page_number")
    ps: int = Field(default=5, ge=1, description="Page size", serialization_alias="page_size")
