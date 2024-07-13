from typing import TYPE_CHECKING

from orders import constants as c

if TYPE_CHECKING:
    from users import Customer
    from products import Product


class Order:
    def __init__(
        self,
        id: int,
        customer: "Customer",
        products: list["Product"],
        status: int = c.placed,
    ) -> None:
        """
        Pedido.

        Parameters
        ----------
        id : int
            Identificador
        customer : Customer
            Cliente
        products : list[&quot;Product&quot;]
            Produtos
        status : int, optional
            Status do Pedido, by default c.placed
        """
        self.__id = id
        self.__customer = customer
        self._status = status
        self._products = products

        self._price = 0.0
        for product in self._products:
            self._price += product.get_total_price()

    def cancel(self) -> bool:
        """
        Tenta cancelar o pedido.

        Returns
        -------
        bool
            Se o pedido foi cancelado com sucesso
        """
        if self._status == (c.placed or c.sent):
            self._status = c.canceled
            return True
        return False

    def send(self) -> None:
        """
        Envia o pedido.
        """
        if self._status == c.placed:
            self._status = c.sent

    def receive(self) -> None:
        """
        Confirma o recebimento do pedido.
        """
        if self._status == c.sent:
            self._status = c.finished

    def print(self) -> None:
        """
        Printa o pedido.
        """
        print("Pedido:")
        print("- - - - -")
        for product in self._products:
            print(
                f"\t{product.quantity}x {product.name} - {product.get_total_price():.2f}R$"
            )
        print("- - - - -")
        print(f"Preço total: {self._price}\n")

    @property
    def id(self) -> int:
        return self.__id

    @property
    def customer(self) -> "Customer":
        return self.__customer

    @property
    def status(self) -> int:
        return self._status

    @property
    def products(self) -> list["Product"]:
        return self._products

    def __repr__(self) -> str:
        text: str = f"Order:[\n"
        for product in self._products:
            text += f"\t" + product.__repr__() + f"\n"
        text += "]"
        return text
