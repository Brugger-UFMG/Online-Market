from typing import TYPE_CHECKING

from orders.interfaces import I_Order_Service
from orders import Order

if TYPE_CHECKING:
    from users import Owner, Customer
    from products import Product


class Order_Manager(I_Order_Service):
    def __init__(self, owner: "Owner", orders: dict[Order.id, Order] = dict()) -> None:
        """
        Gerenciador de Pedidos.

        Parameters
        ----------
        owner : Owner
            Dono
        orders : dict[Order.id, Order], optional
            Pedidos, by default dict()
        """
        self.__owner = owner
        self._orders = orders

    def __generate_id(self) -> int:
        return len(self._orders)

    def place_order(self, customer: "Customer", products: list["Product"]) -> Order:
        """
        Faz um pedido.

        Parameters
        ----------
        customer : Customer
            Cliente
        products : list[&quot;Product&quot;]
            Produtos

        Returns
        -------
        Order
            Pedido realizado

        Raises
        ------
        ValueError
            A lista deve conter produtos
        """
        if len(products) < 1:
            raise ValueError("Lista de produtos vazia!")
        else:
            order_id = self.__generate_id()
            order = Order(order_id, customer, products)
            self._orders[order_id] = order
            customer.orders.append(order)
            return order

    def cancel_order(self, order_id: int) -> bool:
        """
        Tenta cancelar um pedido.

        Parameters
        ----------
        order_id : int
            Id do pedido

        Returns
        -------
        bool
            Se o pedido foi cancelado com sucesso

        Raises
        ------
        KeyError
            Caso o pedido não exista
        """
        if order_id not in self._orders.keys():
            raise KeyError("Pedido inexistente!")
        else:
            return self._orders[order_id].cancel()

    def send_order(self, order_id: int) -> None:
        """
        Envia um pedido.

        Parameters
        ----------
        order_id : int
            Id do pedido

        Raises
        ------
        KeyError
            Caso o pedido não exista
        """
        if order_id not in self._orders.keys():
            raise KeyError("Pedido inexistente!")
        else:
            self._orders[order_id].send()

    def receive_order(self, order_id: int) -> None:
        """
        Confirma o recebimento de um pedido.

        Parameters
        ----------
        order_id : int
            Id do pedido

        Raises
        ------
        KeyError
            Caso o pedido não exista
        """
        if order_id not in self._orders.keys():
            raise KeyError("Pedido inexistente!")
        else:
            self._orders[order_id].receive()

    def list_orders(self) -> list[Order]:
        return list(self._orders)

    @property
    def owner(self) -> "Owner":
        return self.__owner

    @property
    def orders(self) -> dict[Order.id, Order]:
        return self._orders

    def __repr__(self) -> str:
        return f"Order_Manager(contem {len(self._orders)} pedidos)"
