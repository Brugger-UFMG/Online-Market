from users import Abstract_User
from products import Product_Manager, Product
from orders import Order


class Owner(Abstract_User):
    def __init__(
        self,
        id: int,
        name: str,
        password: str,
        products: dict[Product.id, "Product"] = dict(),
        orders: dict[Order.id, "Order"] = dict(),
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
        products : dict[Product.id, Product], optional
            Produtos, by default dict()
        orders : dict[Order.id, Order], optional
            Pedidos, by default dict()
        """
        super().__init__(id, name, password)
        self.__products = products
        self.__orders = orders

    def add_product(self, name: str, price: float, quantity: int) -> None:
        pass

    def remove_product(self, product_id: int) -> None:
        pass

    def send_order(self, order_id: int) -> None:
        pass
