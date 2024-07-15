import json
from copy import deepcopy

from users import Abstract_User, Address, Customer, Owner
from products import Product_Manager, Product
from orders import Order, Order_Manager

import constants as C
import functions as F


def run():
    # --- Inicialização --- #
    # TODO carregar os dados e criar os objetos do programa
    # Obtem os usuários do sistema
    owner = Owner(0, "admin", "123")
    customers: dict[Customer.id, Customer] = dict()
    for i, name in enumerate(C.nomes):
        customers[i + 1] = Customer(
            i + 1,
            name,
            "123",
            Address(
                "Rua Tal", "Belo Horizonte", "Minas Gerais", "12345678-09", 321, "A"
            ),
        )
    auth_data = F.generate_auth_data(owner, customers)

    # Obtém os produtos do mercado
    market = Product_Manager(owner)
    for i, product in enumerate(C.produtos):
        market.register_product(i, product, C.precos[i])
    for i, quantity in enumerate(C.quantidades):
        market.add_product(i, quantity)

    # Obtém os pedidos do mercado
    orders = Order_Manager(owner)
    _produto = deepcopy(market.get_product(0))
    _produto.quantity = 1
    orders.place_order(customers[1], [_produto])

    # --- Tela de início --- #
    logged_in = None
    while logged_in == None:
        print("- - - Bem Vindo! - - -")
        print("O que deseja fazer?")
        print(f"[{C.login}] Login\n[{C.register}] Register\n[{C.quit}] Quit")

        option = input(">> ")
        print()

        # Converte o input em inteiro
        try:
            int(option)
        except ValueError:
            print("Digite um número! Tente novamente.\n")
            continue

        # Procede com o proximo passo de acordo com
        # o escolhido pelo usuário
        match int(option):
            case C.login:
                print("- - - Login - - -")
                logged_in = F.login(auth_data)

            case C.register:
                print("- - - Registrar - - -")
                F.register(customers, auth_data)

            case C.quit:
                break

            case _:
                print("Opção inválida! Tente novamente.")
        print()

    # --- Loop Principal --- #
    if logged_in != None:
        assert isinstance(logged_in, Abstract_User)
        permissions = logged_in.get_permissions()

        while logged_in != None:
            # Dicionario especificando argumentos para métodos que precisam
            args_dict: dict[str, tuple[tuple, dict]] = {
                "view_products": ((market,), {}),
                "place_order": ((owner,), {}),
            }

            print("- - - Mercado Online - - -")
            print(f"Olá {logged_in.name}!\n")
            print("O que deseja fazer?")

            # Printa as permissões do usuário
            i = 0
            for i, permission in enumerate(permissions):
                permission = permission.replace("_", " ")
                permission = permission.title()
                print(f"[{i + 1}] {permission}")
            print(f"[{i + 2}] Quit")

            option = input(">> ")
            print()

            # Converte o input em um índice da permissão selecionada na lista de permissões
            try:
                selected = int(option) - 1
            except ValueError:
                print("Digite um número! Tente novamente.")
                continue

            # Determina qual método executar dinamicamente baseado na permissão selecionada
            if selected < len(permissions) and selected >= 0:
                method = getattr(logged_in, permissions[selected])
                args, kwargs = args_dict.get(permissions[selected], ((), {}))
                method(*args, **kwargs)
            elif selected == len(permissions):
                break
            else:
                print("Opção inválida! Tente novamente.")
            print()

    # --- Finalização --- #
    # TODO salvar os dados do programa
    print("- - - Owner - - -")
    print(owner)
    print("- - -Customers - - -")
    print(customers)
    print("- - - Auth Data - - -")
    print(auth_data)
    print("- - - Market - - -")
    print(market)
    print("- - - Products - - -")
    print(market.list_products())
    print("- - - Order Manager - - -")
    print(orders)
    print("- - - Orders - - -")
    print(orders.list_orders())


if __name__ == "__main__":
    run()
