import sqlite3
from sqlite3 import Error
import base64

#Cria conexao com o banco de dados
def createConnection():
    conn = None
    try:
        conn = sqlite3.connect("DB/MMAmbiente.db")
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

#Fecha conexao com o banco de dados
def closeConnection():
    conn = createConnection()
    if conn:
        conn.close()

#Seleciona todos os cargos existentes
def selectCargos():
    conn = createConnection()
    cur = conn.cursor()
    return cur.execute('SELECT * FROM CARGOS ORDER BY id ASC')

#Seleciona todos os usuarios existentes, juntamente com cargo e nivel de acesso
def selectUsuarios():
    conn = createConnection()
    cur = conn.cursor()
    return cur.execute(f'''SELECT u.id AS id_usuario, u.usuario, u.nome AS nome_usuario, c.id AS id_cargo, c.nome AS nome_cargo, c.nvl_acesso
                                FROM USUARIOS u
                                LEFT JOIN CARGOS_USUARIOS ca ON ca.id_usuario = u.id
                                LEFT JOIN CARGOS c ON c.id = ca.id_cargo''')

#Seleciona as informacoes referentes ao usuario passado como parametro
def selectUsuario(usuario):
    conn = createConnection()
    cur = conn.cursor()
    return cur.execute(f'''SELECT u.id AS id_usuario, u.usuario, u.nome AS nome_usuario, c.id AS id_cargo, c.nome AS nome_cargo, c.nvl_acesso
                                FROM USUARIOS u
                                LEFT JOIN CARGOS_USUARIOS ca ON ca.id_usuario = u.id
                                LEFT JOIN CARGOS c ON c.id = ca.id_cargo
                                WHERE usuario = "{usuario}"''').fetchone()

#Verifica se existe um usuario com os parametros de login passado, retorna True ou False de acordo com o resultado
def autenticaUsuario(usuario, senha):
    conn = createConnection()
    cur = conn.cursor()
    cur.execute(f'''SELECT COUNT(id) FROM USUARIOS WHERE usuario = "{usuario}" AND senha="{encodeBase64(senha)}"''')
    return cur.fetchone()[0] > 0

#Codifica string passada para base64 (usado na senha, para autenticacao)
def encodeBase64(str):
    return base64.b64encode(str.encode("ascii")).decode("ascii")

#Decodifica string base64 passada
def decodeBase64(str):
    return base64.b64decode(str.encode("ascii")).decode("ascii")