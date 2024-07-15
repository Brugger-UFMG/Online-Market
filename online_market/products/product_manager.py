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
        self.__owner.products = self
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

    def delete_product(self, product_id: int) -> None:
        """
        Deleta completamente um produto e seu Id.
        Este método não verifica se o produto existe em outras partes do sistema,
        o que pode gerar conflitos de Id.

        Parameters
        ----------
        product_id : int
            Id do produto

        Raises
        ------
        KeyError
            Caso o id não exista
        """
        if product_id not in self._products.keys():
            raise KeyError("Id não existe!")
        else:
            self._products.pop(product_id)

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
            return deepcopy(self._products[product_id])

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
        Lista os produtos no sistema, ordenados por seus Ids.

        Returns
        -------
        list[Product]
            Lista de produtos
        """
        sorted_keys = self.ids()
        return [self._products[key] for key in sorted_keys]

    def ids(self) -> set[int]:
        """
        Retorna os Ids de todos produtos em ordem crescente.

        Returns
        -------
        set[int]
            Set contendo os Ids.
        """
        return set(sorted(self._products.keys()))

    @property
    def owner(self) -> "Owner":
        return self.__owner

    @property
    def products(self) -> dict[Product.id, Product]:
        return self._products

    def __repr__(self) -> str:
        return f"Product_Manager(contem {len(self._products)} produtos)"
