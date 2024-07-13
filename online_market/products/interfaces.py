from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


class I_Product_Manager(ABC):
    @abstractmethod
    def register_product(self, id: int, name: str, price: float) -> None:
        pass

    @abstractmethod
    def add_product(self, product_id: int, ammount: int) -> None:
        pass

    @abstractmethod
    def remove_product(self, product_id: int, ammount: int) -> None:
        pass

    @abstractmethod
    def get_product(self, product_id: int) -> "Product":
        pass

    @abstractmethod
    def retrieve_product(self, product_id: int, ammount: int) -> "Product":
        pass
