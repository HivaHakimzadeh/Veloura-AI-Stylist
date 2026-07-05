from __future__ import annotations

from app.models.product import Product
from app.repositories.base import Repository


class ProductRepository(Repository[Product]):
    def __init__(self) -> None:
        super().__init__(Product)


product_repository = ProductRepository()

