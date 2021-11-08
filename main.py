from sqlite3 import dbapi2
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
                else:
                    print("Opção inválida")
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

#Lista os menus que o usuario tem acesso
def openMenuAutenticado(dados_usuario):
    print(f"Bem vindo {dados_usuario[4]} {dados_usuario[2]}, nível de acesso {dados_usuario[5]}")

    #Busca os menus que o usuario tem acesso
    menu = DBConnection.getMenuUsuario(dados_usuario[5])

    #Fica em loop ate escolher um menu valido
    while True:
        #Se possui ao menos um menu exibe
        if len(menu) > 0:
            print("O que deseja fazer?")

            #percorre os menus para listar
            for idx in range(len(menu)):
                print(f"{idx+1} - {menu[idx][1]}")
            menu_escolhido = input()
            #tenta converter para inteiro o valor recebido (assim programa nao para em caso de letras e simbolos),
            #pois o valor inteiro é comparado para saber se existe menu correspondente, assim parando o loop
            try:
                menu_escolhido = int(menu_escolhido)
                if menu_escolhido <= len(menu) and menu_escolhido > 0:
                    break
                else:
                    print("Opção inválida")
            except:
                print("Opção inválida")
        #Se nao possui menu, exibe mensagem e para programa
        else:
            print("Seu nível de acesso não possui nenhuma funcionalidade do sistema liberada, contate um administrador")
            return

    #Se chegou aqui, o usuario possui acesso a menus, neste caso ira seguir para a opção escolhida
    if menu[menu_escolhido-1][0] == "inserir_usuario":
        menuInserirUsuario()
    elif menu[menu_escolhido-1][0] == "excluir_usuario":
        menuExcluirUsuario()

#Inserir usuario
def menuInserirUsuario():
    print("I")

#Excluir usuario
def menuExcluirUsuario():
    #Busca todos os usuarios do sistema
    lista_usuarios = DBConnection.selectUsuarios()
    #Loop até escolher um usuario valido
    while True:
        print("Usuários cadastrados no sistema:")
        #Lista os usuarios
        for idx in range(len(lista_usuarios)):
            print(f"{idx+1} - {lista_usuarios[idx][4]} {lista_usuarios[idx][2]}")
        idx_usuario_excluir = input("Qual dos usuários acima deseja excluir?\n")
        #Tenta converter o valor recebido para inteiro (evita erro em caso de letras e simbolos)
        try:
            idx_usuario_excluir = int(idx_usuario_excluir)
            #Se for um valor correspondente a um usuario, para o loop
            if idx_usuario_excluir <= len(lista_usuarios) and idx_usuario_excluir > 0:
                break
        except:
            None
    #Manda excluir o usuario e exibe mensagem de acordo com o resultado
    if DBConnection.excluirUsuario(lista_usuarios[idx_usuario_excluir-1][0]):
        print("Usuário excluído com sucesso")
    else:
        print("Falha ao excluir usuário")

#Para a aplicacao
def fechaSistema():
    exit()

if __name__ == '__main__':
    menuInicial()