from pydantic import field_serializer

from src.api.commons.filters import PaginationQueryParams
from src.api.product.utils.category import Category


class PaginationQueryParamsWithCategory(PaginationQueryParams):
    category: Category | None = None

    @field_serializer('category')
    def serialize_dt(self, category: Category):
        if category is not None:
            return category.value
