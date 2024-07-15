import os
import json

from users import Owner
from products import Product_Manager
from orders import Order_Manager

import constants as C
import functions as F


def setup() -> None:
    if os.path.exists(C.database):
        print("Uma database já existe! Abortando setup.")
        return

    # Recbe o nome
    while True:
        print("Insira o nome do admin:")
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

    # Cria o usuário
    print("\n- - - Revisão - - -")
    print("Revise seus dados:")
    print(f"> Nome: {name}\n> Senha: {password}\n")

    while True:
        print("Confirmar usuário? [s/n]")
        yes_no = input(">> ")
        if yes_no == "s":
            owner = Owner(
                0,
                name,
                password,
            )
            print("Cadastro realizado com sucesso!\n")
            break
        elif yes_no == "n":
            print("Cadastro cancelado.\n")
            break
        else:
            print("Opção inválida.")

    F.save_data(owner, {}, Product_Manager(owner), Order_Manager(owner), C.database)


if __name__ == "__main__":
    setup()
