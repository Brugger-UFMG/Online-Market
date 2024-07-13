from copy import deepcopy
from typing import TYPE_CHECKING

from products.interfaces import I_Product_Manager
from products import Product

if TYPE_CHECKING:
    from users import Owner


class Product_Manager(I_Product_Manager):
    def __init__(
        self, owner: "Owner", products: dict[Product.id, Product] = dict()
    ) -> None:
        """
        Gerenciador de Produtos.

        Parameters
        ----------
        owner : Owner
            Dono
        products : dict[Product.id, Product], optional
            Produtos, by default dict()
        """
        self.__owner = owner
        self._products = products

    def register_product(self, id: int, name: str, price: float) -> None:
        """
        Registra um produto no sistema.

        Parameters
        ----------
        id : int
            Id único do produto
        name : str
            Nome do produto
        price : float
            Preço do produto
        owner : Owner
            Dono

        Raises
        ------
        ValueError
            Caso o id já esteja cadastrado
        """
        if id in self._products.keys():
            raise ValueError("Id já existe!")
        else:
            self._products[id] = Product(id, name, price, 0, self.__owner)

    def add_product(self, product_id: int, ammount: int = 1) -> None:
        """
        Adiciona uma quantidade de um produto no sistema.

        Parameters
        ----------
        product_id : int
            Id do produto
        ammount : int, optional
            Quantidade, by default 1

        Raises
        ------
        ValueError
            A quantidade deve ser maior que zero
        KeyError
            Caso o id não exista
        """
        if ammount <= 0:
            raise ValueError("A quantidade deve ser maior que zero!")

        if product_id not in self._products.keys():
            raise KeyError("Id não existe!")
        else:
            self._products[product_id].quantity += ammount

    def remove_product(self, product_id: int, ammount: int = 1) -> None:
        """
        Remove uma quantidade de um produto no sistema.

        Parameters
        ----------
        product_id : int
            Id do produto
        ammount : int, optional
            Quantidade, by default 1

        Raises
        ------
        ValueError
            A quantidade deve ser maior que zero
        KeyError
            Caso o id não exista
        """
        if ammount <= 0:
            raise ValueError("A quantidade deve ser maior que zero!")

        if product_id not in self._products.keys():
            raise KeyError("Id não existe!")
        else:
            self._products[product_id].quantity -= ammount

    def get_product(self, product_id: int) -> Product:
        """
        Obtem um produto.

        Parameters
        ----------
        product_id : int
            Id do produto

        Returns
        -------
        Product
            Produto

        Raises
        ------
        KeyError
            Caso o id não exista
        """
        if product_id not in self._products.keys():
            raise KeyError("Produto não existe!")
        else:
            return self._products[product_id]

    def retrieve_product(self, product_id: int, ammount: int = 1) -> Product:
        """
        Obtem uma quantidade de produto do sistema, a quantidade é automaticamente deduzida

        Parameters
        ----------
        product_id : int
            Id do produto
        ammount : int, optional
            Quantidade, by default 1

        Returns
        -------
        Product
            Produto

        Raises
        ------
        ValueError
            Caso a quantidade de produto seja um número inválido
        KeyError
            Caso o id não exista
        """
        if ammount <= 0:
            raise ValueError("A quantidade deve ser maior que zero!")

        if product_id not in self._products.keys():
            raise KeyError("Produto não existe!")
        else:

            if ammount > self._products[product_id].quantity:
                raise ValueError(
                    "Quantidade requisitada maior que a quantidade disponível!"
                )
            else:
                retrieved = deepcopy(self._products[product_id])
                retrieved.quantity = ammount
                self.remove_product(product_id, ammount)
                return retrieved

    def list_products(self) -> list[Product]:
        """
        Lista os produtos no sistema.

        Returns
        -------
        list[Product]
            Lista de produtos
        """
        return list(self._products)

    @property
    def owner(self) -> "Owner":
        return self.__owner

    @property
    def products(self) -> dict[Product.id, Product]:
        return self._products

    def __repr__(self) -> str:
        return f"Product_Manager(contem {len(self._products)} produtos)"
