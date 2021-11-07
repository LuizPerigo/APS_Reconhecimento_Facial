import shutil
import os

def createUserDir(usuario, imagePath):
    current_dir = os.getcwd()
    final_dir = os.path.join(current_dir, f'Images\{usuario}')
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    shutil.copy2(imagePath, final_dir)