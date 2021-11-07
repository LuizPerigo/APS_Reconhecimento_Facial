import loadFaces
import faceRecognition
import DBConnection
import getpass

#Carrega o menu inicial
def menuInicial():
    print("Bem-vindo ao sistema do Ministério do Meio Ambiente")
    print("O que deseja fazer?")
    #Fica na pergunta ate que seja digitado um valor aceito
    while True:
        acao = input("1 - Login\n0 - Sair\n")
        if acao == "0" or acao == "1":
            break
    opcAcao(acao)

#Chama a opcao escolhida pelo usuario
def opcAcao(acao):
    if acao == "1":
        login()
    elif acao == "0":
        fechaSistema()

#Abre o login
def login():
    autenticacao_completa = False
    #Fica no login ate que seja autenticado com sucesso, ou o usuario decida parar
    retry = None
    while True:
        usuario = input("Usuario: ")
        senha = getpass.getpass("Senha: ") #similar ao input, mas nao mostra o que ta sendo digitado
        autenticou = DBConnection.autenticaUsuario(usuario, senha)
        if autenticou:
            break
        else:
            print("Usuário e senha incorretos")
            while True:
                retry = input("Deseja tentar novamente?(s/n): ")
                if retry == "n" or retry == "N" or retry == "s" or retry == "S":
                    break
            if retry == "n" or retry == "N":
                menuInicial()
                return

    #Se for admin, nao faz reconhecimento facial
    if(usuario == "admin"):
        #Para o admin, a autenticacao ja esta completa
        autenticacao_completa = True
    else:
        #Para os outros usuario, abre o reconhecimento facial
        usuario_fr = faceRecognition.openFaceRecognition()
        #Se nao reconhecer ninguem em 60 segundos, a funcao faceRecognition.openFaceRecognition() retorna TIMEOUT, nesse caso o usuario volta para o menu inicial
        if usuario_fr == "TIMEOUT":
            print("Tempo para autenticação facial esgotado")
            menuInicial()
            return
        else:
            #Se reconhecer alguem, checa se o usuario informado bate com o do rosto reconhecido
            if(usuario_fr == usuario):
                #Para outros usuarios, a autenticacao esta completa
                autenticacao_completa = True
            else:
                #Se os usuarios nao baterem, volta para o menu inicial
                print("Reconhecimento facial falhou, a face reconhecida não pertence ao usuário utilizado")
                menuInicial()
                return

    #Se chegou aqui, teve sucesso em toda a autenticacao
    if(autenticacao_completa):
        #Abre as opcoes que o usuario tem no sistema, de acordo com nivel de acesso
        dados_usuario = DBConnection.selectUsuario(usuario)
        openMenuAutenticado(dados_usuario)

def openMenuAutenticado(dados_usuario):
    print(f"Bem vindo {dados_usuario[4]} {dados_usuario[2]}, nível de acesso {dados_usuario[5]}")
    menu = getMenuUsuario(dados_usuario[1], dados_usuario[5])
    print(menu)

#Retorna o menu que o usuario tem acesso apos login
def getMenuUsuario(usuario, nvl_acesso):
    menu = ["menu"]
    return menu

#Para a aplicacao
def fechaSistema():
    exit()

if __name__ == '__main__':
    menuInicial()