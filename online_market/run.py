import products
import users
import products
import orders
import users.customer


def run():
    teste = users.Customer(0, "teste", "123", "rua tal")
    print(teste.get_permissions())
    print("Hello World")


if __name__ == "__main__":
    run()
