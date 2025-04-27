import models
from datetime import datetime

def userMenu():
    while(True):
        print("\n--- Menu de Clientes ---")
        print("1 - Adicionar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("0 - Voltar")
        op = input("Escolha: ")

        if op == "1":
            name = input("Nome: ")
            cpf = input("CPF: ")
            models.User.create(name=name, cpf=cpf)  
            print("Cliente adicionado com sucesso!")
        elif op == "2":
            print("\n--- Lista de Clientes ---")
            for user in models.User.select():  
                print(f"{user.id} - {user.name} ({user.cpf})")
        elif op == '3':
            try:
                userId = int(input("ID do cliente a atualizar: "))
                try:
                    user = models.User.get_by_id(userId)  
                    newName = input("Novo nome: ")
                    newCpf = input("Novo CPF: ")
                    user.name = newName
                    user.cpf = newCpf
                    user.save()
                    print("Cliente atualizado com sucesso!")
                except models.User.DoesNotExist:  
                    print(f"Cliente com ID {userId} não encontrado.")
            except ValueError:
                print("ID inválido. Digite um número inteiro.")
        elif op == '4':
            try:
                userId = int(input("ID do cliente a excluir: "))
                try:
                    user = models.User.get_by_id(userId)  
                    user.delete_instance()
                    print("Cliente excluído com sucesso!")
                except models.User.DoesNotExist:  
                    print(f"Cliente com ID {userId} não encontrado.")
            except ValueError:
                print("ID inválido. Digite um número inteiro.")
        elif op == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def productsMenu():
    while(True):
        print("\n--- Menu de Produtos ---")
        print("1 - Adicionar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Excluir produto")
        print("0 - Voltar")
        op = input("Escolha: ")

        if op == "1":
            productName = input("Nome do produto: ")
            price = input("Preço do produto: ")
            models.Product.create(productName=productName, price=price)  
            print("Produto adicionado com sucesso!")
        elif op == "2":
            print("\n--- Lista de Produtos ---")
            for product in models.Product.select():  
                print(f"{product.id} - {product.productName} (R$ {product.price})")
        elif op == '3':
            try:
                productId = int(input("ID do produto a atualizar: "))
                try:
                    product = models.Product.get_by_id(productId)
                    newProductName = input("Novo nome do produto: ")
                    newPrice = input("Novo preço do produto: ")
                    product.productName = newProductName
                    product.price = newPrice
                    product.save()
                    print("Produto atualizado com sucesso!")
                except models.Product.DoesNotExist:
                    print(f"Produto com ID {productId} não encontrado.")
                except Exception as e:
                    print(f"Erro ao atualizar produto: {e}")
            except ValueError:
                print("ID inválido. Digite um número inteiro.")
        elif op == '4':
            try:
                productId = int(input("ID do produto a excluir: "))
                try:
                    product = models.Product.get_by_id(productId)
                    product.delete_instance()
                    print("Produto excluído com sucesso!")
                except models.Product.DoesNotExist:
                    print(f"Produto com ID {productId} não encontrado.")
            except ValueError:
                print("ID inválido. Digite um número inteiro.")
        elif op == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def ordersMenu():
    while(True):
        print("\n--- Menu de Pedidos ---")
        print("1 - Criar novo pedido")
        print("2 - Listar pedidos")
        print("3 - Adicionar item ao pedido")
        print("0 - Voltar")
        op = input("Escolha: ")

        if op == "1":
            try:
                userId = int(input("ID do cliente para este pedido: "))
                user = models.User.get_by_id(userId)
                newOrder = models.Order.create(user=user, orderDate=datetime.now(), totalPrice=0.0)
                print(f"Pedido {newOrder.id} criado para o cliente {user.name}.")
                adicionar_itens_ao_pedido(newOrder)
            except models.User.DoesNotExist:
                print(f"Cliente com ID {userId} não encontrado.")
            except ValueError:
                print("ID inválido. Digite um número inteiro.")
        elif op == "2":
            print("\n--- Lista de Pedidos ---")
            for order in models.Order.select(models.Order, models.User).join(models.User).order_by(models.Order.id):
                print(f"ID: {order.id}, Cliente: {order.user.name} (ID: {order.user.id}), Data: {order.orderDate.strftime('%d/%m/%Y %H:%M:%S')}, Total: R$ {order.totalPrice:.2f}")
                print("Itens do Pedido:")
                for item in models.productOrder.select(models.productOrder, models.Product).join(models.Product).where(models.productOrder.pedido == order):
                    print(f"  - {item.product.productName} (R$ {item.product.price})")
        elif op == "3":
            adicionar_itens_ao_pedido()
        elif op == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def adicionar_itens_ao_pedido(pedido):

    while True:
        try:
            productId = int(input("ID do product a adicionar (ou 0 para terminar): "))
            if productId == 0:
                break  # Encerra o loop quando o usuário digita 0

            product = models.Product.get_by_id(productId)
            quantidade = int(input("Quantidade: "))
            models.productOrder.create(pedido=pedido, product=product)
            print(f"Item {product.productName} adicionado ao pedido {pedido.id}.")

            pedido.totalPrice += float(product.price) * quantidade
            pedido.save()

        except models.Product.DoesNotExist:
            print(f"Produto com ID {productId} não encontrado.")
        except ValueError:
            print("ID de product ou quantidade inválida. Digite um número inteiro.")
        except Exception as e:
            print(f"Erro ao adicionar item: {e}")
    print("Itens adicionados ao pedido.")


def ordersMenu():
    while (True):
        print("\n--- Menu de Pedidos ---")
        print("1 - Criar novo pedido")
        print("2 - Listar pedidos")
        print("3 - Adicionar item ao pedido")
        print("0 - Voltar")
        op = input("Escolha: ")

        if op == "1":
            try:
                userId = int(input("ID do cliente para este pedido: "))
                user = models.User.get_by_id(userId)
                newOrder = models.Order.create(user=user, orderDate=datetime.now(),
                                                totalPrice=0.0)  
                print(f"Pedido {newOrder.id} criado para o cliente {user.name}.")
                adicionar_itens_ao_pedido(
                    newOrder)  
            except models.User.DoesNotExist:
                print(f"Cliente com ID {userId} não encontrado.")
            except ValueError:
                print("ID inválido. Digite um número inteiro.")

        elif op == "2":
            print("\n--- Lista de Pedidos ---")
            for order in models.Order.select(models.Order, models.User).join(
                    models.User).order_by(models.Order.id):
                print(
                    f"ID: {order.id}, Cliente: {order.user.name} (ID: {order.user.id}), Data: {order.orderDate.strftime('%d/%m/%Y %H:%M:%S')}, Total: R$ {order.totalPrice:.2f}")
                print("Itens do Pedido:")
                for item in models.productOrder.select(models.productOrder, models.Product).join(
                        models.Product).where(models.productOrder.pedido == order):
                    print(f"  - {item.product.productName}  R$ {item.product.price} cada)")

        elif op == "3":
            try:
                orderId = int(input("ID do pedido para adicionar itens: "))
                order = models.Order.get_by_id(orderId)
                adicionar_itens_ao_pedido(order)  
            except models.Order.DoesNotExist:
                print(f"Pedido com ID {orderId} não encontrado.")
            except ValueError:
                print("ID de pedido inválido. Digite um número inteiro.")

        elif op == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
def menu():
    while(True):
        print("\n--- Menu Principal ---")
        print("1 - Clientes")
        print("2 - Produtos")
        print("3 - Pedidos")
        print("4 - Sair")
        option = input("Escolha: ")

        if option == "1":
            userMenu()
        elif option == "2":
            productsMenu()
        elif option == "3":
            ordersMenu()
        elif option == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu()