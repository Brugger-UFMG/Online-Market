from typing import TYPE_CHECKING, Type

from users import Abstract_User
import users.helpers as h
from products import Product

if TYPE_CHECKING:
    from orders import Order
    from users import Address, Owner
    from products import Product_Manager


class Customer(Abstract_User):
    def __init__(
        self,
        id: int,
        name: str,
        password: str,
        address: "Address",
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
        orders : list[Order], optional
            Pedidos, by default []
        """
        super().__init__(id, name, password)
        self._address = address
        self._orders = orders

    def view_orders(self) -> None:
        """
        Visualiza todos os pedidos do cliente.
        """
        print("- - - Pedidos - - -")
        if len(self._orders) < 1:
            print("Você não tem pedidos!")
        else:
            for i, order in enumerate(self._orders):
                print(order.description(i + 1))

    def view_products(self, market: "Product_Manager") -> None:
        """
        Visualiza todos os produtos no mercado.

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
                if product.quantity > 0:
                    print(f"[{product.id}]: " + product.description())

    def place_order(self, market_owner: "Owner") -> None:
        """
        Realiza um pedido por meio de um processo interativo.

        Parameters
        ----------
        market_owner : Owner
            Dono do mercado
        """
        products: list[Product] = []

        while True:
            print("- - - Novo Pedido - - -")
            print("O que deseja fazer? ")
            print("[1] Adicionar produto")
            print("[2] Remover produto")
            print("[3] Concluir")
            print("[4] Cancelar")
            check = input(">> ")
            print()

            try:
                selected = int(check)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            match selected:
                case 1:
                    retrieved = self.__get_product_from_market(market_owner.products)
                    if retrieved != None:
                        assert isinstance(retrieved, Product)
                        products.append(retrieved)
                        print("Operação realizada com sucesso!")
                case 2:
                    self.__remove_product_from_list(products)
                case 3:
                    if len(products) < 1:
                        print("Não há produtos no pedido!")
                    else:
                        print("- - - Pedido - - -")
                        preco_total = 0.0
                        for product in products:
                            print(
                                f"> {product.quantity}x {product.name} = {product.get_total_price():.2f}R$"
                            )
                            preco_total += product.get_total_price()
                        print(f"Preço total: {preco_total}")
                        print("- - - - -\n")

                        if h.confirm("Confirmar pedido?") == True:
                            market_owner.orders.place_order(self, products)
                            print("Pedido realizado com sucesso!")
                            return
                        else:
                            print("Voltando...")
                case 4:
                    print("Operação cancelada!")
                    return
                case _:
                    print("Opção inválida! Tente novamente.")
            print()

    def cancel_order(self) -> None:
        """
        Cancela um pedido por meio de um processo interativo.
        """
        print("- - - Cancelar Pedido - - -")
        self.view_orders()

        while True:
            print("\nQual pedido deve ser cancelado?")
            check = input(">> ")
            try:
                selected = int(check) - 1
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if selected < 0 or selected > len(self._orders):
                print("Seleção inválida! Tente novamente.")
            else:
                print()
                if self._orders[selected].cancel() == True:
                    print("Pedido cancelado com sucesso!")
                else:
                    print("Não foi possível cancelar o pedido!")
                return

    def confirm_arrival(self) -> None:
        """
        Confirma o recebimento de um pedido por meio de um processo interativo.
        """
        print("- - - Confirmar Recebimento - - -")
        self.view_orders()

        while True:
            print("\nQual pedido você recebeu?")
            check = input(">> ")
            try:
                selected = int(check) - 1
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if selected < 0 or selected > len(self._orders):
                print("Seleção inválida! Tente novamente.")
            else:
                print()
                if self._orders[selected].receive() == True:
                    print("Pedido recebido com sucesso!")
                else:
                    print("Falha! Este pedido não foi enviado!")
                return

    def __get_product_from_market(self, market: "Product_Manager") -> Product | None:
        """
        Obtem um produto do mercado por meio de um processo interativo.

        Parameters
        ----------
        market : Product_Manager
            Mercado

        Returns
        -------
        Product | None
            Produto obtido
            None caso nenhum produto seja escolhido
        """
        self.view_products(market)

        # Seleciona o produto
        selected = self._select_product(market, "\nQual dos produtos deseja adicionar?")
        product = market.get_product(selected)
        print("Produto selecionado: ")
        print(product.description() + "\n")

        # Seleciona quantidade
        while True:
            print(f"Quantos {product.name} devem ser adicionados?")
            ammount_str = input(">> ")

            try:
                ammount = int(ammount_str)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if ammount < 1:
                print("A quantidade deve ser maior que 0")
            elif ammount > product.quantity:
                print(f"A quantidade deve ser menor que {product.quantity}")
            else:
                product = market.retrieve_product(selected, ammount)
                return product
            print()

    def __remove_product_from_list(self, products: list[Product]) -> None:
        """
        Remove um produto de uma lista de compras.

        Parameters
        ----------
        products : list[Product]
            Lista de compras
        """
        print("- - - Produtos - - -")
        if len(products) < 1:
            print("Não há produtos no pedido!")
            return
        else:
            for i, product in enumerate(products):
                print(f"[{i + 1}]: " + product.description())

        while True:
            print("\nQual produto deseja remover?")
            check = input(">> ")
            try:
                selected = int(check) - 1
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if selected < 0 or selected > len(products):
                print("Seleção inválida! Tente novamente.")
            else:
                products.pop(selected)
                print("Produto removido com sucesso!")
                return

    @property
    def address(self) -> "Address":
        return self._address

    @address.setter
    def address(self, address: "Address") -> None:
        self._address = address

    @property
    def orders(self) -> list["Order"]:
        return self._orders

    @orders.setter
    def orders(self, orders: list["Order"]) -> None:
        self._orders = orders

    def __repr__(self) -> str:
        return f"Customer(id={self.id}, name={self.name}, password={self.password}, address={self.address}, has {len(self.orders)} orders)"
