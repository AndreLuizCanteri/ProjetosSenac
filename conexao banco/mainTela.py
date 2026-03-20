from DAO import UsuarioDAO
from PyQt5 import QtWidgets, uic

# Telas da main 
def cadastro():
    dao = UsuarioDAO
    usuario = telaCadastro.line_usuario.text()
    email = telaCadastro.line_email.text()
    senha = telaCadastro.line_Senha.text()
    if usuario == "" and email == "" and senha == "":
        if dao.cadastrar (usuario, email, senha):
            print ("Cadastro realizado com exito")
        else:
            print ("Não foi possivel fazer o cadastro ")

def Login ():
    dao = UsuarioDAO
    email = telaLogin.line_email.text()
    senha = telaLogin.line_senha.text()
    if email == "" and senha == "":
        if dao.autenticar(email, senha):
            print ("Login feito com exito")

def Consulta():
    dao = UsuarioDAO
    telaConsulta.obj_branco.setText(f"{dao.consultar_todos()}")

def Remover():
    dao = UsuarioDAO
    email = telaRemover.line_email.text()
    if dao.remover(email):
        print("O email de usuario foi removido com exito")


#Fechar e abrir a proxima tela 
def Telacadastro():
    telaMain.close()
    telaCadastro.show()

def Telalogin():
    telaMain.close()
    telaLogin.show()

def TelaConsulta():
    telaMain.close()
    telaConsulta.show()

def TelaRemover():
    telaMain.close()
    telaRemover.show()

def Sair():
    telaMain.close()


#Botão voltar das telas
def VoltaCadastro():
    telaCadastro.close()
    telaMain.show()

def VoltaLogin():
    telaLogin.close()
    telaMain.show()

def VoltaConsulta():
    telaConsulta.close()
    telaMain.show()

def VoltaRemover():
    telaRemover.close()
    telaMain.show()

app = QtWidgets.QApplication([])
telaMain = uic.loadUi("tela_main.ui")
telaCadastro = uic.loadUi("tela_cadastro.ui")
telaLogin = uic.loadUi("tela_login.ui")
telaConsulta = uic.loadUi("tela_consulta.ui")
telaRemover = uic.loadUi("tela_remover.ui")

#Tela cadastro
telaCadastro.btn_cadastrar.clicked.connect(cadastro)
telaMain.btn_cadastro.clicked.connect(Telacadastro)
telaCadastro.btn_voltar.clicked.connect(VoltaCadastro)

#Tela Login
telaLogin.btn_login.clicked.connect(Login)
telaMain.btn_Login.clicked.connect(Telalogin)
telaLogin.btn_voltar.clicked.connect(VoltaLogin)

#Tela Consulta
telaMain.btn_consultar.clicked.connect(TelaConsulta)
telaConsulta.btn_voltar.clicked.connect(VoltaConsulta)

#Tela Remover
telaRemover.btn_remover.clicked.connect(Remover)
telaMain.btn_remover.clicked.connect(TelaRemover)
telaRemover.btn_voltar.clicked.connect(VoltaRemover)

#Botao Sair
telaMain.btn_sair.clicked.connect(Sair)

telaMain.show()
app.exec_()