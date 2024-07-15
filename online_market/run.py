import json
import os

from users import Abstract_User, Address, Customer, Owner
from products import Product_Manager
from orders import Order_Manager

import constants as C
import functions as F


def run() -> None:
    # --- Inicialização --- #
    try:
        owner, customers, market, orders = F.load_data(C.database)
    except FileNotFoundError:
        print("Database não encontrada! (Execute o setup para cadastrar um dono)")
    except json.JSONDecodeError as e:
        print(f"Um erro ocorreu enquanto decodificando o arquivo JSON: {e}")
    except Exception as e:
        print(f"Um erro inexperado ocorreu enquanto carregando a database: {e}")

    auth_data = F.generate_auth_data(owner, customers)

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
    F.save_data(owner, customers, market, orders, C.database)


if __name__ == "__main__":
    run()
