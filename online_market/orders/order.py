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
        status: str = c.placed,
    ) -> None:
        """
        Pedido.

        Parameters
        ----------
        id : int
            Identificador
        customer : Customer
            Cliente
        products : list[Product]
            Produtos
        status : str, optional
            Status do Pedido, by default c.placed
        """
        self.__id = id
        self.__customer = customer
        self.__customer.orders.append(self)

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
        if self._status != c.canceled:
            self._status = c.canceled
            return True
        return False

    def send(self) -> bool:
        """
        Envia o pedido.

        Returns
        -------
        bool
            Se o pedido foi enviado.
        """
        if self._status == c.placed:
            self._status = c.sent
            return True
        return False

    def receive(self) -> bool:
        """
        Confirma o recebimento do pedido.

        Returns
        -------
        bool
            Se o pedido foi confirmado recebido
        """
        if self._status == c.sent:
            self._status = c.finished
            return True
        return False

    def description(self, id: int = -1) -> str:
        """
        Gera uma descrição do pedido.

        Parameters
        ----------
        id : int, optional
            Se deve ser usado um outro id, by default -1

        Returns
        -------
        str
            Descrição
        """
        if id < 0:
            id = self.__id

        description = f"- Pedido {id} -\n"
        for product in self._products:
            description += f"> {product.quantity}x {product.name} = {product.get_total_price():.2f}R$\n"

        description += f"\nPreço total: {self._price}"
        description += f"\nCliente: {self.__customer.name}"
        description += f"\nStatus: {self._status}\n"
        description += "- - -"
        return description

    @property
    def id(self) -> int:
        return self.__id

    @property
    def customer(self) -> "Customer":
        return self.__customer

    @property
    def status(self) -> str:
        return self._status

    @property
    def products(self) -> list["Product"]:
        return self._products

    @property
    def price(self) -> float:
        return self._price

    def __repr__(self) -> str:
        text: str = (
            f"Order:(id={self.__id}, customer={self.__customer}, status={self._status}, products=[\n"
        )
        for product in self._products:
            text += f"\t" + product.__repr__() + f"\n"
        text += "])"
        return text
