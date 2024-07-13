from typing import TYPE_CHECKING

from users import Abstract_User

if TYPE_CHECKING:
    from orders import Order
    from users import Owner


class Customer(Abstract_User):
    def __init__(
        self,
        id: int,
        name: str,
        password: str,
        address: str,
        orders: list["Order"] = [],
    ) -> None:
        """
        Cliente.

        Parameters
        ----------
        id : int
            Identificador
        name : str
            Nome
        password : str
            Senha
        address : str
            Endereço
        orders : list[&quot;Order&quot;], optional
            Pedidos, by default []
        """
        super().__init__(id, name, password)
        self._address = address
        self._orders = orders

    # def place_order(self, market_owner: "Owner") -> None:
    #     pass

    # def get_order(self, order_id: int) -> Order: ...

    # def cancel_order(self, order_id: int) -> bool: ...

    # def confirm_arrival(self, order_id: int) -> None: ...

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, address: str) -> None:
        self._address = address

    @property
    def orders(self) -> list["Order"]:
        return self._orders
