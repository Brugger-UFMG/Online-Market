from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import inspect

if TYPE_CHECKING:
    from products import Product_Manager, Product


class Abstract_User(ABC):
    def __init__(self, id: int, name: str, password: str) -> None:
        """
        Abstração de um usuário do sistema.

        Parameters
        ----------
        id : int
            Identificador unico do usuário
        name : str
            Nome do usuário
        password : str
            Senha de autenticação do usuário
        """
        self.__id = id
        self._name = name
        self.__password = password

    @abstractmethod
    def view_orders(self) -> None:
        pass

    def view_products(self, market: "Product_Manager") -> None:
        """
        Printa todos produtos no mercado.

        Parameters
        ----------
        market : Product_Manager
            Mercado
        """
        print("- - - Produtos - - -")
        products = market.list_products()
        if len(products) < 1:
            print("Não há produtos no mercado!")
        else:
            for product in products:
                print(f"[{product.id}]: " + product.description())

    def get_permissions(self) -> list[str]:
        """
        Retorna todos métodos públicos da classe, com excessão desse método.

        Returns
        -------
        list[str]
            Lista com os nomes de todos métodos
        """
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        permissions = [name for name, method in methods if not name.startswith("_")]
        permissions.remove("get_permissions")
        return permissions

    def change_password(self) -> None:
        """
        Altera a senha do usuário por meio de um processo interativo.
        """
        print("- - - Alteração de Senha - - -")
        print("Digite sua senha atual: ")
        check = input(">> ")

        if check != self.__password:
            print("Senha incorreta, operação cancelada.")
        else:
            while True:
                print("\nDigite sua nova senha: ")
                password = input(">> ")

                if len(password) <= 1:
                    print("Insira uma senha mais comprida!")
                else:
                    print("Senha alterada com sucesso!")
                    self.__password = password
                    break

    def _select_product(self, products: "Product_Manager", message: str) -> int:
        """
        Seleciona um produto por meio de um processo interativo.

        Parameters
        ----------
        message : str
            Mensagem a ser mostrada na tela

        Returns
        -------
        int
            Id do produto selecionado
        """
        while True:
            print(message)
            check = input(">> ")
            print()

            try:
                selected = int(check)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if not selected in products.products.keys():
                print("Opção inválida!\n")
            else:
                return selected

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if len(name) > 1:
            self._name = name

    @property
    def password(self) -> str:
        return self.__password
