import face_recognition
import imutils
import pickle
import time
import cv2
import os

def openFaceRecognition():
    #caminho para o arquivo xml haarcascade
    cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    #carrega o xml no classificador
    faceCascade = cv2.CascadeClassifier(cascPathface)
    #carrega as faces conhecidas salvas no ultimo arquivo encoding gerado
    data = pickle.loads(open('face_enc', "rb").read())

    video_capture = cv2.VideoCapture(0)
    #armazenar quantidade de matches por pessoa
    counts = {}
    #armazenar quando houver mais de 5 matches em uma pessoa, para entao dar sequencia na autenticacao
    fiveMatches = {'hasFiveMatches': False, 'nameFiveMatches': ''}
    #loop para procurar um match
    while True:
        #ler conteudo do video
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(60, 60),
                                            flags=cv2.CASCADE_SCALE_IMAGE)

        #converter frame de BGR para RGB 
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #gera os face_encodings das faces reconhecidas no frame recebido do video
        encodings = face_recognition.face_encodings(rgb)
        names = []
        #percorre os encoding identificados no video
        for encoding in encodings:
            #compara video encodings com os encondings salvos em arquivo
            matches = face_recognition.compare_faces(data["encodings"],
            encoding)
            #nome padrao desconhecido (evita problema nos objetos de match)
            name = "Desconhecido"
            #se houve um match
            if True in matches:
                #salva posicoes(faces) que tiveram match
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                #percorre as posicoes com match e salva a quantidade de matches que essa face teve
                for i in matchedIdxs:
                    #nome da face reconhecida
                    name = data["names"][i]
                    #aumenta quantidade de vezes que a face foi reconhecida na execucao atual
                    counts[name] = counts.get(name, 0) + 1

            #se o nome ja teve mais de 5 matches, salva no objeto para prosseguir a autenticacao
            if counts.get(name, 0) >= 5:
                fiveMatches['hasFiveMatches'] = True
                fiveMatches['nameFiveMatches'] = name

            #INICIO - Desenha um quadro na tela de video com o nome - TEMPORARIO
            names.append(name)
            for ((x, y, w, h), name) in zip(faces, names):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)
            #FIM - Desenha um quadro na tela de video com o nome - TEMPORARIO

        cv2.imshow("Frame", frame)
        if fiveMatches['hasFiveMatches']:
            #se tem os 5 matches, ira parar o loop para seguir com a autenticacao
            break
        #escape do video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    print(f"Autenticar como {fiveMatches['nameFiveMatches']}")