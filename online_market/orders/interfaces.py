from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product
    from users import Customer
    from orders import Order


class I_Order_Service(ABC):
    @abstractmethod
    def place_order(self, customer: "Customer", products: "list[Product]") -> "Order":
        pass

    @abstractmethod
    def cancel_order(self, order_id: int) -> bool:
        pass

    @abstractmethod
    def send_order(self, order_id: int) -> None:
        pass

    @abstractmethod
    def receive_order(self, order_id: int) -> None:
        pass
