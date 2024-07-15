from users import Abstract_User
from products import Product_Manager, Product
from orders import Order_Manager, Order
import orders.constants as o_constants
import users.helpers as h


class Owner(Abstract_User):
    def __init__(
        self,
        id: int,
        name: str,
        password: str,
    ) -> None:
        """
        Dono/Administrador.

        Parameters
        ----------
        id : int
            Identificador
        name : str
            Nome
        password : str
            Senha
        """
        super().__init__(id, name, password)
        self.__products: Product_Manager
        self.__orders: Order_Manager

    def view_orders(self) -> None:
        """
        Visualiza todos os pedidos.
        """
        print("- - - Pedidos - - -")
        orders = self.__orders.list_orders()
        if len(orders) < 1:
            print("Não existem pedidos no sistema!")
        else:
            for order in orders:
                print(order.description())

    def add_product(self) -> None:
        """
        Adiciona um produto ao sistema por meio de um processo interativo.
        """
        while True:
            print("- - - Adicionar Produto - - -")
            print("Como deseja adicionar o novo produto?: ")
            print("[1] Cadastrar novo")
            print("[2] Reabastecer existente")
            print("[3] Cancelar")
            check = input(">> ")
            print()

            try:
                selected = int(check)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            match selected:
                case 1:
                    self.__register_product()
                    return
                case 2:
                    self.__add_to_product()
                    return
                case 3:
                    print("Operação cancelada!")
                    return
                case _:
                    print("Opção inválida! Tente novamente.")
            print()

    def remove_product(self) -> None:
        """
        Remove um produto do sistema por meio de um processo interativo.
        """
        while True:
            print("- - - Remover Produto - - -")
            print("Como deseja remover produto?: ")
            print("[1] Deletar um produto e seu Id")
            print("[2] Remover uma quantidade de um produto")
            print("[3] Cancelar")
            check = input(">> ")
            print()

            try:
                selected = int(check)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            match selected:
                case 1:
                    self.__delete_product()
                    return
                case 2:
                    self.__remove_from_product()
                    return
                case 3:
                    print("Operação cancelada!")
                    return
                case _:
                    print("Opção inválida! Tente novamente.")
            print()

    def send_order(self) -> None:
        """
        Envia um pedido por meio de um processo interativo.
        """
        while True:
            print("- - - Enviar Pedido - - -")

            not_sent: list[Order] = []
            for order in self.__orders.list_orders():
                if order.status == o_constants.placed:
                    not_sent.append(order)

            if len(not_sent) < 1:
                print("Não há pedidos a serem enviados!")
                return
            else:
                for i, order in enumerate(not_sent):
                    print(order.description(i + 1))

                while True:
                    print("Qual pedido deseja enviar?")

                    check = input(">> ")
                    try:
                        selected = int(check) - 1
                    except ValueError:
                        print("Digite um número! Tente novamente.\n")
                        continue

                    if selected < 0 or selected >= len(not_sent):
                        print("Valor inválido!\n")
                    else:
                        break

                print("\n- - - - -\nPedido selecionado:")
                print(not_sent[selected].description(selected + 1))
                if h.confirm("\nConfirmar envio do pedido?") == False:
                    print("Operação cancelada!")
                else:
                    not_sent[selected].send()
                    print("Pedido enviado com sucesso!")
                return

    def __register_product(self) -> None:
        """
        Registra um novo produto por meio de um processo interativo.
        """
        print("- - - Registrar Produto - - -")
        # Nome do produto
        while 1:
            print("Nome do produto: ")
            name = input(">> ")

            if not all(char.isalpha() or char.isspace() for char in name):
                print("O nome deve ser composto somente por letras e espaços!")
            else:
                break
            print()

        # Preço
        while 1:
            print("\nPreço do produto: ")
            price_str = input(">> ")

            try:
                price = float(price_str)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if price <= 0.0:
                print("O preço deve ser maior que 0!")
            else:
                break
            print()

        # Id
        sorted_ids = sorted(self.__products.products.keys())
        if len(sorted_ids) == 0:
            id = 0
        elif sorted_ids[-1] < len(sorted_ids):
            id = len(self.__products.list_products())
        else:
            for i, j in enumerate(sorted_ids):
                if i < j:
                    id = i
                    break

        # Cria o Produto
        print("\n- - - Revisão - - -")
        print("Revise os dados do produto criado:")
        print(f"\n> Id: {id}\n> Nome: {name}\n> Preço: {price}\n")

        while True:
            print("Confirmar registro? [s/n]")
            yes_no = input(">> ")
            if yes_no == "s":
                self.__products.register_product(id, name, price)
                print("Cadastro realizado com sucesso!\n")
                return
            elif yes_no == "n":
                print("Cadastro cancelado.\n")
                return
            else:
                print("Opção inválida.")

    def __add_to_product(self) -> None:
        """
        Adiciona uma quantidade de produtos a um produto já existente
        por meio de um processo interativo.
        """
        self.view_products(self.__products)

        # Seleciona o produto
        selected = self._select_product(
            self.__products, "Qual dos produtos deseja reabastecer?"
        )
        product = self.__products.get_product(selected)
        print("Produto selecionado: ")
        print(product.description())

        if h.confirm("Confirmar produto?") == False:
            return

        # Adiciona quantidade ao produto
        while True:
            print(f"Quantos {product.name} devem ser adicionados?")
            ammount_str = input(">> ")

            try:
                ammount = int(ammount_str)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if ammount <= 0:
                print("A quantidade deve ser maior que 0!")
            else:
                self.__products.add_product(selected, ammount)
                print("Operação realizada com sucesso!")
                return
            print()

    def __delete_product(self) -> None:
        """
        Deleta um produto e seu ID por meio de um processo interativo.
        """
        self.view_products(self.__products)

        # Seleciona o produto
        selected = self._select_product(self.__products, "Qual produto deseja excluir?")
        product = self.__products.get_product(selected)
        print("Produto selecionado: ")
        print(product.description())

        if h.confirm("Confirmar produto?") == False:
            return

        # Deleta o produto
        for order in self.__orders.list_orders():
            used_ids = set()
            for product in order.products:
                used_ids.add(product.id)

        try:
            if selected in used_ids:
                can_remove = False
            else:
                can_remove = True
        except UnboundLocalError:
            can_remove = True

        if can_remove:
            self.__products.delete_product(selected)
            print("Produto removido com sucesso!")
        else:
            print(
                "Não é possível remover este produto pois ele ainda está sendo usado no sistema."
            )

    def __remove_from_product(self) -> None:
        """
        Deduz uma quantidade de produto de um produto já existente
        por meio de um processo interativo.
        """
        self.view_products(self.__products)

        # Seleciona o produto
        selected = self._select_product(
            self.__products, "De qual dos produtos deseja remover?"
        )
        product = self.__products.get_product(selected)
        print("Produto selecionado: ")
        print(product.description())

        if h.confirm("Confirmar produto?") == False:
            return

        # Remove quantidade do produto
        while True:
            print(f"Quantos {product.name} devem ser removidos?")
            ammount_str = input(">> ")

            try:
                ammount = int(ammount_str)
            except ValueError:
                print("Digite um número! Tente novamente.\n")
                continue

            if ammount <= 0:
                print("A quantidade deve ser maior que 0!")
            else:
                if ammount > product.quantity:
                    self.__products.remove_product(selected, product.quantity)
                else:
                    self.__products.remove_product(selected, ammount)
                print("Operação realizada com sucesso!")
                return
            print()

    @property
    def products(self) -> Product_Manager:
        return self.__products

    @products.setter
    def products(self, products: Product_Manager) -> None:
        self.__products = products

    @property
    def orders(self) -> Order_Manager:
        return self.__orders

    @orders.setter
    def orders(self, orders: Order_Manager) -> None:
        self.__orders = orders

    def __repr__(self) -> str:
        return f"Owner(id={self.id}, name={self.name}, password={self.password}, products={self.products}, orders={self.orders})"
