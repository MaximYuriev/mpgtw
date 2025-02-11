from pydantic import BaseModel


class ProductOnBasketFilterSchema(BaseModel):
    with_products_marked_for_order: bool | None = None
