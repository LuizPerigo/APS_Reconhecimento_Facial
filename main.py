from sqlite3 import dbapi2
import loadFaces
import faceRecognition
import DBConnection
import getpass
import fileControl
import re

#Carrega o menu inicial
def menuInicial():
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
        global dados_usuario #define a variavel global, pois sera usada diversas vezes em instancias diferentes da funcao openMenuAutenticado()
        dados_usuario = DBConnection.selectUsuario(usuario)
        print(f"Bem vindo {dados_usuario[4]} {dados_usuario[2]}, nível de acesso {dados_usuario[5]}")
        openMenuAutenticado()

#Lista os menus que o usuario tem acesso
def openMenuAutenticado():
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
            print("0 - Sair")
            menu_escolhido = input()
            #tenta converter para inteiro o valor recebido (assim programa nao para em caso de letras e simbolos),
            #pois o valor inteiro é comparado para saber se existe menu correspondente, assim parando o loop
            try:
                menu_escolhido = int(menu_escolhido)
                if menu_escolhido <= len(menu) and menu_escolhido >= 0:
                    break
                else:
                    print("Opção inválida")
            except:
                print("Opção inválida")
        #Se nao possui menu, exibe mensagem e para programa
        else:
            input("Seu nível de acesso não possui nenhuma funcionalidade do sistema liberada, contate um administrador.\nPressione enter para finalizar a aplicação")
            return

    #Se escolheu 0, fecha sistema
    if menu_escolhido == 0:
        fechaSistema()

    #Se chegou aqui, o usuario possui acesso a menus, neste caso ira seguir para a opção escolhida
    if menu[menu_escolhido-1][0] == "inserir_usuario":
        menuInserirUsuario()
    elif menu[menu_escolhido-1][0] == "excluir_usuario":
        menuExcluirUsuario()

#Inserir usuario
def menuInserirUsuario():
    novo_usuario = {"nome": None, "usuario": None, "senha": None, "cargo": None, "imagePath": None}
    #Loop ate digitar nome valido
    while True:
        novo_usuario["nome"] = input("Nome: ")
        #Se for nome valido, para loop
        if validaCampoUsuario(novo_usuario["nome"], "nome"):
            break
        else:
            print("Nome inválido, deve conter ao menos 3 caracteres")
    #Loop ate digitar usuario valido
    while True:
        novo_usuario["usuario"] = input("Usuário: ")
        #Se for usuario valido, para loop
        if validaCampoUsuario(novo_usuario["usuario"], "usuario"):
            break
        else:
            print("Usuário inválido, deve conter de 5 a 20 caracteres e somente letras, números e underline (_)")
    #Loop ate digitar senha valida
    while True:
        novo_usuario["senha"] = getpass.getpass("Senha: ")
        #Se for senha valida, para loop
        if validaCampoUsuario(novo_usuario["senha"], "senha"):
            novo_usuario["senha"] = DBConnection.encodeBase64(novo_usuario["senha"])
            break
        else:
            print("Senha inválida, deve conter ao menos 8 caracteres")
    
    #Busca cargos do sistema
    lista_cargos = DBConnection.selectCargos()
    #Loop até escolher um cargo valido
    while True:
        print("Cargos:")
        #Lista os cargos
        for idx in range(len(lista_cargos)):
            print(f"{idx+1} - {lista_cargos[idx][1]}")
        cargo_escolhido = input("Qual será o cargo do usuário?\n")
        #Tenta converter o valor recebido para inteiro (evita erro em caso de letras e simbolos)
        try:
            cargo_escolhido = int(cargo_escolhido)
            #Se for um valor correspondente a um cargo, para o loop
            if cargo_escolhido <= len(lista_cargos) and cargo_escolhido > 0:
                novo_usuario["cargo"] = lista_cargos[cargo_escolhido-1][0] #pegar id do cargo
                break
            else:
                print("Opção inválida")
        except:
            print("Opção inválida")

    #Loop até selecionar uma imagem valida
    while True:
        print("Selecione uma foto para o reconhecimento facial (que tenha somente você e com o rosto visível)")
        #Abre file explorer
        novo_usuario["imagePath"] = fileControl.openImageSelector()
        #Valida faces reconhecidas na imagem
        numero_faces = loadFaces.detectFacesFromImage(novo_usuario["imagePath"])
        if numero_faces == 1:
            break
        elif numero_faces > 1:
            print("Foi detectada mais de uma face na imagem selecionada")
        else:
            print("Nenhuma face foi reconhecida")

    #Se chegou aqui, as entradas acima foram validas e tenta inserir o usuario
    if DBConnection.inserirUsuario(novo_usuario):
        print("Usuário inserido com sucesso.")
    else:
        print("Falha ao inserir usuário.")
    openMenuAutenticado()

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
            else:
                print("Opção inválida")
        except:
            print("Opção inválida")
    #Manda excluir o usuario e exibe mensagem de acordo com o resultado
    if DBConnection.excluirUsuario(lista_usuarios[idx_usuario_excluir-1][0], lista_usuarios[idx_usuario_excluir-1][1]):
        print("Usuário excluído com sucesso")
    else:
        print("Falha ao excluir usuário")
    openMenuAutenticado()

#Valida se campo é valido
def validaCampoUsuario(valor, campo):
    #minimo de 3 caracteres para nome
    if campo == "nome":
        return len(valor) > 2
    #5 a 20 caracteres, sendo eles letras, numeros e underline para usuario, alem de que nao pode existir alguem com o mesmo usuario
    elif campo == "usuario":  
        pattern = re.compile("^[A-Za-z0-9_]{5,20}$")
        return bool(pattern.match(valor)) and not DBConnection.verificaUsuarioExiste(valor) and valor != "TIMEOUT" and valor != "Desconhecido"
    #minimo de 8 caracteres para senha
    elif campo == "senha":
        return len(valor) > 7

#Para a aplicacao
def fechaSistema():
    exit()

if __name__ == '__main__':
    print("Bem-vindo ao sistema do Ministério do Meio Ambiente")
    menuInicial()