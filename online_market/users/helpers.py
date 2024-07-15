def confirm(message: str) -> bool:
    while True:
        print(message + " [s/n]:")
        yes_no = input(">> ")
        if yes_no == "s":
            print()
            return True
        elif yes_no == "n":
            print("Operação cancelada.\n")
            return False
        else:
            print("Opção inválida.")
