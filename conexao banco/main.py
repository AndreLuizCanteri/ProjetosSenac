from DAO import UsuarioDAO
class Main ():
    def menu():
        dao = UsuarioDAO()
        while True:
            pergunta  = input(
            """1 - Cadastrar \n
            2- Login \n
            3 - Consultar \n
            4 - Remover \n
            5 - Sair \n"""
        )
        
            if pergunta == '1':
                usuario = input("Digite o usuario:\n")
                email = input ("Digite o email:\n")
                senha = input ("Digite a senha:\n")

                if dao.cadastrar(usuario, email, senha):
                        print ("Cadastro realizado com exito")

                else:
                    print("Não foi possivel fazer o cadastro")

            if pergunta == '2':
                email = input("Digite o email:\n")
                senha = input("Digite a senha:\n")

                if dao.autenticar(email, senha):
                    print("Foi realizado o login")
                else:
                    print("Não foi possivel fazer o login")

            if pergunta == '3':
                print(f"Os dados são {dao.consultar_todos()}")

            if pergunta == '4':
                email = input("Informe o email")

                if dao.remover(email):
                    print("O email foi removido com exito")

            if pergunta == '5':
                print("saindo..")
                break

if __name__ == "__main__":
    Main.menu()