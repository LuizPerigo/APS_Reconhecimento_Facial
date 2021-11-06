import sqlite3
from sqlite3 import Error
import base64

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect("DB/MMAmbiente.db")
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

def closeConnection():
    conn = createConnection()
    if conn:
        conn.close()

def selectCargos():
    conn = createConnection()
    cur = conn.cursor()
    return cur.execute('SELECT * FROM CARGOS ORDER BY id ASC')

def selectUsuarios():
    conn = createConnection()
    cur = conn.cursor()
    return cur.execute(f'''SELECT u.id AS id_usuario, u.usuario, u.nome AS nome_usuario, c.id AS id_cargo, c.nome AS nome_cargo, c.nvl_acesso
                                FROM USUARIOS u
                                LEFT JOIN CARGOS_USUARIOS ca ON ca.id_usuario = u.id
                                LEFT JOIN CARGOS c ON c.id = ca.id_cargo''')

def selectUsuario(usuario):
    conn = createConnection()
    cur = conn.cursor()
    return cur.execute(f'''SELECT u.id AS id_usuario, u.usuario, u.nome AS nome_usuario, c.id AS id_cargo, c.nome AS nome_cargo, c.nvl_acesso
                                FROM USUARIOS u
                                LEFT JOIN CARGOS_USUARIOS ca ON ca.id_usuario = u.id
                                LEFT JOIN CARGOS c ON c.id = ca.id_cargo
                                WHERE usuario = "{usuario}"''').fetchone()

def autenticaUsuario(usuario, senha):
    conn = createConnection()
    cur = conn.cursor()
    cur.execute(f'''SELECT COUNT(id) FROM USUARIOS WHERE usuario = "{usuario}" AND senha="{encodeBase64(senha)}"''')
    return cur.fetchone()[0] > 0

def encodeBase64(str):
    return base64.b64encode(str.encode("ascii")).decode("ascii")

def decodeBase64(str):
    return base64.b64decode(str.encode("ascii")).decode("ascii")
    
# if __name__ == '__main__':
#     conn = createConnection()