import json
import os
from typing import Type

from users import Abstract_User, Address, Customer, Owner
from products import Product_Manager, Product
from orders import Order_Manager, Order

import constants as C


def save_data(
    owner: Owner,
    customers: dict[Customer.id, Customer],
    products: Product_Manager,
    orders: Order_Manager,
    filename: str,
) -> None:
    """
    Salva os dados do programa em um arquivo.

    Parameters
    ----------
    owner : Owner
        Dono
    customers : dict[Customer.id, Customer]
        Clientes
    products : Product_Manager
        Produtos
    orders : Order_Manager
        Pedidos
    filename : str
        Nome do arquivo a ser criado
    """
    data = {
        "owner": owner.to_dict(),
        "customers": [customer.to_dict() for customer in customers.values()],
        "products": [product.to_dict() for product in products.list_products()],
        "orders": [order.to_dict() for order in orders.list_orders()],
    }

    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Um erro ocorreu enquanto escrevendo os dados para {filename}: {e}")
    except Exception as e:
        print(f"Um erro inexperado ocorreu: {e}")


def load_data(
    filename: str,
) -> tuple[Owner, dict[Customer.id, Customer], Product_Manager, Order_Manager]:
    """
    Carrega os dados do mercado de um arquivo JSON.

    Parameters
    ----------
    filename : str
        Caminho para o arquivo JSON.

    Returns
    -------
    tuple[Owner, dict[Customer.id, Customer], Product_Manager, Order_Manager]
        Tupla contendo: owner, customers, products e orders

    Raises
    ------
    FileNotFoundError
        Caso o arquivo não seja encontrado
    json.JSONDecodeError
        Caso ocorra um erro de decodificação
    """
    if not os.path.exists(filename):
        raise FileNotFoundError("Arquivo {filename} não encontrado.")

    with open(filename, "r") as file:
        data = json.load(file)

    owner = Owner.from_dict(data["owner"])

    customers = {}
    for customer_data in data["customers"]:
        customer = Customer.from_dict(customer_data)
        customers[customer.id] = customer

    products_dict = {}
    for product_data in data["products"]:
        product = Product.from_dict(product_data, owner)
        products_dict[product.id] = product
    products = Product_Manager(owner, products_dict)

    orders_dict = {}
    for order_data in data["orders"]:
        order = Order.from_dict(order_data, customers, owner)
        orders_dict[order.id] = order
    orders = Order_Manager(owner, orders_dict)

    return owner, customers, products, orders


def generate_auth_data(
    owner: Owner, customers: dict[Customer.id, Customer]
) -> dict[Abstract_User.name, Abstract_User]:
    """
    Cria os dados de autenticação para todos usuários do sistema.

    Parameters
    ----------
    owner : Owner
        Dono
    customers : dict[Customer.id, Customer]
        Clientes

    Returns
    -------
    dict[Abstract_User.name, Abstract_User]
        Dados de autenticação de todos usuários
    """

    auth_data: dict[Abstract_User.name, Abstract_User] = dict()

    for customer in customers.values():
        assert isinstance(customer, Abstract_User)
        auth_data[customer.name] = customer
    auth_data[owner.name] = owner

    return auth_data


def login(auth_data: dict[Abstract_User.name, Abstract_User]) -> Abstract_User | None:
    """
    Inicia o processo de login na plataforma.

    Parameters
    ----------
    auth_data : dict[Abstract_User.name, Abstract_User]
        Dicionário contendo todos usuários do sistema
        key = Nome do usuário
        value = Objeto do usuário

    Returns
    -------
    Type | None
        Retorna o tipo do usuário se o login foi bem sucedido
        Retorna None se o login não foi bem sucedido
    """

    print("Insira seu nome de usuário:")
    name = input(">> ")

    if name not in auth_data.keys():
        print("Nome incorreto.")
        return None
    else:
        print("\nInsira sua senha:")
        password = input(">> ")
        if password == auth_data[name].password:
            print("Login bem sucedido!")
            return auth_data[name]
        else:
            print("Senha incorreta!")
            return None


def is_zip_code(zip_code: str) -> bool:
    if len(zip_code) == len("xxxxx-xxx"):
        if zip_code[5] == "-":
            split = zip_code.split("-", 1)
            if len(split) == 2:
                zip_code = split[0] + split[1]
                if zip_code.isnumeric():
                    return True
    return False


def register(
    customers: dict[Customer.id, Customer],
    auth_data: dict[Abstract_User.name, Abstract_User],
) -> None:
    """
    Realiza o registro de um novo cliente e o insere na lista de clientes.

    Parameters
    ----------
    customers : dict[Customer.id, Customer]
        Dicionario contendo os dados dos clientes registrados

    auth_data : dict[Abstract_User.name, Abstract_User]
        Dicionário contendo todos usuários do sistema
        key = Nome do usuário
        value = Objeto do usuário
    """

    # Recbe o nome
    while True:
        print("Insira seu nome de usuário:")
        name = input(">> ")

        if len(name) <= 1:
            print("Nome muito curto!\n")
        elif not name.isalpha():
            print("O nome deve ser composto somente de letras!\n")
        else:
            break

    # Recebe a senha
    while True:
        print("\nInsira sua senha:")
        password = input(">> ")

        if len(password) <= 1:
            print("Insira uma senha mais comprida!")
        else:
            break

    # Cria o endereço
    # Estado
    while True:
        print("\nInsira o nome do seu estado:")
        state = input(">> ")
        if not all(char.isalpha() or char.isspace() for char in state):
            print("O nome deve ser composto somente por letras e espaços!")
        else:
            break
    # Cidade
    while True:
        print("\nInsira o nome da sua cidade:")
        city = input(">> ")
        if not all(char.isalpha() or char.isspace() for char in city):
            print("O nome deve ser composto somente por letras e espaços!")
        else:
            break
    # Rua
    while True:
        print("\nInsira o nome da sua rua:")
        street = input(">> ")
        if not all(char.isalpha() or char.isspace() for char in street):
            print("O nome deve ser composto somente por letras e espaços!")
        else:
            break
    # Numero da casa
    while True:
        print("\nInsira o número da sua casa:")
        house_num_str = input(">> ")
        if not house_num_str.isnumeric():
            print("O nome deve ser composto somente por letras e espaços!")
        else:
            house_number = int(house_num_str)
            break
    # Complemento
    print("\nInsira o complemento (se houver):")
    complement = input(">> ")
    # CEP
    while True:
        print("\nInsira o seu CEP (xxxxx-xxx):")
        zip_code = input(">> ")

        if not is_zip_code(zip_code):
            print("CEP inválido!")
        else:
            break

    # Cria o usuário
    print("\n- - - Revisão - - -")
    print("Revise seus dados:")
    print(f"> Nome: {name}\n> Senha: {password}\n> Endereço:")
    print(
        f"  - Estado: {state}\n  - Cidade:{city}\n  - Rua: {street}\n  - Número: {house_number}\n  - Complemento: {complement}\n  - CEP: {zip_code}\n"
    )

    while True:
        print("Confirmar usuário? [s/n]")
        yes_no = input(">> ")
        if yes_no == "s":
            new_user = Customer(
                len(customers) + 1,
                name,
                password,
                Address(street, city, state, zip_code, house_number, complement),
            )
            customers[new_user.id] = new_user
            auth_data[new_user.name] = new_user
            print("Cadastro realizado com sucesso!\n")
            break
        elif yes_no == "n":
            print("Cadastro cancelado.\n")
            break
        else:
            print("Opção inválida.")


def quit() -> None:
    pass
