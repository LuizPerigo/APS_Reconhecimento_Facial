from imutils import paths
import face_recognition
import pickle
import cv2
import os

#Carrega faces do diretorios de imagens para gerar arquivo com os encodings
def loadFacesFromDir():
    #pega o caminho dos arquivos na pasta Images(cada pessoa cadastrada deve ter um pasta aqui dentro com seu usuario[sera usado na autenticacao])
    imagePaths = list(paths.list_images('Images'))
    knownEncodings = []
    knownNames = []
    #percorre as imagens
    for (i, imagePath) in enumerate(imagePaths):
        #extrai o usuario do caminho da imagem
        name = imagePath.split(os.path.sep)[-2]
        # carrega imagem e converte de BGR para RGB
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #usa face_recognition para localizar faces na imagem
        boxes = face_recognition.face_locations(rgb,model='hog')
        #gera o encoding das faces reconhecidas
        encodings = face_recognition.face_encodings(rgb, boxes)
        #percorre os encodings
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
    #salva os encodings com o usuario
    data = {"encodings": knownEncodings, "names": knownNames}
    #salva os encodings em um arquivo, que sera usado na comparacao com video
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()

#Detecta se imagem possui faces e retorna a quantidade
def detectFacesFromImage(imagePath):
    #Cria arquivo haar
    cascPath = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    #Le a imagem e transforma ela em cinza
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Detecta faces na imagem cinza
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    #Retorna quantidade de faces detectadas
    return len(faces)