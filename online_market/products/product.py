from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users import Owner


class Product:
    def __init__(
        self, id: int, name: str, price: float, quantity: int, owner: "Owner"
    ) -> None:
        """
        Produto.

        Parameters
        ----------
        id : int
            Identificador
        name : str
            Nome
        price : float
            Preço
        quantity : int
            Quantidade
        owner : Owner
            Dono
        """
        self.__id = id
        self.__owner = owner
        self._name = name
        self._price = price
        self._quantity = quantity

    @staticmethod
    def from_dict(data: dict, owner: "Owner") -> Product:
        expected_owner = data["owner_id"]
        if owner.id != expected_owner:
            raise ValueError(
                f"Dono inválido! Esperado dono com id: {expected_owner}, recebeu id: {owner.id}"
            )
        return Product(data["id"], data["name"], data["price"], data["quantity"], owner)

    def to_dict(self) -> dict:
        """
        Transforma o objeto em um dicionário.

        Returns
        -------
        dict
            Dicionário
        """
        return {
            "id": self.__id,
            "owner_id": self.__owner.id,
            "name": self._name,
            "price": self._price,
            "quantity": self._quantity,
        }

    def description(self) -> str:
        """
        Produz uma descrição do produto.

        Returns
        -------
        str
            Descrição
        """
        return f"{self._quantity}x {self._name} - preço unitário = {self._price}"

    def get_total_price(self) -> float:
        """
        Obtem o preço total dos produtos.

        Returns
        -------
        float
            Preço
        """
        return self._price * self._quantity

    @property
    def id(self) -> int:
        return self.__id

    @property
    def owner(self) -> "Owner":
        return self.__owner

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        if price <= 0:
            raise ValueError("O preço não pode ser menor ou igual a zero!")
        else:
            self._price = price

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        if quantity < 0:
            raise ValueError("A quantidade não pode ser menor que zero!")
        else:
            self._quantity = quantity

    def __hash__(self) -> int:
        return hash(self.__id)

    def __eq__(self, other) -> bool:
        if isinstance(other, Product):
            return self.__id == other.__id
        return False

    def __repr__(self) -> str:
        return f"Product(id={self.__id}, name={self._name}, price={self._price}, quatity={self._quantity})"
