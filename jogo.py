import cv2

# cor padrão para desenhos e textos.
roxinho = (115, 50, 168)

#converte a imagem para cinza.
def imagem_video_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray

#identifica a imagem de movimento, e imprime o texto na tela
def identifica_movimento(img, ref, texto):
    #Classificador do movimento
    movimentoCascade = cv2.CascadeClassifier(str(ref))

    #detecta o movimento na imagem
    movimento = movimentoCascade.detectMultiScale(img, minNeighbors=20, minSize=(30, 30), maxSize=(500,500))

    # Desenha um retangulo nos movimentos detectados
    for (x, y, w, h) in movimento:
        cv2.rectangle(img, (x, y), (x+w, y+h), roxinho, 4)
        cv2.putText(img, str(texto), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1, roxinho, 2, cv2.LINE_AA)
    return movimento

#Cria uma janela onde o vídeo irá rodar.
cv2.namedWindow("checkpoint")
video = cv2.VideoCapture("pedra-papel-tesoura.mp4")

#Se o vídeo estiver rodando, ele continua exacutando o script
if video.isOpened(): 
    rval, frame = video.read()
#Se o vídeo não estiver rodando, o script para
else:
    rval = False

while rval:

    #Pega o frame atual e o transforma em tom de cinza.
    gray = imagem_video_gray(frame)

    #Identifica o movimento pedra
    identifica_movimento(gray,'imagens/pedra.png','Pedra')
    
    #Identifica o movimento tesoura
    identifica_movimento(gray,'imagens/tesoura.png','Tesoura')
    
    #Identifica o movimento papel
    identifica_movimento(gray,'imagens/papel.png','Papel')

    #Exibe a imagem scriptada.
    cv2.imshow("checkpoint", gray)

    #Leitura do vídeo, frame a frame.
    rval, frame = video.read()
    

    key = cv2.waitKey(20)

    #Caso a tecla ESC for pressionada, o vídeo para. 
    if key == 27:
        break

#Destroí a janela criada e para de executar o vídeo.
cv2.destroyWindow("checkpoint")
video.release()
