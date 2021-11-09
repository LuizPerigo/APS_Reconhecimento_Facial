import shutil
import os
import tkinter as tk
from tkinter import filedialog

def createUserDir(usuario, imagePath):
    current_dir = os.getcwd()
    final_dir = os.path.join(current_dir, f'Images\{usuario}')
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    shutil.copy2(imagePath, final_dir)

def openImageSelector():
    #TK cria uma UI para abrir o file explorer, com o codigo abaixo essa janela é oculta
    root = tk.Tk()
    root.withdraw()

    #Abre explorador de arquivos
    image_path = filedialog.askopenfilename(initialdir = "/",
                                          title = "Selecione uma imagem",
                                          filetypes=[
                                                    ('Imagens', ('.jpg', '.jpeg')),
                                                    ('Todos os arquivos', '.*')
                                                ])
    return image_path

def deleteUserDir(usuario):
    shutil.rmtree(f"Images/{usuario}")