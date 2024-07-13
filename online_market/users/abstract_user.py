from abc import ABC, abstractmethod
import inspect


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

    def get_permissions(self) -> list[str]:
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        permissions = [name for name, method in methods if not name.startswith("_")]
        permissions.remove("get_permissions")
        return permissions

    def change_password(self) -> None:
        """
        Altera a senha do usuário por meio de um processo interativo.
        """

        check = input("Digite sua senha atual: ")
        if check == self.__password:
            self._password = input("Digite sua nova senha: ")
        else:
            print("Senha incorreta, operação cancelada.")

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
        return self._password
