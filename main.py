import loadFaces
import faceRecognition
import DBConnection
import getpass

if __name__ == '__main__':
    # loadFaces.loadFacesFromDir()
    # faceRecognition.openFaceRecognition()
    print("Bem-vindo ao sistema do Ministério do Meio Ambiente")
    print("O que deseja fazer?")
    while True:
        acao = int(input("1 - Login\n0 - Sair\n"))
        if acao == 0 or acao == 1:
            break

    if acao == 1:

        while True:
            usuario = input("Usuario: ")
            senha = getpass.getpass("Senha: ") #similar ao input, mas nao mostra o que ta sendo digitado
            autenticou = DBConnection.autenticaUsuario(usuario, senha)
            if autenticou:
                break
            else:
                print("Usuário e senha incorretos")

        if(usuario == "admin"):
            #mostra opcoes de admin
            print("Autenticou como admin")
        else:
            usuario_fr = faceRecognition.openFaceRecognition()
            if usuario_fr == "TIMEOUT":
                print("Tempo para autenticação facial esgotado")
            else:
                if(usuario_fr == usuario):
                    dados_usuario = DBConnection.selectUsuario(usuario)
                    print(f"Bem vindo {dados_usuario[4]} {dados_usuario[2]}, nível de acesso {dados_usuario[5]}")
                else:
                    print("Reconhecimento facial falhou, a face reconhecida não pertence ao usuário utilizado")
            
    elif acao == 0:
        exit()